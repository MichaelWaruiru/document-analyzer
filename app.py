from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from models.models import User, db, AnalysisLog
from ml.analyzer import analyze_document
from config import Config

UPLOAD_EXTENSIONS = ['.txt', '.pdf', '.docx']
UPLOAD_PATH = 'static/uploads'

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

"""Forms"""
class LoginForm(FlaskForm):
  email = StringField("Email", filters=[lambda x: x.strip() if x else x], validators=[InputRequired(), Email(check_deliverability=False)])
  password = PasswordField("Password", validators=[InputRequired()])
  
class RegisterForm(FlaskForm):
  username = StringField("Username", validators=[InputRequired(), Length(min=4, max=100)])
  email = StringField("Email", filters=[lambda x: x.strip() if x else x], validators=[InputRequired(), Email(check_deliverability=False)])
  password = PasswordField("Password", validators=[InputRequired(), Length(min=6)])
  confirm_password = PasswordField("Confirm Password", validators=[InputRequired(), EqualTo("password", message="Passwords must match")])
  
class DeleteForm(FlaskForm):
  pass

# Creates all tables in mysql
@app.cli.command("init-db")
def init_db():
    db.create_all()
    print("Database tables created!")
  
@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

"""Routes"""
@app.route("/")
def index():
  return render_template("index.html")

@app.route("/register", methods=["POST", "GET"])
def register():
  form = RegisterForm()
  if form.validate_on_submit():
    hash_password = generate_password_hash(form.password.data)
    email = form.email.data.strip().lower()
    user = User(username=form.username.data, email=email, password=hash_password)
    db.session.add(user)
    db.session.commit()
    flash("Registration successful. Please log in.")
    return redirect(url_for("login"))
  elif request.method == "POST":
    flash("Form validation failed.Please try again.")
    print("Register form errors:", form.errors)
  return render_template("register.html", form=form)

@app.route("/login", methods=["POST", "GET"])
def login():
  form = LoginForm()
  if request.method == "POST":
    print("Raw email from POST:", request.form.get("email"))
  if form.validate_on_submit():
    email = form.email.data.strip().lower()
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, form.password.data):
      login_user(user)
      return redirect(url_for("index"))
    flash("Invalid credentials. Check email and password.")
  elif request.method == "POST":
    flash("Form validation failed. Please try again.")
    print("Login form errors:", form.errors)
  return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
  logout_user()
  return redirect(url_for("index"))

@app.route("/dashboard")
@login_required
def dashboard():
  logs = AnalysisLog.query.filter_by(user_id=current_user.id).order_by(AnalysisLog.upload_time.desc()).all()
  form = DeleteForm()
  return render_template("dashboard.html", logs=logs, form=form)

@app.route("/analyze", methods=["POST"])
# @login_required
def analyze():
  uploaded_file = request.files["document"]
  filename = secure_filename(uploaded_file.filename)
  if filename == "":
    return jsonify({"error": "No file selected"}), 400
  file_ext = os.path.splitext(filename)[1].lower()
  if file_ext not in UPLOAD_EXTENSIONS:
    return jsonify({"error": "Invalid file type"}), 400
  text = ""
  # Handle different file types
  if file_ext == ".txt":
    text = uploaded_file.read().decode("utf-8", "ignore")
  elif file_ext == ".pdf":
    from PyPDF2 import PdfReader
    reader = PdfReader(uploaded_file)
    for page in reader.pages:
      text += page.extract_text() or ""
  elif file_ext == ".docx":
    from docx import Document
    doc = Document(uploaded_file)
    text = "\n".join([p.text for p in doc.paragraphs])
  else:
    return jsonify({"error": "Unsupported file type"}), 400
  
  result = analyze_document(text)
  # log = AnalysisLog(user_id=current_user.id, filename=filename, risk_score=result["risk_score"], highlights="\n".join(result["highlights"]))
  # db.session.add(log)
  # db.session.commit()
  # return jsonify(result)
  
  # Only save log if the user is authenticated (logged in)
  if hasattr(current_user, "is_authenticated") and current_user.is_authenticated:
      log = AnalysisLog(
          user_id=current_user.id,
          filename=filename,
          risk_score=result["risk_score"],
          highlights="\n".join(result["highlights"])
      )
      db.session.add(log)
      db.session.commit()
  # For anonymous users, just return the result (don't try to access current_user.id)
  return jsonify(result)

@app.route("/delete-log/<int:log_id>", methods=["POST"])
@login_required
def delete_log(log_id):
  form = DeleteForm()
  if form.validate_on_submit():
    log = AnalysisLog.query.get_or_404(log_id)
    if log.user_id != current_user.id:
      flash("You do not have permission to delete this log.", "danger")
      return redirect(url_for("dashboard"))
    db.session.delete(log)
    db.session.commit()
    flash("Log deleted successfully.", "success")
    return redirect(url_for("dashboard"))
  else:
    flash("Invalid CSRF token or form submission.", "danger")
    return redirect(url_for("dashboard"))

"""Optional--> Route for admin"""
@app.route("/admin")
@login_required
def admin():
  if not current_user.is_admin:
    flash("Admin only!")
    return redirect(url_for("dashboard"))
  users = User.query.all()
  analyses = AnalysisLog.query.order_by(AnalysisLog.upload_time.desc()).all()
  return render_template("admin.html", users=users, analyses=analyses)

if __name__ == "__main__":
  app.run(debug=True, port=5000)