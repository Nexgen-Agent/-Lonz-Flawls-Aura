# backend/database/mock_connection.py

class MockCollection:
    def __init__(self):
        self.data = []

    def insert_one(self, item):
        self.data.append(item)
        return item

    def update_one(self, query, update):
        for item in self.data:
            match = True
            for k, v in query.items():
                if item.get(k) != v:
                    match = False
                    break
            if match:
                if "$set" in update:
                    item.update(update["$set"])
                return True
        return False

    def find_one(self, query=None, projection=None, sort=None):
        data = self.data
        if sort:
            key, direction = sort[0]
            data = sorted(data, key=lambda x: str(x.get(key, "")), reverse=(direction == -1))

        for item in data:
            match = True
            if query:
                for k, v in query.items():
                    if item.get(k) != v:
                        match = False
                        break
            if match:
                res = item.copy()
                if projection and "_id" in projection and projection["_id"] == 0:
                    res.pop("_id", None)
                return res
        return None

    def find(self, query=None):
        if query is None:
            return self.data

        results = []
        for item in self.data:
            match = True
            for k, v in query.items():
                if item.get(k) != v:
                    match = False
                    break
            if match:
                results.append(item)
        return results

    def count_documents(self, query):
        if not query:
            return len(self.data)
        return len(self.find(query))

class MockDatabase:
    def __init__(self):
        self.collections = {}

    def __getattr__(self, name):
        if name not in self.collections:
            self.collections[name] = MockCollection()
        return self.collections[name]

    def get_collection(self, name):
        return getattr(self, name)

    def command(self, cmd):
        if cmd == "ping":
            return True
        return None

def get_db():
    return MockDatabase()
