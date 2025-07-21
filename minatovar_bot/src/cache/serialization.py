import pickle
from typing import Any


class AbstractSerializer:
    def serialize(self, data: Any) -> bytes:
        raise NotImplementedError

    def deserialize(self, data: bytes) -> Any:
        raise NotImplementedError


class PickleSerializer(AbstractSerializer):
    def serialize(self, data: Any) -> bytes:
        return pickle.dumps(data)

    def deserialize(self, data: bytes) -> Any:
        return pickle.loads(data)
