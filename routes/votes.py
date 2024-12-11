import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import scrutins_collection, votes_collection

votes_bp = Blueprint("votes", __name__)

@votes_bp.route("/participate/<scrutin_id>", methods=["GET", "POST"])
def participate(scrutin_id):
    scrutin = scrutins_collection.find_one({"_id": scrutin_id})
    if not scrutin:
        flash("Scrutin introuvable.", "danger")
        return redirect(url_for("home.home"))

    if request.method == "POST":
        pseudo = request.form["pseudo"]
        choices = request.form.getlist("choices")

        if not choices:
            flash("Veuillez sélectionner au moins une option.", "danger")
        else:
            vote = {
                "scrutin_id": scrutin_id,
                "pseudo": pseudo,
                "choices": choices,
                "created_at": datetime.utcnow()
            }
            votes_collection.insert_one(vote)
            scrutins_collection.update_one({"_id": scrutin_id}, {"$inc": {"participants": 1}})
            flash("Votre vote a été enregistré.", "success")
            return redirect(url_for("home.home"))

    return render_template("vote.html", scrutin=scrutin)
