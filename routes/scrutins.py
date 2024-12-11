from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import create_scrutin

scrutins_bp = Blueprint("scrutins", __name__)

@scrutins_bp.route("/create", methods=["GET", "POST"])
def create_scrutin_page():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        options = request.form.getlist("options")
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        organizer = request.form["organizer"]

        try:
            create_scrutin(title, description, options, start_date, end_date, organizer)
            flash("Scrutin créé avec succès", "success")
            return redirect(url_for("home.home"))
        except ValueError as e:
            flash(str(e), "danger")

    return render_template("scrutin_create.html")

@scrutins_bp.route("/results/<scrutin_id>")
def results(scrutin_id):
    scrutin = scrutins_collection.find_one({"_id": scrutin_id})
    if not scrutin:
        flash("Scrutin introuvable.", "danger")
        return redirect(url_for("home.home"))

    # Calcul des résultats (exemple simple)
    votes = votes_collection.find({"scrutin_id": scrutin_id})
    results = {option: 0 for option in scrutin["options"]}

    for vote in votes:
        for choice in vote["choices"]:
            if choice in results:
                results[choice] += 1

    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)

    return render_template("results.html", scrutin=scrutin, results=sorted_results)

