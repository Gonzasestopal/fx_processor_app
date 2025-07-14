from typing import Type

from pydantic import BaseModel


class Memory(object):  # noqa: WPS214
    _instance = None
    _models: dict[str, Type[BaseModel]] = {}

    def __new__(cls, storage=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            if storage is None:
                storage = {
                    'currencies': [
                        {'id': 1, 'name': 'MXN'},
                        {'id': 2, 'name': 'USD'},
                    ],
                }
            cls._instance.storage = storage
        return cls._instance

    def get_table(self, table: str):
        return self.storage.setdefault(table, [])

    def find_one(self, table: str, **filters):
        table_data = self.get_table(table)
        for row in table_data:
            if all(row.get(k) == v for k, v in filters.items()):  # noqa: WPS111, WPS221
                return row
        return None

    def find(self, table: str, **filters):
        return []

    @classmethod
    def register_model(cls, table: str, model: Type[BaseModel]):
        cls._models[table] = model

    def insert(self, table: str, record: dict):
        model = self._models.get(table)

        if model is not None:
            # Check unique_together (optional)
            meta = getattr(model, "Meta", None)
            unique_fields = getattr(meta, "unique_together", [])
            if unique_fields:
                filters = {field: record[field] for field in unique_fields}
                if self.find_one(table, **filters):
                    raise ValueError(f"Record with {unique_fields} already exists")

        table_data = self.get_table(table)

        existing_ids = [row.get("id", 0) for row in table_data]
        next_id = max(existing_ids, default=0) + 1

        new_obj = {"id": next_id, **record}
        table_data.append(new_obj)

        return new_obj

    def update(self, table: str, filters: dict, new_values: dict):
        table_data = self.get_table(table)
        for row in table_data:
            if all(row.get(key) == v for key, v in filters.items()):  # noqa: WPS111, WPS221
                row.update(new_values)
        return self.find_one(table, **filters)


memory_storage = Memory()
