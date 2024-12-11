import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import users_collection

users_bp = Blueprint("users", __name__)

@users_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        pseudo = request.form["pseudo"]
        personal_info = {
            "nom": request.form["nom"],
            "prenom": request.form["prenom"],
            "email": request.form["email"]
        }

        if users_collection.find_one({"pseudo": pseudo}):
            flash("Le pseudonyme est déjà utilisé. Veuillez en choisir un autre.", "danger")
        else:
            user = {
                "pseudo": pseudo,
                "personal_info": personal_info,
                "created_at": datetime.utcnow(),
                "closed": False
            }
            users_collection.insert_one(user)
            flash("Inscription réussie !", "success")
            return redirect(url_for("users.profile", pseudo=pseudo))

    return render_template("register.html")

@users_bp.route("/profile/<pseudo>")
def profile(pseudo):
    user = users_collection.find_one({"pseudo": pseudo})
    if not user:
        flash("Utilisateur introuvable.", "danger")
        return redirect(url_for("home.home"))

    return render_template("profile.html", user=user)
