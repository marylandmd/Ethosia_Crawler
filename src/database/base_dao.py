
class BaseDAO:
    def __init__(self, client, db, collection):
        self.db = client[db]
        self.collection = self.db[collection]

    def save(self, item):
        return self.collection.insert_one(item)

    def save_many(self, items):
        return self.collection.insert_many(items)

    def find(self, query):
        return self.collection.find(query, {'_id': False})

    def find_all(self, query, projection):
        return self.collection.find(query, projection)

    def find_one(self, query):
        return self.collection.find_one(query)

    def update(self, query, item):
        return self.collection.update_one(query, item)

    def delete(self, query):
        return self.collection.delete_one(query)

    def delete_many(self, query):
        return self.collection.delete_many(query)