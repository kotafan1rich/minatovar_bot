from src.client.models import User
from src.db.admin import AdminBase


class UserAdmin(AdminBase):
    model = User

    fields = [
        User.id,
        User.username,
        User.user_id,
        User.time_created,
        User.time_updated,
    ]
