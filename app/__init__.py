from flask import Flask
from flask_pymongo import PyMongo
# from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost:27017/scrutinDB"
app.config['SECRET_KEY'] = 'your-secret-key'
mongo = PyMongo(app)
# csrf = CSRFProtect(app)

from app import routes
