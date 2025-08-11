from src.admin.dal import SettingsDAL
from src.client.dal import ReferralDAL
from src.client.utils import get_active_referrals
from src.orders.models import OrderTypeItem


async def calculate_rub_price(
    user_id: int, price_cny: int, type_item: OrderTypeItem, db_session
) -> int:
    settings_dal = SettingsDAL(db_session)
    referral_dal = ReferralDAL(db_session)

    current_rate: float = await settings_dal.get_param("current_rate")
    deliver_price = (
        await settings_dal.get_param("shoes_price")
        if type_item == OrderTypeItem.SHOES.display()
        else await settings_dal.get_param("cloth_price")
    )
    price_rub = price_cny * current_rate + deliver_price

    if price_rub < 50000:
        user_referrals: list = await referral_dal.get_refferals(id_from=user_id)
        active_referrals = await get_active_referrals(user_referrals, db_session)

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
