from flask import Blueprint, render_template
from models import scrutins_collection, votes_collection

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin/stats")
def stats():
    # Scrutins avec le plus de participants
    top_scrutins = scrutins_collection.find().sort("participants", -1).limit(5)

    # Répartition des votes par année de naissance
    votes_by_year = votes_collection.aggregate([
        {"$group": {"_id": "$year_of_birth", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ])

    # Moyenne des options des scrutins
    avg_options = scrutins_collection.aggregate([
        {"$project": {"num_options": {"$size": "$options"}}},
        {"$group": {"_id": None, "avg": {"$avg": "$num_options"}}}
    ])
    avg_options_result = list(avg_options)
    avg_options = avg_options_result[0]["avg"] if avg_options_result else 0

    return render_template("admin_stats.html", top_scrutins=top_scrutins, votes_by_year=votes_by_year, avg_options=avg_options)
