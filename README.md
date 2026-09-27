# ixraypy

Async Python client for the [iXRay](https://github.com/sephrrr/iXRay-Panel) panel API.

Every one of the panel's 229 endpoints is available as a typed `async` method,
with pydantic v2 models for requests and responses, API-key or password
authentication (two-factor supported), automatic re-login on token expiry,
typed exceptions, and streaming of node logs.

```bash
pip install git+https://github.com/sephrrr/iXRay-Py.git
```

Requires Python 3.11 or newer.

## Quick start

```python
import asyncio
from ixraypy import IXRayClient, models


async def main() -> None:
    async with IXRayClient("https://panel.example.com", api_key="ix_key_...") as ix:
        me = await ix.admin.get_current_admin()
        print(me.username, me.role.name)

        page = await ix.users.get_users(limit=20, status=[models.UserStatus.active])
        for user in page.users:
            print(user.username, user.used_traffic, user.expire)

        created = await ix.users.create_user(
            body=models.UserCreate(username="alice", group_ids=[1], data_limit=50 * 1024**3)
        )
        print(created.subscription_url)


asyncio.run(main())
```

### Authentication

| Method | Constructor arguments | Notes |
|---|---|---|
| API key | `api_key="ix_key_..."` | Created in *Settings → API keys*. Sent as `X-Api-Key`. Recommended for integrations. |
| Password | `username=..., password=...` | Logs in on first call; logs in again when the token expires. |
| Password + 2FA | `username=..., password=..., otp="123456"` | Or call `await ix.login(otp="123456")` yourself. |
| Existing token | `token="..."` | A bearer token you obtained elsewhere. |

If an admin has two-factor enabled and no code is given, `OTPRequiredError` is raised.

### Resources

Endpoints are grouped the same way as the panel's OpenAPI tags:

| Attribute | What it covers |
|---|---|
| `ix.users` | users, usage, subscriptions, bulk operations, templates applied to users, events, IPs |
| `ix.nodes` | nodes, reconnect/sync, realtime stats, online counts, logs (SSE), routing rules |
| `ix.cores` | core configs (Xray, sing-box, Hysteria2, MTProto, OpenVPN, WireGuard), outbound stats, restart |
| `ix.hosts` | subscription hosts |
| `ix.groups` | groups and their inbounds |
| `ix.user_templates`, `ix.client_templates` | user plans and client config templates |
| `ix.admin`, `ix.admin_roles`, `ix.api_keys` | admins, roles, two-factor, API keys |
| `ix.hwids` | device (HWID) records of a user |
| `ix.settings`, `ix.backups`, `ix.system`, `ix.setup` | panel settings, database backups, system stats, first-run setup |
| `ix.subscription` | the public `/sub/{token}` endpoints clients use |

Method names are the API operation ids, so `PUT /api/user/{username}` is
`ix.users.modify_user(username, body=...)`. See [docs/reference.md](docs/reference.md)
for the full list and [docs/models.md](docs/models.md) for the models.

### Errors

All errors derive from `ixraypy.IXRayError`:

```python
from ixraypy import NotFoundError, PermissionDeniedError, ValidationError

try:
    await ix.users.get_user("ghost")
except NotFoundError as e:
    print(e.status_code, e.detail)
```

| Exception | Status |
|---|---|
| `TransportError` | network failure, timeout |
| `AuthenticationError` / `OTPRequiredError` | 401 |
| `PermissionDeniedError` | 403 |
| `NotFoundError` | 404 |
| `ConflictError` | 409 |
| `ValidationError` | 422 (`detail` holds the field errors) |
| `RateLimitedError` | 429 |
| `ServerError` | 5xx |

### Streaming node logs

```python
async for line in ix.nodes.node_logs(node_id=1):
    print(line)
```

### Bring your own `httpx.AsyncClient`

```python
import httpx

client = httpx.AsyncClient(proxy="socks5://127.0.0.1:1080")
ix = IXRayClient("https://panel.example.com", api_key="ix_key_...", http_client=client)
```

## More examples

See [docs/examples.md](docs/examples.md): create a user from a template, reset
usage, revoke a subscription, read traffic per node, take a backup, manage
groups and hosts.

## Regenerating from a newer panel

The models and resource classes are generated from `spec/openapi.json`:

```bash
make spec PANEL=http://127.0.0.1:8000   # panel must run with DOCS=1
make generate
make test
```

## License

MIT
