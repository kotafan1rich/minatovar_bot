from src.orders.dal import OrderDAL


async def get_active_referrals(user_referrals, db_session) -> int:
    order_dal = OrderDAL(db_session)
    k = 0
    for id_ref in user_referrals:
        summ = sum(await order_dal.get_completed_orders_for_user(user_id=id_ref))
        if summ >= 4000:
            k += 1
    return k
