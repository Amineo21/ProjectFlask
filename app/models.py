from app import mongo 

class Scrutin:
    @staticmethod
    def create_scrutin(data):
        mongo.db.scrutins.insert_one(data)

    @staticmethod
    def get_active_scrutins():
        return list(mongo.db.scrutins.find({"status": "active"}))

    @staticmethod
    def close_scrutin(scrutin_id):
        mongo.db.scrutins.update_one({"_id": scrutin_id}, {"$set": {"status": "closed"}})
