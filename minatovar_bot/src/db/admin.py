from starlette_admin.contrib.sqla import ModelView

from src.db.models import BaseModel


class AdminBase(ModelView):
    model = BaseModel

    exclude_fields_from_create = [
        "id",
        "time_created",
        "time_updated",
    ]
    exclude_fields_from_edit = [
        "id",
        "time_created",
        "time_updated",
    ]

    def get_list_query(self, request):
        return super().get_list_query(request).order_by(self.model.id.desc())
