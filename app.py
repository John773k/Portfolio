import os
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-this-secret-key-before-deploying")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(app.instance_path, "portfolio.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = os.path.join("static", "uploads")
app.config["MAX_CONTENT_LENGTH"] = 4 * 1024 * 1024
os.makedirs(app.instance_path, exist_ok=True)
os.makedirs(os.path.join(app.root_path, app.config["UPLOAD_FOLDER"]), exist_ok=True)

db = SQLAlchemy(app)
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "gif"}

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    technologies = db.Column(db.String(250), default="")
    project_url = db.Column(db.String(300), default="")
    github_url = db.Column(db.String(300), default="")
    image = db.Column(db.String(300), default="")
    featured = db.Column(db.Boolean, default=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("admin"):
            return redirect(url_for("admin_login"))
        return view(*args, **kwargs)
    return wrapped

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    projects = Project.query.order_by(Project.featured.desc(), Project.id.desc()).all()
    return render_template("index.html", projects=projects)

@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()
    if not name or not email or not message:
        flash("Please complete every contact field.", "error")
    elif len(message) > 3000:
        flash("Your message is too long. Please keep it under 3,000 characters.", "error")
    else:
        db.session.add(Message(name=name, email=email, message=message))
        db.session.commit()
        flash("Thanks! Your message has been received.", "success")
    return redirect(url_for("home") + "#contact")

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        admin_user = os.environ.get("ADMIN_USERNAME", "admin")
        admin_hash = os.environ.get("ADMIN_PASSWORD_HASH")
        # Development fallback: change these credentials before publishing.
        valid = (username == admin_user and
                 (check_password_hash(admin_hash, password) if admin_hash else password == "ChangeMe123!"))
        if valid:
            session["admin"] = True
            return redirect(url_for("dashboard"))
        flash("Invalid username or password.", "error")
    return render_template("login.html")

@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/admin")
@login_required
def dashboard():
    projects = Project.query.order_by(Project.id.desc()).all()
    messages = Message.query.order_by(Message.created_at.desc()).all()
    return render_template("dashboard.html", projects=projects, messages=messages)

@app.route("/admin/projects/new", methods=["GET", "POST"])
@app.route("/admin/projects/<int:project_id>/edit", methods=["GET", "POST"])
@login_required
def edit_project(project_id=None):
    project = Project.query.get_or_404(project_id) if project_id else Project()
    if request.method == "POST":
        project.title = request.form.get("title", "").strip()
        project.description = request.form.get("description", "").strip()
        project.technologies = request.form.get("technologies", "").strip()
        project.project_url = request.form.get("project_url", "").strip()
        project.github_url = request.form.get("github_url", "").strip()
        project.featured = request.form.get("featured") == "on"
        upload = request.files.get("image")
        if upload and upload.filename:
            if not allowed_file(upload.filename):
                flash("Use a PNG, JPG, JPEG, WEBP or GIF image.", "error")
                return render_template("project_form.html", project=project)
            filename = secure_filename(upload.filename)
            unique_name = f"{os.urandom(8).hex()}_{filename}"
            upload.save(os.path.join(app.root_path, app.config["UPLOAD_FOLDER"], unique_name))
            project.image = "uploads/" + unique_name
        if not project.title or not project.description:
            flash("Project title and description are required.", "error")
            return render_template("project_form.html", project=project)
        db.session.add(project)
        db.session.commit()
        flash("Project saved.", "success")
        return redirect(url_for("dashboard"))
    return render_template("project_form.html", project=project)

@app.route("/admin/projects/<int:project_id>/delete", methods=["POST"])
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    flash("Project deleted.", "success")
    return redirect(url_for("dashboard"))

@app.route("/admin/messages/<int:message_id>/delete", methods=["POST"])
@login_required
def delete_message(message_id):
    message = Message.query.get_or_404(message_id)
    db.session.delete(message)
    db.session.commit()
    flash("Message deleted.", "success")
    return redirect(url_for("dashboard") + "#messages")

with app.app_context():
    db.create_all()
    if Project.query.count() == 0:
        db.session.add_all([
            Project(title="LogiTrack — Supply Chain Analytics",
                    description="A supply-chain analytics platform concept for tracking shipments, monitoring warehouse inventory and identifying logistics bottlenecks.",
                    technologies="Python, Flask, Pandas, SQL, JavaScript",
                    github_url="https://github.com/", featured=True),
            Project(title="Developer Portfolio",
                    description="A responsive personal portfolio with a Flask-powered admin dashboard and contact inbox.",
                    technologies="HTML, CSS, JavaScript, Python, Flask, SQLite",
                    github_url="https://github.com/", featured=True)
        ])
        db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)
