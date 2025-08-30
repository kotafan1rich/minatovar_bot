from src.db.admin import AdminBase
from src.orders.models import Referral, Order


class OrderAdmin(AdminBase):
    model = Order

    fields = [
        Order.id,
        Order.user_id,
        Order.status,
        Order.article,
        Order.size,
        Order.addres,
        Order.price_rub,
        Order.price_cny,
        Order.type_item,
        Order.time_created,
        Order.time_updated,
    ]


class ReferralAdmin(AdminBase):
    model = Referral

    fields = [
        Referral.id,
        Referral.id_from,
        Referral.id_to,
        Referral.time_created,
        Referral.time_updated,
    ]
