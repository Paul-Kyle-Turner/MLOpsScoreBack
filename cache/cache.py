
from datetime import datetime
from typing import Any, Dict

import json

from pydantic import BaseModel, Field, field_validator


class CacheableModel(BaseModel):
    data: Dict = Field(description="Data to be cached")
    created: datetime = Field(default_factory=datetime.now)

    def is_expired(self, expiration_seconds: int) -> bool:
        return (datetime.now() - self.created).total_seconds() > expiration_seconds

    @field_validator('data', mode='before')
    @classmethod
    def validate_data(cls, value: Dict | str) -> Dict:
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON string provided for data.")
        return value  # type: ignore


class Cache:
    def __init__(self):
        self._cache: Dict[str, CacheableModel] = {}

    def get(self, key) -> CacheableModel | None:
        cacheable_model: CacheableModel | None = self._cache.get(key)
        if cacheable_model is None:
            return None

        if cacheable_model.is_expired(3600):
            self._cache.pop(key)
            return None

        return cacheable_model

    def set(self, key, value: CacheableModel | Dict):
        if isinstance(value, CacheableModel):
            self._cache[key] = value
        elif isinstance(value, dict):
            self._cache[key] = CacheableModel(data=value)
        else:
            raise TypeError("Value must be a CacheableModel or dict.")

    def clear(self):
        self._cache.clear()
