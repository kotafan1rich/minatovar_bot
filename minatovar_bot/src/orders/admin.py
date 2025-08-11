from starlette_admin.contrib.sqla import ModelView

from src.orders.models import Order, Referral


class OrderAdmin(ModelView):
    exclude_fields_from_create = [
        Order.id,
        Order.time_created,
        Order.time_updated,
    ]
    exclude_fields_from_edit = [
        Order.id,
        Order.time_created,
        Order.time_updated,
    ]

class ReferralAdmin(ModelView):
    exclude_fields_from_create = [
        Referral.id,
        Referral.time_created,
        Referral.time_updated,
    ]
    exclude_fields_from_edit = [
        Referral.id,
        Referral.time_created,
        Referral.time_updated,
    ]
