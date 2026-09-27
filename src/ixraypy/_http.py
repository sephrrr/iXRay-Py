"""HTTP transport shared by every resource: auth, retries on token expiry, error mapping."""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator, Callable, Mapping
from datetime import datetime
from enum import Enum
from typing import Any

import httpx
from pydantic import BaseModel

from ixraypy.exceptions import APIError, AuthenticationError, TransportError, error_for

TokenProvider = Callable[[], "asyncio.Future[str] | Any"]


def _clean(values: Mapping[str, Any]) -> dict[str, Any]:
    """Drop ``None`` values and serialise enums and datetimes for query strings and forms."""
    out: dict[str, Any] = {}
    for k, v in values.items():
        if v is None:
            continue
        out[k] = _scalar(v)
    return out


def _scalar(v: Any) -> Any:
    if isinstance(v, Enum):
        return v.value
    if isinstance(v, datetime):
        return v.isoformat()
    if isinstance(v, list | tuple | set):
        return [_scalar(x) for x in v]
    if isinstance(v, bool):
        return "true" if v else "false"
    return v


def _dump(body: Any) -> Any:
    """Turn a model (or nested models) into JSON-ready data, keeping explicitly set fields only."""
    if isinstance(body, BaseModel):
        return body.model_dump(mode="json", exclude_unset=True, by_alias=True)
    if isinstance(body, dict):
        return {k: _dump(v) for k, v in body.items()}
    if isinstance(body, list):
        return [_dump(v) for v in body]
    return body


def _fmt(template: str, values: Mapping[str, Any]) -> str:
    """Fill ``{name}`` placeholders of a path with URL-safe values."""
    out = template
    for k, v in values.items():
        if isinstance(v, Enum):
            v = v.value
        out = out.replace("{" + k + "}", httpx.URL(path=str(v)).path.lstrip("/") if "/" in str(v) else str(v))
    return out


class HttpTransport:
    """Thin wrapper over :class:`httpx.AsyncClient`.

    Not part of the public API; use :class:`ixraypy.IXRayClient`.
    """

    def __init__(
        self,
        base_url: str,
        *,
        api_key: str | None,
        token: str | None,
        login: Callable[[], Any] | None,
        timeout: float,
        verify: bool | str,
        user_agent: str,
        client: httpx.AsyncClient | None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.token = token
        self._login = login
        self._client = client or httpx.AsyncClient(
            base_url=self.base_url,
            timeout=timeout,
            verify=verify,
            headers={"User-Agent": user_agent},
        )
        self._owns_client = client is None
        self._lock = asyncio.Lock()
        self._in_login = False

    async def aclose(self) -> None:
        if self._owns_client:
            await self._client.aclose()

    def _auth_headers(self) -> dict[str, str]:
        if self._in_login:
            return {}
        if self.api_key:
            return {"X-Api-Key": self.api_key}
        if self.token:
            return {"Authorization": f"Bearer {self.token}"}
        return {}

    async def ensure_auth(self) -> None:
        """Log in once when only username/password were given."""
        if self.api_key or self.token or self._login is None or self._in_login:
            return
        async with self._lock:
            if not self.token:
                await self.run_login()

    async def run_login(self) -> None:
        """Call the login hook with auth headers and the auth guard switched off."""
        if self._login is None:
            return
        self._in_login = True
        try:
            await self._login()
        finally:
            self._in_login = False

    async def _send(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        headers: Mapping[str, Any] | None = None,
        json: Any = None,
        data: Mapping[str, Any] | None = None,
        files: Any = None,
        stream: bool = False,
        _retry: bool = True,
    ) -> httpx.Response:
        await self.ensure_auth()
        h = {**self._auth_headers(), **(headers or {})}
        try:
            req = self._client.build_request(
                method.upper(), path, params=params, headers=h, json=json, data=data, files=files
            )
            resp = await self._client.send(req, stream=stream)
        except httpx.HTTPError as exc:  # network level
            raise TransportError(str(exc)) from exc
        if resp.status_code == 401 and _retry and self._login is not None and not self.api_key and not self._in_login:
            # Token expired: log in again and replay once.
            if stream:
                await resp.aclose()
            else:
                await resp.aread()
            async with self._lock:
                self.token = None
                await self.run_login()
            return await self._send(
                method,
                path,
                params=params,
                headers=headers,
                json=json,
                data=data,
                files=files,
                stream=stream,
                _retry=False,
            )
        if resp.status_code >= 400:
            if stream:
                await resp.aread()
            raise self._error(resp)
        return resp

    @staticmethod
    def _error(resp: httpx.Response) -> APIError:
        body: Any = None
        detail: Any = resp.text
        try:
            body = resp.json()
        except ValueError:
            body = None
        if isinstance(body, dict):
            detail = body.get("detail", body)
        return error_for(resp.status_code, detail, body)

    async def request(self, method: str, path: str, **kw: Any) -> Any:
        """Send a request and decode the body: JSON when the panel says so, text otherwise, ``None`` when empty."""
        resp = await self._send(method, path, **kw)
        if resp.status_code == 204 or not resp.content:
            return None
        ctype = resp.headers.get("content-type", "")
        if "json" in ctype:
            return resp.json()
        return resp.text

    async def request_bytes(self, method: str, path: str, **kw: Any) -> bytes:
        resp = await self._send(method, path, **kw)
        return resp.content

    async def stream_sse(self, method: str, path: str, **kw: Any) -> AsyncIterator[str]:
        """Yield the ``data:`` payload of each server-sent event."""
        resp = await self._send(method, path, stream=True, **kw)
        try:
            async for line in resp.aiter_lines():
                if line.startswith("data:"):
                    yield line[5:].lstrip()
        finally:
            await resp.aclose()


__all__ = ["HttpTransport", "AuthenticationError", "_clean", "_dump", "_fmt"]
