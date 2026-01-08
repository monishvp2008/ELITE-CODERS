from flask import Flask, render_template, redirect, url_for, session
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
    access_token_url="https://accounts.google.com/o/oauth2/token",
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    api_base_url="https://www.googleapis.com/oauth2/v1/",
    client_kwargs={"scope": "email profile"}
)

# -------------------------                 
# Routes
# -------------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login")
def login():
    return google.authorize_redirect(url_for("authorize", _external=True))


@app.route("/authorize")
def authorize():
    token = google.authorize_access_token()
    user_info = google.get("userinfo").json()

    user = User.query.filter_by(email=user_info["email"]).first()
    today = date.today()

    if not user:
        user = User(
            google_id=user_info["id"],
            name=user_info["name"],
            email=user_info["email"],
            streak=1,
            last_login=today
        )
        db.session.add(user)
    else:
        if user.last_login != today:
            user.streak += 1
            user.last_login = today

    db.session.commit()

    session["user_id"] = user.id

    return redirect("/dashboard")


# =========================
# DASHBOARD
# =========================
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])
    return render_template("dashboard.html", user=user)


# =========================
# JEE
# =========================
@app.route("/jee")
def jee_dashboard():
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])
    return render_template("jee.html", user=user)

# JEE PYQs
@app.route("/jee/pyqs")
def jee_pyqs():
    if "user_id" not in session:
        return redirect("/login")
    user = User.query.get(session["user_id"])
    return render_template("jeepyq.html", user=user)


@app.route("/neet")
def neet_dashboard():
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])
    return render_template("neet.html", user=user)


# NEET PYQs
@app.route("/neet/pyqs")
def neet_pyqs():
    if "user_id" not in session:
        return redirect("/login")
    user = User.query.get(session["user_id"])
    return render_template("neetpyq.html", user=user)



# =========================
# UPSC
# =========================
@app.route("/upsc")
def upsc_dashboard():
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])
    return render_template("upsc.html", user=user)


@app.route("/upsc/youtube")
def upsc_youtube_topics():
    if "user_id" not in session:
        return redirect("/login")
    user = User.query.get(session["user_id"])
    return render_template("upscyt.html",user=user)


@app.route("/upsc/pyqs")
def upsc_pyqs():
    if "user_id" not in session:
        return redirect("/login")
    user = User.query.get(session["user_id"])
    return render_template("upscpyq.html",user=user)


# =========================
# LOGOUT
# =========================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/jee/youtube/physics")
def jee_physics_youtube():
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])
    return render_template("jeephyyt.html", user=user)

@app.route("/jee/youtube/chemistry")
def jee_chemistry_youtube():
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])
    return render_template("jeechemyt.html", user=user)

@app.route("/jee/youtube/maths")
def jee_mathematics_youtube():
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])
    return render_template("jeemathyt.html", user=user)

@app.route("/neet/youtube/physics")
def neet_physics_youtube():
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])
    return render_template("neetphyyt.html", user=user)

@app.route("/neet/youtube/chemistry")
def neet_chemistry_youtube():
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])
    return render_template("neetchemyt.html", user=user)

@app.route("/neet/youtube/biology")
def neet_biology_youtube():
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])
    return render_template("neetbioyt.html", user=user)

@app.route("/upsc/youtube/current-affairs")
def upsc_youtube_current_affairs():
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])
    return render_template("cfyt.html", user=user)

@app.route("/upsc/youtube/polity")
def upsc_youtube_polity():
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])
    return render_template("polityyt.html", user=user)

@app.route("/upsc/youtube/history")
def upsc_youtube_history():
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])
    return render_template("hisyt.html", user=user)

@app.route("/upsc/youtube/geography")
def upsc_youtube_geography():
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])
    return render_template("geoyt.html", user=user)

@app.route("/upsc/youtube/economy")
def upsc_youtube_economy():
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])
    return render_template("ecoyt.html", user=user)

@app.route("/quiz")
def quiz():
    if "user_id" not in session:
        return redirect("/login")

    exam = request.args.get("exam", "jee").upper()
    return render_template("quiz.html", exam=exam)



if __name__ == '__main__':
    # host='0.0.0.0' is REQUIRED for Docker
    app.run(host='0.0.0.0', port=5000, debug=True)