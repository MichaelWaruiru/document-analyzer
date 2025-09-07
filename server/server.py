from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(100), unique=True, nullable=False)
  email = db.Column(db.String(200), unique=True, nullable=False)
  password = db.Column(db.String(200), nullable=False)
  is_admin = db.Column(db.Boolean, default=False)
  

class AnalysisLog(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
  filename = db.Column(db.String(200))
  upload_time = db.Column(db.DateTime, default=datetime.now)
  risk_score = db.Column(db.Float)
  highlights = db.Column(db.Text)
  user = db.relationship("User", backref="analyses")