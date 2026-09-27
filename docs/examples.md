# Examples

All snippets assume:

```python
from ixraypy import IXRayClient, models

ix = IXRayClient("https://panel.example.com", api_key="ix_key_...")
```

and run inside an `async` function. Close the client with `await ix.aclose()`
or use `async with`.

## Users

```python
# Create from a user template (plan): the template decides limits and groups.
user = await ix.users.create_user_from_template(
    body=models.CreateUserFromTemplate(username="alice", user_template_id=2)
)

# Or spell everything out.
user = await ix.users.create_user(
    body=models.UserCreate(
        username="bob",
        group_ids=[1, 3],
        data_limit=100 * 1024**3,          # bytes; 0 = unlimited
        expire="2027-01-01T00:00:00+00:00",
        data_limit_reset_strategy=models.DataLimitResetStrategy.monthly,
        note="sold via bot",
    )
)
print(user.subscription_url, user.links)

# Read, modify, reset, revoke, disable, delete.
u = await ix.users.get_user("bob")
u = await ix.users.modify_user("bob", body=models.UserModify(data_limit=200 * 1024**3))
u = await ix.users.reset_user_data_usage("bob")
u = await ix.users.revoke_user_subscription("bob")
u = await ix.users.modify_user("bob", body=models.UserModify(status="disabled"))
await ix.users.remove_user("bob")

# Lists and filters (all keyword-only).
page = await ix.users.get_users(limit=50, offset=0, search="ali", status=[models.UserStatus.active])
expiring = await ix.users.get_users(expire_before="2026-10-01T00:00:00+00:00")
top = await ix.users.get_top_users_usage(limit=10)

# Usage per node over a window.
usage = await ix.users.get_user_usage("alice", start="2026-09-01T00:00:00", end="2026-09-30T23:59:59")

# Where a user connected from lately, and what happened to the account.
ips = await ix.users.get_user_ips(user.id)
events = await ix.users.get_user_events(user.id)

# Bulk operations.
await ix.users.bulk_reset_users_data_usage(body={"user_ids": [1, 2, 3]})
await ix.users.bulk_modify_users_expire(body={"amount": 30 * 86400, "user_ids": [1, 2]})
```

## Subscription content

```python
# The same content the client apps download, in a chosen format.
links = await ix.users.get_user_subscription_by_id(user.id, "links")
clash = await ix.users.get_user_subscription_by_id(user.id, models.ConfigFormat.clash)

# Public endpoint with a subscription token (no admin auth needed).
info = await ix.subscription.user_subscription_info(token)
```

## Nodes and traffic

```python
nodes = await ix.nodes.get_nodes()
live = await ix.nodes.realtime_nodes_stats()          # cpu, memory, bandwidth per node
online = await ix.nodes.nodes_online_counts()          # users online per node

await ix.nodes.reconnect_node(node_id=1)
await ix.nodes.sync_node(node_id=1, flush_users=False)

async for line in ix.nodes.node_logs(node_id=1):       # server-sent events
    print(line)

# Traffic per node in a time window.
usage = await ix.nodes.get_usage(start="2026-09-01T00:00:00", end="2026-09-30T23:59:59")

# Register a new node.
node = await ix.nodes.create_node(
    body=models.NodeCreate(
        name="fi-2", address="203.0.113.10", port=62050,
        api_key="node-api-key", server_ca="-----BEGIN CERTIFICATE-----...",
        core_config_id=1,
    )
)
```

## Cores, groups, hosts

```python
cores = await ix.cores.get_all_cores()
core = await ix.cores.get_core_config(core_id=1)
await ix.cores.restart_core(core_id=1)
stats = await ix.cores.get_core_outbound_stats(core_id=1, period="hour")

groups = await ix.groups.get_all_groups()
group = await ix.groups.create_group(body=models.GroupCreate(name="premium", inbound_tags=["vless-reality"]))

hosts = await ix.hosts.get_hosts()
await ix.hosts.create_host(body=models.CreateHost(remark="FI Reality", address=["fi.example.com"], inbound_tag="vless-reality"))
```

## Admins, roles, API keys

```python
me = await ix.admin.get_current_admin()
admins = await ix.admin.get_admins()
admin = await ix.admin.create_admin(body=models.AdminCreate(username="reseller1", password="...", role_id=2))
usage = await ix.admin.get_admin_usage("reseller1")

roles = await ix.admin_roles.get_roles()

key = await ix.api_keys.create_api_key(
    body=models.APIKeyCreate(name="billing-bot", inherit_permissions=False,
                             permissions={"users": {"create": True, "read": {"scope": 1}}})
)
print(key.api_key)   # shown once
await ix.api_keys.revoke_api_key(key.id)
```

## Settings and backups

```python
settings = await ix.settings.get_settings()
await ix.settings.modify_settings(body={"general": {"timezone": "Asia/Tehran"}})

backups = await ix.backups.get_backups()
await ix.backups.create_backup_now()
raw = await ix.backups.download_backup(backups.backups[0].name)   # bytes (pg_dump custom format)
```

## System

```python
stats = await ix.system.get_system_stats()
print(stats.online_users, stats.incoming_bandwidth_speed)
inbounds = await ix.system.get_inbounds()
```
