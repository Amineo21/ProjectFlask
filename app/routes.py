from flask import render_template, redirect, url_for, request, flash
from app import app, mongo
from app.models import Scrutin
from bson.objectid import ObjectId

@app.route('/')
def home():
    active_scrutins = Scrutin.get_active_scrutins()
    return render_template('home.html', scrutins=active_scrutins)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        if mongo.db.users.find_one({"username": username}):
            flash('Pseudonyme déjà pris.')
            return redirect(url_for('register'))
        user = {
            "username": username,
            "email": request.form['email'],
            "birth_year": request.form['birth_year']
        }
        mongo.db.users.insert_one(user)
        flash('Enregistrement réussi!')
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/profile/<username>', methods=['GET', 'POST'])
def profile(username):
    user = mongo.db.users.find_one({"username": username})
    if not user:
        flash('Utilisateur introuvable!')
        return redirect(url_for('home'))
    if request.method == 'POST':
        updated_info = {
            "email": request.form['email'],
            "birth_year": request.form['birth_year']
        }
        mongo.db.users.update_one({"username": username}, {"$set": updated_info})
        flash('Profil mis à jour!')
    return render_template('profile.html', user=user)

@app.route('/create_scrutin', methods=['GET', 'POST'])
def create_scrutin():
    if request.method == 'POST':
        data = {
            "question": request.form['question'],
            "options": request.form.getlist('options'),
            "start_date": request.form['start_date'],
            "end_date": request.form['end_date'],
            "status": "active"
        }
        Scrutin.create_scrutin(data)
        flash('Scrutin créé!')
        return redirect(url_for('home'))
    return render_template('create_scrutin.html')

@app.route('/vote/<scrutin_id>', methods=['GET', 'POST'])
def vote(scrutin_id):
    scrutin = mongo.db.scrutins.find_one({"_id": ObjectId(scrutin_id)})
    if not scrutin:
        flash('Scrutin introuvable!')
        return redirect(url_for('home'))
    if request.method == 'POST':
        votes = request.form.getlist('votes')
        vote_data = {
            "scrutin_id": scrutin_id,
            "username": request.form['username'],
            "votes": votes
        }
        mongo.db.votes.insert_one(vote_data)
        flash('Vote enregistré!')
        return redirect(url_for('home'))
    return render_template('vote.html', scrutin=scrutin)
