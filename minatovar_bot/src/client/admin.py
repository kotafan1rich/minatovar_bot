from starlette_admin.contrib.sqla import ModelView

from src.client.models import User


class UserAdmin(ModelView):
    fields = [User.id, User.username, User.user_id, User.time_created, User.time_updated]
    exclude_fields_from_create = [
        User.id,
        User.time_created,
        User.time_updated,
    ]
    exclude_fields_from_edit = [
        User.id,
        User.time_created,
        User.time_updated,
    ]
