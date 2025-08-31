from src.db.admin import AdminBase
from src.orders.models import Referral, Order


class OrderAdmin(AdminBase):
    model = Order

    fields = [
        model.id,
        model.user_id,
        model.status,
        model.article,
        model.size,
        model.addres,
        model.price_rub,
        model.price_cny,
        model.type_item,
        model.time_created,
        model.time_updated,
    ]


class ReferralAdmin(AdminBase):
    model = Referral

    fields = [
        model.id,
        model.id_from,
        model.id_to,
        model.time_created,
        model.time_updated,
    ]
