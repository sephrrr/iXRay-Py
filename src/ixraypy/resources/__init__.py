"""Resource classes, one per API tag."""

from ixraypy.resources.admin import AdminResource
from ixraypy.resources.admin_roles import AdminRolesResource
from ixraypy.resources.api_keys import ApiKeysResource
from ixraypy.resources.backups import BackupsResource
from ixraypy.resources.client_templates import ClientTemplatesResource
from ixraypy.resources.cores import CoresResource
from ixraypy.resources.groups import GroupsResource
from ixraypy.resources.hosts import HostsResource
from ixraypy.resources.hwids import HwidsResource
from ixraypy.resources.misc import MiscResource
from ixraypy.resources.nodes import NodesResource
from ixraypy.resources.settings import SettingsResource
from ixraypy.resources.setup import SetupResource
from ixraypy.resources.subscription import SubscriptionResource
from ixraypy.resources.system import SystemResource
from ixraypy.resources.user_templates import UserTemplatesResource
from ixraypy.resources.users import UsersResource

__all__ = [
    "AdminResource",
    "AdminRolesResource",
    "ApiKeysResource",
    "BackupsResource",
    "ClientTemplatesResource",
    "CoresResource",
    "GroupsResource",
    "HostsResource",
    "HwidsResource",
    "MiscResource",
    "NodesResource",
    "SettingsResource",
    "SetupResource",
    "SubscriptionResource",
    "SystemResource",
    "UserTemplatesResource",
    "UsersResource",
]
