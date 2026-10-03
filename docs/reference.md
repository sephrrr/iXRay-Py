# API reference

Every method is `async`. Names follow the panel's OpenAPI operation ids, so the
Swagger page of your panel (`/docs` when `DOCS=1`) and this list line up one to one.

Methods that take a `body` accept either the pydantic model from `ixraypy.models`
or a plain `dict` with the same fields. Query parameters are keyword-only.

| Client attribute | Class | Methods |
|---|---|---|
| `ix.admin` | `AdminResource` | 38 |
| `ix.admin_roles` | `AdminRolesResource` | 6 |
| `ix.api_keys` | `ApiKeysResource` | 7 |
| `ix.backups` | `BackupsResource` | 5 |
| `ix.client_templates` | `ClientTemplatesResource` | 7 |
| `ix.cores` | `CoresResource` | 10 |
| `ix.groups` | `GroupsResource` | 11 |
| `ix.hosts` | `HostsResource` | 9 |
| `ix.hwids` | `HwidsResource` | 3 |
| `ix.misc` | `MiscResource` | 2 |
| `ix.nodes` | `NodesResource` | 42 |
| `ix.push` | `PushResource` | 2 |
| `ix.settings` | `SettingsResource` | 4 |
| `ix.setup` | `SetupResource` | 5 |
| `ix.subscription` | `SubscriptionResource` | 7 |
| `ix.system` | `SystemResource` | 7 |
| `ix.user_templates` | `UserTemplatesResource` | 9 |
| `ix.users` | `UsersResource` | 61 |

## `ix.admin` — AdminResource

### `activate_all_disabled_users(username: 'str') -> 'Any'`

`POST /api/admin/{username}/users/activate` — Activate All Disabled Users

### `activate_all_disabled_users_by_id(admin_id: 'int') -> 'Any'`

`POST /api/admin/by-id/{admin_id}/users/activate` — Activate All Disabled Users By Id

### `activate_all_disabled_users_by_username(username: 'str') -> 'Any'`

`POST /api/admin/by-username/{username}/users/activate` — Activate All Disabled Users By Username

### `admin_mini_app_token(*, x_telegram_authorization: 'str') -> 'Any'`

`POST /api/admin/miniapp/token` — Admin Mini App Token

### `admin_token(*, username: 'str', password: 'str', otp: 'str | None' = None, grant_type: 'str | None' = None, scope: 'str | None' = None, client_id: 'str | None' = None, client_secret: 'str | None' = None) -> 'models.Token'`

`POST /api/admin/token` — Admin Token

### `bulk_activate_all_disabled_users(*, body: 'models.BulkAdminSelection | dict[str, Any]') -> 'models.BulkAdminsActionResponse'`

`POST /api/admins/bulk/users/activate` — Bulk Activate All Disabled Users

### `bulk_delete_admins(*, body: 'models.BulkAdminSelection | dict[str, Any]') -> 'models.RemoveAdminsResponse'`

`POST /api/admins/bulk/delete` — Bulk Delete Admins

### `bulk_disable_admins(*, body: 'models.BulkAdminSelection | dict[str, Any]') -> 'models.BulkAdminsActionResponse'`

`POST /api/admins/bulk/disable` — Bulk Disable Admins

### `bulk_disable_all_active_users(*, body: 'models.BulkAdminSelection | dict[str, Any]') -> 'models.BulkAdminsActionResponse'`

`POST /api/admins/bulk/users/disable` — Bulk Disable All Active Users

### `bulk_enable_admins(*, body: 'models.BulkAdminSelection | dict[str, Any]') -> 'models.BulkAdminsActionResponse'`

`POST /api/admins/bulk/enable` — Bulk Enable Admins

### `bulk_remove_all_users(*, body: 'models.BulkAdminSelection | dict[str, Any]') -> 'models.BulkAdminsActionResponse'`

`DELETE /api/admins/bulk/users` — Bulk Remove All Users

### `bulk_reset_admins_usage(*, body: 'models.BulkAdminSelection | dict[str, Any]') -> 'models.BulkAdminsActionResponse'`

`POST /api/admins/bulk/reset` — Bulk Reset Admins Usage

### `create_admin(*, body: 'models.AdminCreate | dict[str, Any]') -> 'models.AdminDetails'`

`POST /api/admin` — Create Admin

### `disable_all_active_users(username: 'str') -> 'Any'`

`POST /api/admin/{username}/users/disable` — Disable All Active Users

### `disable_all_active_users_by_id(admin_id: 'int') -> 'Any'`

`POST /api/admin/by-id/{admin_id}/users/disable` — Disable All Active Users By Id

### `disable_all_active_users_by_username(username: 'str') -> 'Any'`

`POST /api/admin/by-username/{username}/users/disable` — Disable All Active Users By Username

### `get_admin_usage(username: 'str', *, period: 'models.Period | None' = None, node_id: 'int | None' = None, group_by_node: 'bool | None' = None, start: 'datetime | None' = None, end: 'datetime | None' = None) -> 'models.UserUsageStatsList'`

`GET /api/admin/{username}/usage` — Get Admin Usage

### `get_admin_usage_by_id(admin_id: 'int', *, period: 'models.Period | None' = None, node_id: 'int | None' = None, group_by_node: 'bool | None' = None, start: 'datetime | None' = None, end: 'datetime | None' = None) -> 'models.UserUsageStatsList'`

`GET /api/admin/by-id/{admin_id}/usage` — Get Admin Usage By Id

### `get_admin_usage_by_username(username: 'str', *, period: 'models.Period | None' = None, node_id: 'int | None' = None, group_by_node: 'bool | None' = None, start: 'datetime | None' = None, end: 'datetime | None' = None) -> 'models.UserUsageStatsList'`

`GET /api/admin/by-username/{username}/usage` — Get Admin Usage By Username

### `get_admins(*, ids: 'list[int] | None' = None, usernames: 'list[str] | None' = None, username: 'str | None' = None, offset: 'int | None' = None, limit: 'int | None' = None, sort: 'str | None' = None) -> 'models.AdminsResponse'`

`GET /api/admins` — Get Admins

### `get_admins_simple(*, ids: 'list[int] | None' = None, usernames: 'list[str] | None' = None, search: 'str | None' = None, offset: 'int | None' = None, limit: 'int | None' = None, sort: 'str | None' = None, all: 'bool | None' = None) -> 'models.AdminsSimpleResponse'`

`GET /api/admins/simple` — Get lightweight admin list

### `get_current_admin() -> 'models.AdminDetails'`

`GET /api/admin` — Get Current Admin

### `modify_admin(username: 'str', *, body: 'models.AdminModify | dict[str, Any]') -> 'models.AdminDetails'`

`PUT /api/admin/{username}` — Modify Admin

### `modify_admin_by_id(admin_id: 'int', *, body: 'models.AdminModify | dict[str, Any]') -> 'models.AdminDetails'`

`PUT /api/admin/by-id/{admin_id}` — Modify Admin By Id

### `modify_admin_by_username(username: 'str', *, body: 'models.AdminModify | dict[str, Any]') -> 'models.AdminDetails'`

`PUT /api/admin/by-username/{username}` — Modify Admin By Username

### `remove_admin(username: 'str') -> 'None'`

`DELETE /api/admin/{username}` — Remove Admin

### `remove_admin_by_id(admin_id: 'int') -> 'None'`

`DELETE /api/admin/by-id/{admin_id}` — Remove Admin By Id

### `remove_admin_by_username(username: 'str') -> 'None'`

`DELETE /api/admin/by-username/{username}` — Remove Admin By Username

### `remove_all_users(username: 'str') -> 'Any'`

`DELETE /api/admin/{username}/users` — Remove All Users

### `remove_all_users_by_id(admin_id: 'int') -> 'Any'`

`DELETE /api/admin/by-id/{admin_id}/users` — Remove All Users By Id

### `remove_all_users_by_username(username: 'str') -> 'Any'`

`DELETE /api/admin/by-username/{username}/users` — Remove All Users By Username

### `reset_admin_usage(username: 'str') -> 'models.AdminDetails'`

`POST /api/admin/{username}/reset` — Reset Admin Usage

### `reset_admin_usage_by_id(admin_id: 'int') -> 'models.AdminDetails'`

`POST /api/admin/by-id/{admin_id}/reset` — Reset Admin Usage By Id

### `reset_admin_usage_by_username(username: 'str') -> 'models.AdminDetails'`

`POST /api/admin/by-username/{username}/reset` — Reset Admin Usage By Username

### `totp_disable(*, body: 'models.TotpCode | dict[str, Any]') -> 'None'`

`POST /api/admin/totp/disable` — Totp Disable

### `totp_enable(*, body: 'models.TotpCode | dict[str, Any]') -> 'None'`

`POST /api/admin/totp/enable` — Totp Enable

### `totp_reset(username: 'str') -> 'None'`

`DELETE /api/admin/{username}/totp` — Totp Reset

### `totp_setup() -> 'models.TotpSetup'`

`POST /api/admin/totp/setup` — Totp Setup

## `ix.admin_roles` — AdminRolesResource

### `create_role(*, body: 'models.AdminRoleCreate | dict[str, Any]') -> 'models.AdminRoleResponse'`

`POST /api/admin-role` — Create Role

### `delete_role(role_id: 'int') -> 'None'`

`DELETE /api/admin-role/{role_id}` — Delete Role

### `get_role(role_id: 'int') -> 'models.AdminRoleResponse'`

`GET /api/admin-role/{role_id}` — Get Role

### `get_roles(*, search: 'str | None' = None, offset: 'int | None' = None, limit: 'int | None' = None, sort: 'str | None' = None) -> 'models.AdminRolesResponse'`

`GET /api/admin-roles` — Get Roles

### `get_roles_simple() -> 'models.AdminRolesSimpleResponse'`

`GET /api/admin-roles/simple` — Get Roles Simple

### `modify_role(role_id: 'int', *, body: 'models.AdminRoleModify | dict[str, Any]') -> 'models.AdminRoleResponse'`

`PUT /api/admin-role/{role_id}` — Modify Role

## `ix.api_keys` — ApiKeysResource

### `bulk_delete_api_keys(*, body: 'models.BulkAPIKeySelection | dict[str, Any]') -> 'models.RemoveAPIKeysResponse'`

`POST /api/api_keys/bulk/delete` — Bulk Delete Api Keys

### `create_api_key(*, body: 'models.APIKeyCreate | dict[str, Any]') -> 'models.APIKeyCreateResponse'`

`POST /api/api_key` — Create Api Key

### `get_api_key(key_id: 'int') -> 'models.APIKeyResponse'`

`GET /api/api_key/{key_id}` — Get Api Key

### `list_api_keys(*, offset: 'int | None' = None, limit: 'int | None' = None, key_id: 'int | None' = None, name: 'str | None' = None, status: 'models.APIKeyStatus | None' = None) -> 'models.APIKeysResponse'`

`GET /api/api_keys` — List Api Keys

### `modify_api_key(key_id: 'int', *, body: 'models.APIKeyUpdate | dict[str, Any]') -> 'models.APIKeyResponse'`

`PATCH /api/api_key/{key_id}` — Modify Api Key

### `remove_api_key(key_id: 'int') -> 'None'`

`DELETE /api/api_key/{key_id}` — Remove Api Key

### `revoke_api_key(key_id: 'int') -> 'models.APIKeyCreateResponse'`

`POST /api/api_key/{key_id}/revoke` — Revoke Api Key

## `ix.backups` — BackupsResource

### `create_backup_now() -> 'models.BackupInfo'`

`POST /api/backups` — Create Backup Now

### `download_backup(name: 'str') -> 'bytes'`

`GET /api/backups/{name}/download` — Download Backup

### `get_backups() -> 'models.BackupList'`

`GET /api/backups` — Get Backups

### `remove_backup(name: 'str') -> 'None'`

`DELETE /api/backups/{name}` — Remove Backup

### `send_backup_telegram(name: 'str') -> 'None'`

`POST /api/backups/{name}/telegram` — Send Backup Telegram

## `ix.client_templates` — ClientTemplatesResource

### `bulk_delete_client_templates(*, body: 'models.BulkClientTemplateSelection | dict[str, Any]') -> 'models.RemoveClientTemplatesResponse'`

`POST /api/client_templates/bulk/delete` — Bulk Delete Client Templates

### `create_client_template(*, body: 'models.ClientTemplateCreate | dict[str, Any]') -> 'models.ClientTemplateResponse'`

`POST /api/client_template` — Create Client Template

### `get_client_template(template_id: 'int') -> 'models.ClientTemplateResponse'`

`GET /api/client_template/{template_id}` — Get Client Template

### `get_client_templates(*, ids: 'list[int] | None' = None, template_type: 'models.ClientTemplateType | None' = None, offset: 'int | None' = None, limit: 'int | None' = None) -> 'models.ClientTemplateResponseList'`

`GET /api/client_templates` — Get Client Templates

### `get_client_templates_simple(*, ids: 'list[int] | None' = None, template_type: 'models.ClientTemplateType | None' = None, offset: 'int | None' = None, limit: 'int | None' = None, search: 'str | None' = None, sort: 'str | None' = None, all: 'bool | None' = None) -> 'models.ClientTemplatesSimpleResponse'`

`GET /api/client_templates/simple` — Get Client Templates Simple

### `modify_client_template(template_id: 'int', *, body: 'models.ClientTemplateModify | dict[str, Any]') -> 'models.ClientTemplateResponse'`

`PUT /api/client_template/{template_id}` — Modify Client Template

### `remove_client_template(template_id: 'int') -> 'None'`

`DELETE /api/client_template/{template_id}` — Remove Client Template

## `ix.cores` — CoresResource

### `bulk_delete_cores(*, body: 'models.BulkCoreSelection | dict[str, Any]') -> 'models.RemoveCoresResponse'`

`POST /api/cores/bulk/delete` — Bulk Delete Cores

### `create_core_config(*, body: 'models.CoreCreate | dict[str, Any]') -> 'models.CoreResponse'`

`POST /api/core` — Create Core Config

### `delete_core_config(core_id: 'int', *, restart_nodes: 'bool | None' = None) -> 'None'`

`DELETE /api/core/{core_id}` — Delete Core Config

### `get_all_cores(*, ids: 'list[int] | None' = None, offset: 'int | None' = None, limit: 'int | None' = None) -> 'models.CoreResponseList'`

`GET /api/cores` — Get All Cores

### `get_core_config(core_id: 'int') -> 'models.CoreResponse'`

`GET /api/core/{core_id}` — Get Core Config

### `get_core_outbound_stats(core_id: 'int', *, start: 'str | None' = None, end: 'str | None' = None, period: 'models.Period | None' = None) -> 'models.CoreOutboundStats'`

`GET /api/core/{core_id}/outbounds/stats` — Get Core Outbound Stats

### `get_cores_simple(*, ids: 'list[int] | None' = None, offset: 'int | None' = None, limit: 'int | None' = None, search: 'str | None' = None, sort: 'str | None' = None, all: 'bool | None' = None) -> 'models.CoresSimpleResponse'`

`GET /api/cores/simple` — Get lightweight core list

### `modify_core_config(core_id: 'int', *, body: 'models.CoreCreate | dict[str, Any]', restart_nodes: 'bool') -> 'models.CoreResponse'`

`PUT /api/core/{core_id}` — Modify Core Config

### `restart_core(core_id: 'int') -> 'None'`

`POST /api/core/{core_id}/restart` — Restart Core

### `scan_reality_target(*, body: 'models.RealityScanRequest | dict[str, Any]') -> 'models.RealityScanResult'`

`POST /api/core/reality-scan` — Scan Reality Target

## `ix.groups` — GroupsResource

### `bulk_add_groups_to_users(*, body: 'models.BulkGroup | dict[str, Any]') -> 'Any'`

`POST /api/groups/bulk/add` — Bulk add groups to users

### `bulk_delete_groups(*, body: 'models.BulkGroupSelection | dict[str, Any]') -> 'models.RemoveGroupsResponse'`

`POST /api/groups/bulk/delete` — Bulk Delete Groups

### `bulk_disable_groups(*, body: 'models.BulkGroupSelection | dict[str, Any]') -> 'models.BulkGroupsActionResponse'`

`POST /api/groups/bulk/disable` — Bulk Disable Groups

### `bulk_enable_groups(*, body: 'models.BulkGroupSelection | dict[str, Any]') -> 'models.BulkGroupsActionResponse'`

`POST /api/groups/bulk/enable` — Bulk Enable Groups

### `bulk_remove_users_from_groups(*, body: 'models.BulkGroup | dict[str, Any]') -> 'Any'`

`POST /api/groups/bulk/remove` — Bulk remove groups from users

### `create_group(*, body: 'models.GroupCreate | dict[str, Any]') -> 'models.GroupResponse'`

`POST /api/group` — Create a new group

### `get_all_groups(*, ids: 'list[int] | None' = None, offset: 'int | None' = None, limit: 'int | None' = None) -> 'models.GroupsResponse'`

`GET /api/groups` — List all groups

### `get_group(group_id: 'int') -> 'models.GroupResponse'`

`GET /api/group/{group_id}` — Get group details

### `get_groups_simple(*, ids: 'list[int] | None' = None, offset: 'int | None' = None, limit: 'int | None' = None, search: 'str | None' = None, sort: 'str | None' = None, all: 'bool | None' = None) -> 'models.GroupsSimpleResponse'`

`GET /api/groups/simple` — Get lightweight group list

### `modify_group(group_id: 'int', *, body: 'models.GroupModify | dict[str, Any]') -> 'models.GroupResponse'`

`PUT /api/group/{group_id}` — Modify group

### `remove_group(group_id: 'int') -> 'None'`

`DELETE /api/group/{group_id}` — Remove group

## `ix.hosts` — HostsResource

### `bulk_delete_hosts(*, body: 'models.BulkHostSelection | dict[str, Any]') -> 'models.RemoveHostsResponse'`

`POST /api/hosts/bulk/delete` — Bulk Delete Hosts

### `bulk_disable_hosts(*, body: 'models.BulkHostSelection | dict[str, Any]') -> 'models.BulkHostsActionResponse'`

`POST /api/hosts/bulk/disable` — Bulk Disable Hosts

### `bulk_enable_hosts(*, body: 'models.BulkHostSelection | dict[str, Any]') -> 'models.BulkHostsActionResponse'`

`POST /api/hosts/bulk/enable` — Bulk Enable Hosts

### `create_host(*, body: 'models.CreateHost | dict[str, Any]') -> 'models.BaseHost'`

`POST /api/host/` — Create Host

### `get_host(host_id: 'int') -> 'models.BaseHost'`

`GET /api/host/{host_id}` — Get Host

### `get_hosts(*, ids: 'list[int] | None' = None, offset: 'int | None' = None, limit: 'int | None' = None) -> 'list[models.BaseHost]'`

`GET /api/hosts` — Get Hosts

### `modify_host(host_id: 'int', *, body: 'models.CreateHost | dict[str, Any]') -> 'models.BaseHost'`

`PUT /api/host/{host_id}` — Modify Host

### `modify_hosts(*, body: 'list[models.CreateHost]') -> 'list[models.BaseHost]'`

`PUT /api/hosts` — Modify Hosts

### `remove_host(host_id: 'int') -> 'None'`

`DELETE /api/host/{host_id}` — Remove Host

## `ix.hwids` — HwidsResource

### `delete_user_hwid(user_id: 'int', hwid: 'str') -> 'Any'`

`DELETE /api/user/{user_id}/hwids/{hwid}` — Delete User Hwid

### `get_user_hwids(user_id: 'int') -> 'models.UserHWIDListResponse'`

`GET /api/user/{user_id}/hwids` — Get User Hwids

### `reset_user_hwids(user_id: 'int') -> 'Any'`

`POST /api/user/{user_id}/hwids/reset` — Reset User Hwids

## `ix.misc` — MiscResource

### `base() -> 'str'`

`GET /` — Base

### `health() -> 'dict[str, Any]'`

`GET /health` — Health

## `ix.nodes` — NodesResource

### `bulk_delete_nodes(*, body: 'models.BulkNodeSelection | dict[str, Any]') -> 'models.RemoveNodesResponse'`

`POST /api/nodes/bulk/delete` — Bulk Delete Nodes

### `bulk_disable_nodes(*, body: 'models.BulkNodeSelection | dict[str, Any]') -> 'models.BulkNodesActionResponse'`

`POST /api/nodes/bulk/disable` — Bulk Disable Nodes

### `bulk_enable_nodes(*, body: 'models.BulkNodeSelection | dict[str, Any]') -> 'models.BulkNodesActionResponse'`

`POST /api/nodes/bulk/enable` — Bulk Enable Nodes

### `bulk_reconnect_nodes(*, body: 'models.BulkNodeSelection | dict[str, Any]') -> 'models.BulkNodesActionResponse'`

`POST /api/nodes/bulk/reconnect` — Bulk Reconnect Nodes

### `bulk_reset_nodes_usage(*, body: 'models.BulkNodeSelection | dict[str, Any]') -> 'models.BulkNodesActionResponse'`

`POST /api/nodes/bulk/reset` — Bulk Reset Nodes Usage

### `bulk_update_nodes(*, body: 'models.BulkNodeSelection | dict[str, Any]') -> 'models.BulkNodesActionResponse'`

`POST /api/nodes/bulk/update` — Bulk Update Nodes

### `clear_usage_data(table: 'models.UsageTable | str', *, start: 'datetime | None' = None, end: 'datetime | None' = None) -> 'Any'`

`DELETE /api/nodes/clear_usage_data/{table}` — Clear usage data from a specified table

### `create_install(*, body: 'models.InstallCreate | dict[str, Any]') -> 'models.InstallResponse'`

`POST /api/node/install` — Create Install

### `create_node(*, body: 'models.NodeCreate | dict[str, Any]') -> 'models.NodeResponse'`

`POST /api/node` — Create Node

### `get_core_releases(*, core: 'str') -> 'models.CoreReleasesResponse'`

`GET /api/node/core_releases` — Get Core Releases

### `get_install(install_id: 'int') -> 'models.InstallResponse'`

`GET /api/node/install/{install_id}` — Get Install

### `get_node(node_id: 'int') -> 'models.NodeResponse'`

`GET /api/node/{node_id}` — Get Node

### `get_node_settings() -> 'models.NodeSettings'`

`GET /api/node/settings` — Get Node Settings

### `get_node_stats_periodic(node_id: 'int', *, period: 'models.Period | None' = None, start: 'datetime | None' = None, end: 'datetime | None' = None) -> 'models.NodeStatsList'`

`GET /api/node/{node_id}/stats` — Get Node Stats Periodic

### `get_nodes(*, core_id: 'int | None' = None, offset: 'int | None' = None, limit: 'int | None' = None, ids: 'list[int] | None' = None, status: 'models.NodeStatus | list[models.NodeStatus] | None' = None, enabled: 'bool | None' = None, search: 'str | None' = None) -> 'models.NodesResponse'`

`GET /api/nodes` — Get Nodes

### `get_nodes_simple(*, ids: 'list[int] | None' = None, offset: 'int | None' = None, limit: 'int | None' = None, search: 'str | None' = None, sort: 'str | None' = None, all: 'bool | None' = None) -> 'models.NodesSimpleResponse'`

`GET /api/nodes/simple` — Get lightweight node list

### `get_usage(*, period: 'models.Period | None' = None, node_id: 'int | None' = None, group_by_node: 'bool | None' = None, start: 'datetime | None' = None, end: 'datetime | None' = None) -> 'models.NodeUsageStatsList'`

`GET /api/node/usage` — Get Usage

### `get_user_count_metric(metric: 'models.UserCountMetric | str', *, period: 'models.Period | None' = None, node_id: 'int | None' = None, group_by_node: 'bool | None' = None, start: 'datetime | None' = None, end: 'datetime | None' = None) -> 'models.UserCountMetricStatsList'`

`GET /api/node/user_counts/{metric}` — Get User Count Metric

### `modify_node(node_id: 'int', *, body: 'models.NodeModify | dict[str, Any]') -> 'models.NodeResponse'`

`PUT /api/node/{node_id}` — Modify Node

### `node_add_routing_rule(node_id: 'int', *, body: 'models.LiveRoutingRuleAdd | dict[str, Any]') -> 'None'`

`POST /api/node/{node_id}/routing/rules` — Node Add Routing Rule

### `node_balancer_info(node_id: 'int', tag: 'str') -> 'models.BalancerInfo'`

`GET /api/node/{node_id}/routing/balancer/{tag}` — Node Balancer Info

### `node_outbounds_latency(node_id: 'int', *, name: 'str | None' = None, timeout: 'int | None' = None, fresh: 'bool | None' = None) -> 'models.NodeOutboundsLatencyResponse'`

`GET /api/node/{node_id}/outbounds_latency` — Node Outbounds Latency

### `node_override_balancer(node_id: 'int', tag: 'str', *, body: 'models.BalancerOverride | dict[str, Any]') -> 'None'`

`PUT /api/node/{node_id}/routing/balancer/{tag}` — Node Override Balancer

### `node_remove_routing_rule(node_id: 'int', rule_tag: 'str') -> 'None'`

`DELETE /api/node/{node_id}/routing/rules/{rule_tag}` — Node Remove Routing Rule

### `node_routing_rules(node_id: 'int') -> 'models.LiveRoutingRules'`

`GET /api/node/{node_id}/routing/rules` — Node Routing Rules

### `node_test_route(node_id: 'int', *, body: 'models.RouteTestRequest | dict[str, Any]') -> 'models.RouteTestResult'`

`POST /api/node/{node_id}/routing/test` — Node Test Route

### `nodes_latency() -> 'models.ServerLatencyList'`

`GET /api/nodes/latency` — Nodes Latency

### `nodes_online_counts() -> 'models.NodesOnlineCounts'`

`GET /api/nodes/online_counts` — Nodes Online Counts

### `realtime_node_stats(node_id: 'int') -> 'models.NodeRealtimeStats'`

`GET /api/node/{node_id}/realtime_stats` — Realtime Node Stats

### `realtime_nodes_stats() -> 'dict[str, Any]'`

`GET /api/nodes/realtime_stats` — Realtime Nodes Stats

### `reconnect_all_node(*, core_id: 'int | None' = None) -> 'Any'`

`POST /api/nodes/reconnect` — Reconnect All Node

### `reconnect_node(node_id: 'int') -> 'Any'`

`POST /api/node/{node_id}/reconnect` — Reconnect Node

### `refresh_nodes_latency() -> 'models.ServerLatencyList'`

`POST /api/nodes/latency/refresh` — Refresh Nodes Latency

### `remove_node(node_id: 'int') -> 'None'`

`DELETE /api/node/{node_id}` — Remove Node

### `reset_node_usage(node_id: 'int') -> 'models.NodeResponse'`

`POST /api/node/{node_id}/reset` — Reset Node Usage

### `sync_node(node_id: 'int', *, flush_users: 'bool | None' = None) -> 'Any'`

`PUT /api/node/{node_id}/sync` — Sync Node

### `update_core(node_id: 'int', *, body: 'models.NodeCoreUpdate | dict[str, Any]') -> 'Any'`

`POST /api/node/{node_id}/core_update` — Update Core

### `update_geofiles(node_id: 'int', *, body: 'models.NodeGeoFilesUpdate | dict[str, Any]') -> 'Any'`

`POST /api/node/{node_id}/geofiles` — Update Geofiles

### `update_node(node_id: 'int') -> 'Any'`

`POST /api/node/{node_id}/update` — Update Node

### `user_online_ip_list(node_id: 'int', user_id: 'int') -> 'models.UserIPList'`

`GET /api/node/{node_id}/online_stats/{user_id}/ip` — User Online Ip List

### `user_online_ip_list_all_nodes(user_id: 'int') -> 'models.UserIPListAll'`

`GET /api/node/online_stats/{user_id}/ip` — User Online Ip List All Nodes

### `user_online_stats(node_id: 'int', user_id: 'int') -> 'dict[str, Any]'`

`GET /api/node/{node_id}/online_stats/{user_id}` — User Online Stats

## `ix.push` — PushResource

### `push_send(*, body: 'models.PushSend | dict[str, Any]') -> 'models.PushResult'`

`POST /api/push/send` — Push Send

### `push_subscribers() -> 'models.PushSubscribers'`

`GET /api/push/subscribers` — Push Subscribers

## `ix.settings` — SettingsResource

### `get_general_settings() -> 'models.General'`

`GET /api/settings/general` — Get General Settings

### `get_settings() -> 'models.SettingsSchema'`

`GET /api/settings` — Get Settings

### `get_timezone() -> 'dict[str, Any]'`

`GET /api/settings/timezone` — Get Timezone

### `modify_settings(*, body: 'models.SettingsSchema | dict[str, Any]') -> 'models.SettingsSchema'`

`PUT /api/settings` — Modify Settings

## `ix.setup` — SetupResource

### `create_owner(*, body: 'models.OwnerCreateRequest | dict[str, Any]') -> 'models.AdminDetails'`

`POST /api/setup/owner` — Create Owner

### `delete_owner(*, key: 'str') -> 'None'`

`DELETE /api/setup/owner` — Delete Owner

### `reset_owner_password(*, body: 'models.OwnerResetRequest | dict[str, Any]') -> 'models.AdminDetails'`

`PATCH /api/setup/owner` — Reset Owner Password

### `setup_status() -> 'dict[str, Any]'`

`GET /api/setup/status` — Setup Status

### `upgrade_owner(*, body: 'models.OwnerUpgradeRequest | dict[str, Any]') -> 'models.AdminDetails'`

`POST /api/setup/owner/upgrade` — Upgrade Owner

## `ix.subscription` — SubscriptionResource

### `get_sub_user_usage(token: 'str', *, period: 'models.Period | None' = None, start: 'datetime | None' = None, end: 'datetime | None' = None) -> 'models.UserUsageStatsList'`

`GET /sub/{token}/usage` — Get Sub User Usage

### `user_subscription(token: 'str', *, user_agent: 'str | None' = None, x_hwid: 'str | None' = None, x_device_os: 'str | None' = None, x_ver_os: 'str | None' = None, x_device_model: 'str | None' = None) -> 'Any'`

`GET /sub/{token}/` — User Subscription

### `user_subscription_apps(token: 'str') -> 'list[models.Application]'`

`GET /sub/{token}/apps` — User Subscription Apps

### `user_subscription_headers(token: 'str', *, user_agent: 'str | None' = None) -> 'Any'`

`HEAD /sub/{token}/` — User Subscription Headers

### `user_subscription_info(token: 'str') -> 'models.SubscriptionUserResponse'`

`GET /sub/{token}/info` — User Subscription Info

### `user_subscription_raw(token: 'str') -> 'Any'`

`GET /sub/{token}/raw` — User Subscription Raw

### `user_subscription_with_client_type(token: 'str', client_type: 'models.ConfigFormat | str', *, x_hwid: 'str | None' = None, x_device_os: 'str | None' = None, x_ver_os: 'str | None' = None, x_device_model: 'str | None' = None) -> 'Any'`

`GET /sub/{token}/{client_type}` — User Subscription With Client Type

## `ix.system` — SystemResource

### `get_inbound_details() -> 'list[models.InboundSummary]'`

`GET /api/inbounds/details` — Get Inbound Details

### `get_inbounds() -> 'list[str]'`

`GET /api/inbounds` — Get Inbounds

### `get_system_resource_stats() -> 'models.SystemResourceStats'`

`GET /api/system/resources` — Get System Resource Stats

### `get_system_stats(*, admin_username: 'str | None' = None) -> 'models.SystemStats'`

`GET /api/system` — Get System Stats

### `get_system_users_stats(*, admin_username: 'str | None' = None) -> 'models.SystemUsersStats'`

`GET /api/system/users` — Get System Users Stats

### `get_wireguard_subnets() -> 'list[models.WireGuardSubnetUsage]'`

`GET /api/wireguard/subnets` — Get Wireguard Subnets

### `get_workers_health() -> 'models.WorkersHealth'`

`GET /api/workers/health` — Get Workers Health

## `ix.user_templates` — UserTemplatesResource

### `bulk_delete_user_templates(*, body: 'models.BulkUserTemplateSelection | dict[str, Any]') -> 'models.RemoveUserTemplatesResponse'`

`POST /api/user_templates/bulk/delete` — Bulk Delete User Templates

### `bulk_disable_user_templates(*, body: 'models.BulkUserTemplateSelection | dict[str, Any]') -> 'models.BulkUserTemplatesActionResponse'`

`POST /api/user_templates/bulk/disable` — Bulk Disable User Templates

### `bulk_enable_user_templates(*, body: 'models.BulkUserTemplateSelection | dict[str, Any]') -> 'models.BulkUserTemplatesActionResponse'`

`POST /api/user_templates/bulk/enable` — Bulk Enable User Templates

### `create_user_template(*, body: 'models.UserTemplateCreate | dict[str, Any]') -> 'models.UserTemplateResponse'`

`POST /api/user_template` — Create User Template

### `get_user_template(template_id: 'int') -> 'models.UserTemplateResponse'`

`GET /api/user_template/{template_id}` — Get User Template

### `get_user_templates(*, ids: 'list[int] | None' = None, offset: 'int | None' = None, limit: 'int | None' = None) -> 'list[models.UserTemplateResponse]'`

`GET /api/user_templates` — Get User Templates

### `get_user_templates_simple(*, ids: 'list[int] | None' = None, offset: 'int | None' = None, limit: 'int | None' = None, search: 'str | None' = None, sort: 'str | None' = None, all: 'bool | None' = None) -> 'models.UserTemplatesSimpleResponse'`

`GET /api/user_templates/simple` — Get lightweight user template list

### `modify_user_template(template_id: 'int', *, body: 'models.UserTemplateModify | dict[str, Any]') -> 'models.UserTemplateResponse'`

`PUT /api/user_template/{template_id}` — Modify User Template

### `remove_user_template(template_id: 'int') -> 'None'`

`DELETE /api/user_template/{template_id}` — Remove User Template

## `ix.users` — UsersResource

### `active_next_plan(username: 'str') -> 'models.UserResponse'`

`POST /api/user/{username}/active_next` — Active Next Plan

### `active_next_plan_by_id(user_id: 'int') -> 'models.UserResponse'`

`POST /api/user/by-id/{user_id}/active_next` — Active Next Plan By Id

### `active_next_plan_by_username(username: 'str') -> 'models.UserResponse'`

`POST /api/user/by-username/{username}/active_next` — Active Next Plan By Username

### `bulk_apply_template_to_users(*, body: 'models.BulkUsersApplyTemplate | dict[str, Any]') -> 'models.BulkUsersActionResponse'`

`POST /api/users/bulk/apply_template` — Bulk Apply Template To Users

### `bulk_create_users_from_template(*, body: 'models.BulkUsersFromTemplate | dict[str, Any]') -> 'models.BulkUsersCreateResponse'`

`POST /api/users/bulk/from_template` — Bulk Create Users From Template

### `bulk_delete_users(*, body: 'models.BulkUsersSelection | dict[str, Any]') -> 'models.RemoveUsersResponse'`

`POST /api/users/bulk/delete` — Bulk Delete Users

### `bulk_disable_users(*, body: 'models.BulkUsersSelection | dict[str, Any]') -> 'models.BulkUsersActionResponse'`

`POST /api/users/bulk/disable` — Bulk Disable Users

### `bulk_enable_users(*, body: 'models.BulkUsersSelection | dict[str, Any]') -> 'models.BulkUsersActionResponse'`

`POST /api/users/bulk/enable` — Bulk Enable Users

### `bulk_modify_users_datalimit(*, body: 'models.BulkUser | dict[str, Any]') -> 'Any'`

`POST /api/users/bulk/data_limit` — Bulk sum/sub to data limit of users

### `bulk_modify_users_expire(*, body: 'models.BulkUser | dict[str, Any]') -> 'Any'`

`POST /api/users/bulk/expire` — Bulk sum/sub to expire of users

### `bulk_modify_users_proxy_settings(*, body: 'models.BulkUsersProxy | dict[str, Any]') -> 'Any'`

`POST /api/users/bulk/proxy_settings` — Bulk modify users proxy settings

### `bulk_reset_users_data_usage(*, body: 'models.BulkUsersSelection | dict[str, Any]') -> 'models.BulkUsersActionResponse'`

`POST /api/users/bulk/reset` — Bulk Reset Users Data Usage

### `bulk_revoke_users_subscription(*, body: 'models.BulkUsersSelection | dict[str, Any]') -> 'models.BulkUsersActionResponse'`

`POST /api/users/bulk/revoke_sub` — Bulk Revoke Users Subscription

### `bulk_set_owner(*, body: 'models.BulkUsersSetOwner | dict[str, Any]') -> 'models.BulkUsersActionResponse'`

`PUT /api/users/bulk/set_owner` — Bulk Set Owner

### `create_user(*, body: 'models.UserCreate | dict[str, Any]') -> 'models.UserResponse'`

`POST /api/user` — Create User

### `create_user_from_template(*, body: 'models.CreateUserFromTemplate | dict[str, Any]') -> 'models.UserResponse'`

`POST /api/user/from_template` — Create User From Template

### `delete_expired_users(*, admin_username: 'str | None' = None, target: 'str | None' = None, expired_after: 'datetime | None' = None, expired_before: 'datetime | None' = None, dry_run: 'bool | None' = None) -> 'models.RemoveUsersResponse'`

`DELETE /api/users/expired` — Delete Expired Users

### `geoip_lookup(*, ips: 'str') -> 'dict[str, Any]'`

`GET /api/users/geoip` — Geoip Lookup

### `get_expired_users(*, admin_username: 'str | None' = None, target: 'str | None' = None, expired_after: 'datetime | None' = None, expired_before: 'datetime | None' = None, dry_run: 'bool | None' = None) -> 'list[str]'`

`GET /api/users/expired` — Get Expired Users

### `get_recent_user_events(*, limit: 'int | None' = None) -> 'models.RecentEventList'`

`GET /api/users/events` — Get Recent User Events

### `get_suspicious_users(*, days: 'int | None' = None) -> 'models.SuspiciousUsersList'`

`GET /api/users/suspicious` — Get Suspicious Users

### `get_top_users_usage(*, limit: 'int | None' = None, period: 'models.Period | None' = None, node_id: 'int | None' = None, group_by_node: 'bool | None' = None, start: 'datetime | None' = None, end: 'datetime | None' = None, admin: 'list[str] | None' = None) -> 'models.TopUsersUsageList'`

`GET /api/users/top_usage` — Get Top Users Usage

### `get_user(username: 'str') -> 'models.UserResponse'`

`GET /api/user/{username}` — Get User

### `get_user_by_id(user_id: 'int') -> 'models.UserResponse'`

`GET /api/user/by-id/{user_id}` — Get User By Id

### `get_user_by_username(username: 'str') -> 'models.UserResponse'`

`GET /api/user/by-username/{username}` — Get User By Username

### `get_user_events(user_id: 'int', *, limit: 'int | None' = None) -> 'models.UserEventList'`

`GET /api/user/by-id/{user_id}/events` — Get User Events

### `get_user_ips(user_id: 'int', *, days: 'int | None' = None) -> 'models.UserIpSeenList'`

`GET /api/user/by-id/{user_id}/ips` — Get User Ips

### `get_user_sub_update_list(username: 'str', *, offset: 'int | None' = None, limit: 'int | None' = None) -> 'models.UserSubscriptionUpdateList'`

`GET /api/user/{username}/sub_update` — Get User Sub Update List

### `get_user_sub_update_list_by_id(user_id: 'int', *, offset: 'int | None' = None, limit: 'int | None' = None) -> 'models.UserSubscriptionUpdateList'`

`GET /api/user/by-id/{user_id}/sub_update` — Get User Sub Update List By Id

### `get_user_sub_update_list_by_username(username: 'str', *, offset: 'int | None' = None, limit: 'int | None' = None) -> 'models.UserSubscriptionUpdateList'`

`GET /api/user/by-username/{username}/sub_update` — Get User Sub Update List By Username

### `get_user_subscription_by_id(user_id: 'int', client_type: 'models.ConfigFormat | str') -> 'Any'`

`GET /api/user/{user_id}/subscription/{client_type}` — Get User Subscription By Id

### `get_user_usage(username: 'str', *, period: 'models.Period | None' = None, node_id: 'int | None' = None, group_by_node: 'bool | None' = None, start: 'datetime | None' = None, end: 'datetime | None' = None) -> 'models.UserUsageStatsList'`

`GET /api/user/{username}/usage` — Get User Usage

### `get_user_usage_by_id(user_id: 'int', *, period: 'models.Period | None' = None, node_id: 'int | None' = None, group_by_node: 'bool | None' = None, start: 'datetime | None' = None, end: 'datetime | None' = None) -> 'models.UserUsageStatsList'`

`GET /api/user/by-id/{user_id}/usage` — Get User Usage By Id

### `get_user_usage_by_username(username: 'str', *, period: 'models.Period | None' = None, node_id: 'int | None' = None, group_by_node: 'bool | None' = None, start: 'datetime | None' = None, end: 'datetime | None' = None) -> 'models.UserUsageStatsList'`

`GET /api/user/by-username/{username}/usage` — Get User Usage By Username

### `get_users(*, offset: 'int | None' = None, limit: 'int | None' = None, ids: 'list[int] | None' = None, username: 'list[str] | None' = None, usernames: 'list[str] | None' = None, admin: 'list[str] | None' = None, admin_ids: 'list[int] | None' = None, group: 'list[int] | None' = None, no_group: 'bool | None' = None, search: 'str | None' = None, status: 'models.UserStatus | list[models.UserStatus] | None' = None, sort: 'str | None' = None, proxy_id: 'str | None' = None, data_limit_reset_strategy: 'models.DataLimitResetStrategy | list[models.DataLimitResetStrategy] | None' = None, data_limit_min: 'int | None' = None, data_limit_max: 'int | None' = None, expire_after: 'datetime | None' = None, expire_before: 'datetime | None' = None, online_after: 'datetime | None' = None, online_before: 'datetime | None' = None, online: 'bool | None' = None, no_data_limit: 'bool | None' = None, no_expire: 'bool | None' = None, load_sub: 'bool | None' = None) -> 'models.UsersResponse'`

`GET /api/users` — Get Users

### `get_users_count_metric(metric: 'models.UserCountMetric | str', *, period: 'models.Period | None' = None, node_id: 'int | None' = None, group_by_node: 'bool | None' = None, start: 'datetime | None' = None, end: 'datetime | None' = None, admin: 'list[str] | None' = None) -> 'models.UserCountMetricStatsList'`

`GET /api/users/counts/{metric}` — Get Users Count Metric

### `get_users_simple(*, ids: 'list[int] | None' = None, usernames: 'list[str] | None' = None, offset: 'int | None' = None, limit: 'int | None' = None, search: 'str | None' = None, sort: 'str | None' = None, all: 'bool | None' = None) -> 'models.UsersSimpleResponse'`

`GET /api/users/simple` — Get lightweight user list

### `get_users_sub_update_chart(*, user_id: 'int | None' = None, username: 'str | None' = None, admin_id: 'int | None' = None, period: 'models.Period | None' = None, start: 'datetime | None' = None, end: 'datetime | None' = None) -> 'models.UserSubscriptionUpdateChart'`

`GET /api/users/sub_update/chart` — Get Users Sub Update Chart

### `get_users_usage(*, period: 'models.Period | None' = None, node_id: 'int | None' = None, group_by_node: 'bool | None' = None, start: 'datetime | None' = None, end: 'datetime | None' = None, admin: 'list[str] | None' = None) -> 'models.UserUsageStatsList'`

`GET /api/users/usage` — Get Users Usage

### `modify_user(username: 'str', *, body: 'models.UserModify | dict[str, Any]') -> 'models.UserResponse'`

`PUT /api/user/{username}` — Modify User

### `modify_user_by_id(user_id: 'int', *, body: 'models.UserModify | dict[str, Any]') -> 'models.UserResponse'`

`PUT /api/user/by-id/{user_id}` — Modify User By Id

### `modify_user_by_username(username: 'str', *, body: 'models.UserModify | dict[str, Any]') -> 'models.UserResponse'`

`PUT /api/user/by-username/{username}` — Modify User By Username

### `modify_user_with_template(username: 'str', *, body: 'models.ModifyUserByTemplate | dict[str, Any]') -> 'models.UserResponse'`

`PUT /api/user/from_template/{username}` — Modify User With Template

### `modify_user_with_template_by_id(user_id: 'int', *, body: 'models.ModifyUserByTemplate | dict[str, Any]') -> 'models.UserResponse'`

`PUT /api/user/from_template/by-id/{user_id}` — Modify User With Template By Id

### `modify_user_with_template_by_username(username: 'str', *, body: 'models.ModifyUserByTemplate | dict[str, Any]') -> 'models.UserResponse'`

`PUT /api/user/from_template/by-username/{username}` — Modify User With Template By Username

### `remove_user(username: 'str') -> 'None'`

`DELETE /api/user/{username}` — Remove User

### `remove_user_by_id(user_id: 'int') -> 'None'`

`DELETE /api/user/by-id/{user_id}` — Remove User By Id

### `remove_user_by_username(username: 'str') -> 'None'`

`DELETE /api/user/by-username/{username}` — Remove User By Username

### `reset_user_data_usage(username: 'str') -> 'models.UserResponse'`

`POST /api/user/{username}/reset` — Reset User Data Usage

### `reset_user_data_usage_by_id(user_id: 'int') -> 'models.UserResponse'`

`POST /api/user/by-id/{user_id}/reset` — Reset User Data Usage By Id

### `reset_user_data_usage_by_username(username: 'str') -> 'models.UserResponse'`

`POST /api/user/by-username/{username}/reset` — Reset User Data Usage By Username

### `reset_users_data_usage() -> 'Any'`

`POST /api/users/reset` — Reset Users Data Usage

### `revoke_user_subscription(username: 'str') -> 'models.UserResponse'`

`POST /api/user/{username}/revoke_sub` — Revoke User Subscription

### `revoke_user_subscription_by_id(user_id: 'int') -> 'models.UserResponse'`

`POST /api/user/by-id/{user_id}/revoke_sub` — Revoke User Subscription By Id

### `revoke_user_subscription_by_username(username: 'str') -> 'models.UserResponse'`

`POST /api/user/by-username/{username}/revoke_sub` — Revoke User Subscription By Username

### `set_owner(username: 'str', *, admin_username: 'str') -> 'models.UserResponse'`

`PUT /api/user/{username}/set_owner` — Set Owner

### `set_owner_by_id(user_id: 'int', *, admin_username: 'str') -> 'models.UserResponse'`

`PUT /api/user/by-id/{user_id}/set_owner` — Set Owner By Id

### `set_owner_by_username(username: 'str', *, admin_username: 'str') -> 'models.UserResponse'`

`PUT /api/user/by-username/{username}/set_owner` — Set Owner By Username

### `set_user_disabled(username: 'str', *, body: 'models.UserStatusToggle | dict[str, Any]') -> 'models.UserResponse'`

`PUT /api/user/{username}/disabled` — Set User Disabled

### `set_user_disabled_by_id(user_id: 'int', *, body: 'models.UserStatusToggle | dict[str, Any]') -> 'models.UserResponse'`

`PUT /api/user/by-id/{user_id}/disabled` — Set User Disabled By Id

### `set_user_disabled_by_username(username: 'str', *, body: 'models.UserStatusToggle | dict[str, Any]') -> 'models.UserResponse'`

`PUT /api/user/by-username/{username}/disabled` — Set User Disabled By Username
