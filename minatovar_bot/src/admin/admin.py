from starlette_admin.contrib.sqla import ModelView

from src.admin.models import Settings, Promos


class SettingsAdmin(ModelView):
    fields = [Settings.key, Settings.value, Settings.time_updated]
    exclude_fields_from_create = [
        Settings.id,
        Settings.time_created,
        Settings.time_updated,
    ]
    exclude_fields_from_edit = [
        Settings.id,
        Settings.time_created,
        Settings.time_updated,
    ]


class PromoAdmin(ModelView):
    fields = [Promos.id, Promos.descriptions, Promos.time_updated]
    exclude_fields_from_create = [
        Promos.id,
        Promos.time_created,
        Promos.time_updated,
    ]
    exclude_fields_from_edit = [
        Promos.id,
        Promos.time_created,
        Promos.time_updated,
    ]
