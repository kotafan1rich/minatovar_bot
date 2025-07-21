import re

from src.admin.dal import SettingsDAL
from src.client.dal import ReferralDAL
from src.orders.dal import OrderDAL
from src.orders.models import OrderTypeItem



def is_valid_link(link: str) -> bool:
    pattern = r"^https://dw4\.co/t/A/[a-zA-Z0-9]+$"
    return bool(re.match(pattern, link))


async def get_active_referrals(user_id: int, user_referrals, db_session) -> int:
    order_dal = OrderDAL(db_session)
    k = 0
    for id_ref in user_referrals:
        summ = sum(await order_dal.get_completed_orders_for_user(user_id=id_ref))
        if summ >= 4000:
            k += 1
    return k


async def calculate_rub_price(
    user_id: int, price_cny: int, type_item: OrderTypeItem, db_session
) -> int:
    settings_dal = SettingsDAL(db_session)
    referral_dal = ReferralDAL(db_session)

    current_rate: float = await settings_dal.get_param("current_rate")
    deliver_price = (
        await settings_dal.get_param("shoes_price")
        if type_item == OrderTypeItem.SHOES.value
        else await settings_dal.get_param("cloth_price")
    )
    price_rub = price_cny * current_rate + deliver_price

    if price_rub < 50000:
        user_referrals: list = await referral_dal.get_refferals(id_from=user_id)
        active_referrals = await get_active_referrals(
            user_id, user_referrals, db_session
        )

        if active_referrals:
            if price_rub < 10000:
                active_referrals = min(active_referrals, 5)
                price_rub *= 1 - active_referrals * 0.1

            elif price_rub < 20000:
                active_referrals = min(active_referrals, 3)
                price_rub *= 1 - active_referrals * 0.1

            else:
                active_referrals = min(active_referrals, 4)
                price_rub *= 1 - active_referrals * 0.05
    return round(price_rub)
