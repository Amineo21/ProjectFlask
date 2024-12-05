from flask import Flask, jsonify, request, render_template
from flask_pymongo import PyMongo

app = Flask(__name__)

# Route pour la page d'accueil
@app.route('/')
def home():
    user_name = "Alice"
    return render_template('index.html', name=user_name)


# Route pour la page "À propos"
@app.route('/about')
def about():
    return render_template('about.html')




# Configuration de la connexion à MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/mydatabase"  # ou MongoDB Atlas URI
mongo = PyMongo(app)

# Exemple de route pour insérer des données
@app.route('/add', methods=['POST'])
def add():
    data = request.json  # Données envoyées en JSON
    mongo.db.users.insert_one(data)  # Insère dans la collection "users"
    return jsonify(message="User added successfully"), 201

# Exemple de route pour récupérer des données
@app.route('/users', methods=['GET'])
def get_users():
    users = list(mongo.db.users.find())  # Récupère tous les documents
    for user in users:
        user["_id"] = str(user["_id"])  # Convertit ObjectId en chaîne
    return jsonify(users)

#Test de connexion à la base de donnée:
@app.route('/check', methods=['GET'])
def check():
    try:
        mongo.db.command("ping")  # Pinger MongoDB
        return jsonify(message="Connected to MongoDB"), 200
    except Exception as e:
        return jsonify(error=str(e)), 500



if __name__ == "__main__":
    app.run(debug=True)
