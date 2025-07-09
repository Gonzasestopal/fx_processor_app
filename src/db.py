class Memory(object):  # noqa: WPS214
    _instance = None

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

    def insert(self, table: str, record: dict):
        next_id_to_insert = len(self.get_table(table)) + 1
        new_obj = {'id': next_id_to_insert, **record}
        self.get_table(table).append(new_obj)
        return new_obj

    def update(self, table: str, filters: dict, new_values: dict):
        table_data = self.get_table(table)
        for row in table_data:
            if all(row.get(key) == v for key, v in filters.items()):  # noqa: WPS111, WPS221
                row.update(new_values)
        return self.find_one(table, **filters)


memory_storage = Memory()
