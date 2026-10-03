"""The public client."""

from __future__ import annotations

from typing import Any

import httpx

from ixraypy import __version__
from ixraypy._http import HttpTransport
from ixraypy.models import Token
from ixraypy.resources import (
    AdminResource,
    AdminRolesResource,
    ApiKeysResource,
    BackupsResource,
    ClientTemplatesResource,
    CoresResource,
    GroupsResource,
    HostsResource,
    HwidsResource,
    MiscResource,
    NodesResource,
    PushResource,
    SettingsResource,
    SetupResource,
    SubscriptionResource,
    SystemResource,
    UsersResource,
    UserTemplatesResource,
)


class IXRayClient:
    """Async client for an iXRay panel.

    Authenticate with one of:

    * an API key created in the panel (``ix_key_...``), sent as ``X-Api-Key``;
    * an admin username and password (and ``otp`` when two-factor is on): the
      client logs in on first use and logs in again when the token expires;
    * a ready-made bearer ``token``.

    Use it as an async context manager so the connection pool is closed::

        async with IXRayClient("https://panel.example.com", api_key="ix_key_...") as ix:
            me = await ix.admin.get_current_admin()

    Every endpoint of the panel is reachable through the resource attributes
    (``users``, ``nodes``, ``cores``...); method names follow the API's
    operation ids, so ``GET /api/users`` is ``ix.users.get_users()``.

    Args:
        base_url: Panel origin, for example ``https://panel.example.com``.
        api_key: API key from *Settings → API keys*.
        username: Admin username, used with ``password``.
        password: Admin password.
        otp: Current two-factor code, only needed at login when 2FA is enabled.
        token: Existing bearer token, if you already have one.
        timeout: Per-request timeout in seconds.
        verify: TLS verification flag or path to a CA bundle.
        http_client: Bring your own :class:`httpx.AsyncClient` (it will not be closed).
    """

    def __init__(
        self,
        base_url: str,
        *,
        api_key: str | None = None,
        username: str | None = None,
        password: str | None = None,
        otp: str | None = None,
        token: str | None = None,
        timeout: float = 30.0,
        verify: bool | str = True,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        if not any((api_key, token, username and password)):
            raise ValueError("give api_key, token, or username and password")
        self._username = username
        self._password = password
        self._otp = otp
        self._http = HttpTransport(
            base_url,
            api_key=api_key,
            token=token,
            login=self.login if username and password else None,
            timeout=timeout,
            verify=verify,
            user_agent=f"ixraypy/{__version__}",
            client=http_client,
        )
        self.admin = AdminResource(self._http)
        self.admins = self.admin  # alias
        self.admin_roles = AdminRolesResource(self._http)
        self.api_keys = ApiKeysResource(self._http)
        self.backups = BackupsResource(self._http)
        self.client_templates = ClientTemplatesResource(self._http)
        self.cores = CoresResource(self._http)
        self.groups = GroupsResource(self._http)
        self.hosts = HostsResource(self._http)
        self.hwids = HwidsResource(self._http)
        self.push = PushResource(self._http)
        self.misc = MiscResource(self._http)
        self.nodes = NodesResource(self._http)
        self.settings = SettingsResource(self._http)
        self.setup = SetupResource(self._http)
        self.subscription = SubscriptionResource(self._http)
        self.system = SystemResource(self._http)
        self.user_templates = UserTemplatesResource(self._http)
        self.users = UsersResource(self._http)

    @property
    def token(self) -> str | None:
        """Bearer token currently in use (``None`` with API-key auth or before login)."""
        return self._http.token

    async def login(self, otp: str | None = None) -> Token:
        """Exchange username/password (and ``otp``) for a bearer token and keep it.

        Raises:
            OTPRequiredError: two-factor is enabled and no code was given.
            AuthenticationError: wrong username or password.
        """
        if not (self._username and self._password):
            raise ValueError("login needs username and password")
        code = otp if otp is not None else self._otp
        was = self._http._in_login
        self._http._in_login = True  # the token call itself must not trigger or carry auth
        try:
            tok = await self.admin.admin_token(username=self._username, password=self._password, otp=code)
        finally:
            self._http._in_login = was
        self._http.token = tok.access_token
        return tok

    async def health(self) -> Any:
        """``GET /health``: liveness of the panel."""
        return await self.misc.health()

    async def aclose(self) -> None:
        """Close the underlying connection pool."""
        await self._http.aclose()

    async def __aenter__(self) -> IXRayClient:
        return self

    async def __aexit__(self, *exc: object) -> None:
        await self.aclose()
