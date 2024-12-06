from flask import Flask, render_template, request
from flask_pymongo import PyMongo

app = Flask(__name__)

# Configuration MongoDB (changer avec votre URI MongoDB si nécessaire)
app.config["MONGO_URI"] = "mongodb://localhost:27017/scrutin_app"
mongo = PyMongo(app)
 


@app.route("/")
def index():
    """
    Page de consultation des différents scrutins
    """
    scrutins = mongo.db.scrutins.find()  # Récupère tous les scrutins
    return render_template("index.html", scrutins=scrutins)

@app.route("/statistics")
def statistics():
    """
    Page de statistiques
    """
    scrutins = list(mongo.db.scrutins.find())
    if not scrutins:
        return render_template("statistics.html", stats={})

    # Scrutin avec le plus de participants
    max_participants = max(scrutins, key=lambda x: x.get("participants", 0))
    max_scrutin = {
        "title": max_participants["title"],
        "participants": max_participants["participants"],
    }

    # Pourcentage des années ayant répondu une réponse spécifique
    total_scrutins = len(scrutins)
    question_stat = {}
    for scrutin in scrutins:
        for question in scrutin.get("questions", []):
            for response, count in question.get("responses", {}).items():
                if response not in question_stat:
                    question_stat[response] = 0
                question_stat[response] += count

    # Moyenne des options proposées
    moyenne_options = sum(
        sum(q.get("responses", {}).values()) for s in scrutins for q in s.get("questions", [])
    ) / total_scrutins

    stats = {
        "max_scrutin": max_scrutin,
        "response_percentage": question_stat,
        "moyenne_options": round(moyenne_options, 2),
    }

    return render_template("statistics.html", stats=stats)

if __name__ == "__main__":
    app.run(debug=True)







# from flask import Flask, jsonify, request, render_template
# from flask_pymongo import PyMongo

# app = Flask(__name__)

# # Route pour la page d'accueil
# @app.route('/')
# def home():
#     user_name = "Alice"
#     return render_template('index.html', name=user_name)


# # Route pour la page "À propos"
# @app.route('/about')
# def about():
#     return render_template('about.html')




# # Configuration de la connexion à MongoDB
# app.config["MONGO_URI"] = "mongodb://localhost:27017/mydatabase"  # ou MongoDB Atlas URI
# mongo = PyMongo(app)

# # Exemple de route pour insérer des données
# @app.route('/add', methods=['POST'])
# def add():
#     data = request.json  # Données envoyées en JSON
#     mongo.db.users.insert_one(data)  # Insère dans la collection "users"
#     return jsonify(message="User added successfully"), 201

# # Exemple de route pour récupérer des données
# @app.route('/users', methods=['GET'])
# def get_users():
#     users = list(mongo.db.users.find())  # Récupère tous les documents
#     for user in users:
#         user["_id"] = str(user["_id"])  # Convertit ObjectId en chaîne
#     return jsonify(users)

# #Test de connexion à la base de donnée:
# @app.route('/check', methods=['GET'])
# def check():
#     try:
#         mongo.db.command("ping")  # Pinger MongoDB
#         return jsonify(message="Connected to MongoDB"), 200
#     except Exception as e:
#         return jsonify(error=str(e)), 500



# if __name__ == "__main__":
#     app.run(debug=True)
