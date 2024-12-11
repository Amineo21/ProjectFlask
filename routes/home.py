from flask import Blueprint, render_template
from models import scrutins_collection

home_bp = Blueprint("home", __name__)

@home_bp.route("/")
def home():
    # Récupère les derniers scrutins créés et actifs
    recent_scrutins = scrutins_collection.find().sort("created_at", -1).limit(10)
    active_scrutins = scrutins_collection.find({"closed": False}).sort("participants", -1).limit(10)
    return render_template("home.html", recent_scrutins=recent_scrutins, active_scrutins=active_scrutins)
