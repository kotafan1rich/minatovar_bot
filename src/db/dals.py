from .connection import redis_client


class RedisDAL:
    def get_shoes_price(self):
        if delivery_price := redis_client.get("shoes_price"):
            return int(delivery_price.decode())

    def get_cloth_price(self):
        if delivery_price := redis_client.get("cloth_price"):
            return int(delivery_price.decode())

    def get_current_rate(self):
        if current_rate := redis_client.get("current_rate"):
            return float(current_rate.decode())

    def set_shoes_price(self, price: int):
        redis_client.set("shoes_price", price)
        return price

    def set_cloth_price(self, price: int):
        redis_client.set("cloth_price", price)
        return price

    def set_current_rate(self, rate: float):
        redis_client.set("current_rate", rate)
        return rate
