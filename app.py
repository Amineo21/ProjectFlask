from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)

# Configuration MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/scrutin_platform"
mongo = PyMongo(app)

# Import des routes
from routes.home import home_bp
from routes.users import users_bp
from routes.scrutins import scrutins_bp
from routes.votes import votes_bp
from routes.admin import admin_bp

# Enregistrement des blueprints
app.register_blueprint(home_bp)
app.register_blueprint(users_bp, url_prefix="/users")
app.register_blueprint(scrutins_bp, url_prefix="/scrutins")
app.register_blueprint(votes_bp, url_prefix="/votes")
app.register_blueprint(admin_bp, url_prefix="/admin")

if __name__ == "__main__":
    app.run(debug=True)