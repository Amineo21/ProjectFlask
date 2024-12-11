from datetime import datetime
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client.scrutin_platform

# Modèle Utilisateur
users_collection = db.users
scrutins_collection = db.scrutins
votes_collection = db.votes

def create_user(pseudo, personal_info):
    if users_collection.find_one({"pseudo": pseudo}):
        raise ValueError("Le pseudonyme est déjà utilisé.")
    user = {
        "pseudo": pseudo,
        "personal_info": personal_info,
        "created_at": datetime.utcnow(),
        "closed": False
    }
    users_collection.insert_one(user)

def create_scrutin(title, description, options, start_date, end_date, organizer):
    if len(options) < 2:
        raise ValueError("Un scrutin doit avoir au moins deux options.")
    scrutin = {
        "title": title,
        "description": description,
        "options": options,
        "start_date": start_date,
        "end_date": end_date,
        "organizer": organizer,
        "participants": 0,
        "created_at": datetime.utcnow(),
        "closed": False
    }
    scrutins_collection.insert_one(scrutin)
