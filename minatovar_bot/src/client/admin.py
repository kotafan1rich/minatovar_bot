from src.client.models import User
from src.db.admin import AdminBase


class UserAdmin(AdminBase):
    model = User

    fields = [
        model.id,
        model.username,
        model.user_id,
        model.time_created,
        model.time_updated,
    ]
