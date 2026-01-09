from functools import wraps
from flask import Flask, render_template, redirect, url_for, session, g
from authlib.integrations.flask_client import OAuth
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from flask import request


# -------------------------
# App setup
# -------------------------
app = Flask(__name__)
app.secret_key = "THIS_SHOULD_BE_SECRET"

app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = False

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# -------------------------
# Database model
# -------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(200), unique=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    streak = db.Column(db.Integer, default=1)
    last_login = db.Column(db.Date)

# -------------------------
# OAuth setup
# -------------------------
oauth = OAuth(app)

google = oauth.register(
    name="google",
    client_id="659446210252-6m90c2g5t3f9oq1r37d412on8nk4uh0q.apps.googleusercontent.com",
    client_secret="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",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"}
)

# =========================
# LOGIN REQUIRED DECORATOR
# =========================
def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        user_id = session.get("user_id")
        if not user_id:
            return redirect(url_for("login"))

        user = db.session.get(User, user_id)
        if not user:
            session.clear()
            return redirect(url_for("login"))

        g.user = user
        return view(*args, **kwargs)
    return wrapped_view

# =========================
# OAUTH SETUP
# =========================

# =========================
# AUTH ROUTES
# =========================
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login():
    return google.authorize_redirect(url_for("authorize", _external=True))

@app.route("/authorize")
def authorize():
    google.authorize_access_token()
    user_info = google.userinfo()

    today = date.today()
    user = User.query.filter_by(email=user_info["email"]).first()

    if not user:
        user = User(
            google_id=user_info["sub"],
            name=user_info["name"],
            email=user_info["email"],
            streak=1,
            last_login=today,
        )
        db.session.add(user)
    else:
        if user.last_login != today:
            user.streak += 1
            user.last_login = today

    db.session.commit()
    session["user_id"] = user.id
    return redirect(url_for("dashboard"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# =========================
# DASHBOARD
# =========================
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=g.user)

# =========================
# JEE
# =========================
@app.route("/jee")
@login_required
def jee_dashboard():
    return render_template("jee.html", user=g.user)

@app.route("/jee/pyqs")
@login_required
def jee_pyqs():
    return render_template("jeepyq.html", user=g.user)

@app.route("/jee/youtube/physics")
@login_required
def jee_physics_youtube():
    return render_template("jeephyyt.html", user=g.user)

@app.route("/jee/youtube/chemistry")
@login_required
def jee_chemistry_youtube():
    return render_template("jeechemyt.html", user=g.user)

@app.route("/jee/youtube/maths")
@login_required
def jee_mathematics_youtube():
    return render_template("jeemathyt.html", user=g.user)

# =========================
# NEET
# =========================
@app.route("/neet")
@login_required
def neet_dashboard():
    return render_template("neet.html", user=g.user)

@app.route("/neet/pyqs")
@login_required
def neet_pyqs():
    return render_template("neetpyq.html", user=g.user)

@app.route("/neet/youtube/physics")
@login_required
def neet_physics_youtube():
    return render_template("neetphyyt.html", user=g.user)

@app.route("/neet/youtube/chemistry")
@login_required
def neet_chemistry_youtube():
    return render_template("neetchemyt.html", user=g.user)

@app.route("/neet/youtube/biology")
@login_required
def neet_biology_youtube():
    return render_template("neetbioyt.html", user=g.user)

# =========================
# UPSC
# =========================
@app.route("/upsc")
@login_required
def upsc_dashboard():
    return render_template("upsc.html", user=g.user)

@app.route("/upsc/pyqs")
@login_required
def upsc_pyqs():
    return render_template("upscpyq.html", user=g.user)

@app.route("/upsc/youtube")
@login_required
def upsc_youtube_topics():
    return render_template("upscyt.html", user=g.user)

@app.route("/upsc/youtube/current-affairs")
@login_required
def upsc_youtube_current_affairs():
    return render_template("cfyt.html", user=g.user)

@app.route("/upsc/youtube/polity")
@login_required
def upsc_youtube_polity():
    return render_template("polityyt.html", user=g.user)

@app.route("/upsc/youtube/history")
@login_required
def upsc_youtube_history():
    return render_template("hisyt.html", user=g.user)

@app.route("/upsc/youtube/geography")
@login_required
def upsc_youtube_geography():
    return render_template("geoyt.html", user=g.user)

@app.route("/upsc/youtube/economy")
@login_required
def upsc_youtube_economy():
    return render_template("ecoyt.html", user=g.user)

# =========================
# QUIZ
# =========================
@app.route("/quiz")
@login_required
def quiz():
    exam = request.args.get("exam", "jee").upper()
    return render_template("quiz.html", exam=exam)

# =========================
# RUN
# =========================
if __name__ == '__main__':
    # host='0.0.0.0' is REQUIRED for Docker
    app.run(host='0.0.0.0', port=5000, debug=True)
