import httpx
import pytest
import respx

from ixraypy import IXRayClient, NotFoundError, OTPRequiredError, ValidationError, models

BASE = "https://panel.test"


@pytest.fixture
def api():
    with respx.mock(base_url=BASE, assert_all_called=False) as mock:
        yield mock


async def test_api_key_header_and_model_parsing(api):
    route = api.get("/api/system").mock(
        return_value=httpx.Response(
            200,
            json={
                "version": "0.1.0",
                "uptime_seconds": 1,
                "mem_total": 1,
                "mem_used": 1,
                "cpu_cores": 1,
                "cpu_usage": 0.5,
                "total_user": 1,
                "online_users": 0,
                "active_users": 1,
                "disabled_users": 0,
                "expired_users": 0,
                "limited_users": 0,
                "on_hold_users": 0,
                "incoming_bandwidth": 0,
                "outgoing_bandwidth": 0,
                "incoming_bandwidth_speed": 0,
                "outgoing_bandwidth_speed": 0,
            },
        )
    )
    async with IXRayClient(BASE, api_key="ix_key_x") as ix:
        stats = await ix.system.get_system_stats()
    assert route.calls.last.request.headers["X-Api-Key"] == "ix_key_x"
    assert isinstance(stats, models.SystemStats)
    assert stats.total_user == 1


async def test_password_login_then_bearer(api):
    api.post("/api/admin/token").mock(
        return_value=httpx.Response(200, json={"access_token": "T", "token_type": "bearer"})
    )
    route = api.get("/api/nodes").mock(return_value=httpx.Response(200, json={"nodes": [], "total": 0}))
    async with IXRayClient(BASE, username="a", password="b") as ix:
        res = await ix.nodes.get_nodes()
    assert route.calls.last.request.headers["Authorization"] == "Bearer T"
    assert res.total == 0
    form = api.calls[0].request.content.decode()
    assert "username=a" in form and "password=b" in form


async def test_expired_token_relogin(api):
    tokens = iter(["T1", "T2"])
    api.post("/api/admin/token").mock(
        side_effect=lambda r: httpx.Response(200, json={"access_token": next(tokens), "token_type": "bearer"})
    )
    calls = {"n": 0}

    def users(request):
        calls["n"] += 1
        if request.headers["Authorization"] == "Bearer T1":
            return httpx.Response(401, json={"detail": "Not authenticated"})
        return httpx.Response(200, json={"users": [], "total": 0})

    api.get("/api/users").mock(side_effect=users)
    async with IXRayClient(BASE, username="a", password="b") as ix:
        res = await ix.users.get_users(limit=5)
        assert res.total == 0
        assert ix.token == "T2"
    assert calls["n"] == 2


async def test_otp_required(api):
    api.post("/api/admin/token").mock(return_value=httpx.Response(401, json={"detail": "otp_required"}))
    async with IXRayClient(BASE, username="a", password="b") as ix:
        with pytest.raises(OTPRequiredError):
            await ix.login()


async def test_errors_map_to_exceptions(api):
    api.get("/api/user/nobody").mock(return_value=httpx.Response(404, json={"detail": "User not found"}))
    api.post("/api/user").mock(
        return_value=httpx.Response(422, json={"detail": [{"loc": ["body", "username"], "msg": "bad"}]})
    )
    async with IXRayClient(BASE, api_key="k") as ix:
        with pytest.raises(NotFoundError) as e:
            await ix.users.get_user("nobody")
        assert e.value.status_code == 404 and e.value.detail == "User not found"
        with pytest.raises(ValidationError):
            await ix.users.create_user(body={"username": "!"})


async def test_query_params_and_body_dump(api):
    route = api.get("/api/users").mock(return_value=httpx.Response(200, json={"users": [], "total": 0}))
    put = api.put("/api/user/alice").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": 1,
                "username": "alice",
                "status": "active",
                "data_limit": 5,
                "used_traffic": 0,
                "created_at": "2026-01-01T00:00:00Z",
                "subscription_url": "",
                "links": [],
                "proxy_settings": {},
                "group_ids": [],
                "admin": None,
                "lifetime_used_traffic": 0,
            },
        )
    )
    async with IXRayClient(BASE, api_key="k") as ix:
        await ix.users.get_users(limit=10, status=[models.UserStatus.active], username=["a", "b"])
        user = await ix.users.modify_user("alice", body=models.UserModify(data_limit=5))
    q = str(route.calls.last.request.url)
    assert "limit=10" in q and "status=active" in q and "username=a&username=b" in q
    assert put.calls.last.request.content == b'{"data_limit":5}'
    assert user.username == "alice"


async def test_delete_returns_none_and_sse_stream(api):
    api.delete("/api/user/alice").mock(return_value=httpx.Response(204))
    api.get("/api/node/1/logs").mock(return_value=httpx.Response(200, text="data: line one\n\ndata: line two\n\n"))
    async with IXRayClient(BASE, api_key="k") as ix:
        assert await ix.users.remove_user("alice") is None
        lines = [line async for line in ix.nodes.node_logs(1)]
    assert lines == ["line one", "line two"]


async def test_subscription_text_and_bytes_download(api):
    api.get("/sub/tok/").mock(
        return_value=httpx.Response(200, text="vless://...", headers={"content-type": "text/plain"})
    )
    api.get("/api/backups/b.dump/download").mock(return_value=httpx.Response(200, content=b"\x00\x01"))
    async with IXRayClient(BASE, api_key="k") as ix:
        assert await ix.subscription.user_subscription("tok", user_agent="v2rayNG") == "vless://..."
        assert await ix.backups.download_backup("b.dump") == b"\x00\x01"


def test_every_operation_is_exposed():
    import json
    from pathlib import Path

    spec = json.loads((Path(__file__).parents[1] / "spec" / "openapi.json").read_text())
    ops = {op["operationId"] for ms in spec["paths"].values() for op in ms.values()}
    ix = IXRayClient(BASE, api_key="k")
    have = {m for r in vars(ix).values() if hasattr(r, "_http") for m in dir(r) if not m.startswith("_")}
    assert ops <= have
