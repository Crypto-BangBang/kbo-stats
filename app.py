import os
import re
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from authlib.integrations.flask_client import OAuth
from scraper import (get_today_games, get_games_by_date, get_batting_stats, get_pitching_stats,
                     get_team_rankings, get_game_detail, get_player_detail)
from stadium_data import STADIUMS, STADIUM_COORDS
from cheer_data import CHEER_DATA
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "kbo-dev-secret-2026")

# ── DB ─────────────────────────────────────────────────
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///kbo.db")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# ── 로그인 매니저 ───────────────────────────────────────
login_manager = LoginManager(app)
login_manager.login_view = "login"

# ── OAuth ───────────────────────────────────────────────
oauth = OAuth(app)

KAKAO_CLIENT_ID = os.environ.get("KAKAO_CLIENT_ID", "")
naver = oauth.register(
    name="naver",
    client_id=os.environ.get("NAVER_CLIENT_ID"),
    client_secret=os.environ.get("NAVER_CLIENT_SECRET"),
    access_token_url="https://nid.naver.com/oauth2.0/token",
    authorize_url="https://nid.naver.com/oauth2.0/authorize",
    api_base_url="https://openapi.naver.com/v1/nid/",
    client_kwargs={"scope": "profile email"},
)

# ── 유저 모델 ────────────────────────────────────────────
class User(UserMixin, db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    email      = db.Column(db.String(200), unique=True)
    name       = db.Column(db.String(100))
    password   = db.Column(db.String(300))
    provider   = db.Column(db.String(50), default="email")
    avatar     = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))

with app.app_context():
    db.create_all()

# ── 메인 라우트 ─────────────────────────────────────────
@app.route("/")
def index():
    games = get_today_games()
    teams = get_team_rankings()
    today = datetime.now().strftime("%Y년 %m월 %d일")
    return render_template("index.html", games=games, teams=teams, today=today)

@app.route("/stats")
def stats():
    tab = request.args.get("tab", "batting")
    if tab == "pitching":
        data = get_pitching_stats()
    else:
        data = get_batting_stats()
    return render_template("stats.html", data=data, tab=tab)

@app.route("/api/stats")
def api_stats():
    tab = request.args.get("tab", "batting")
    if tab == "pitching":
        return jsonify(get_pitching_stats())
    return jsonify(get_batting_stats())

@app.route("/game/<game_code>")
def game_detail(game_code):
    data = get_game_detail(game_code)
    return render_template("game_detail.html", data=data, game_code=game_code)

@app.route("/player/<player_id>")
def player_detail(player_id):
    data = get_player_detail(player_id)
    return render_template("player_detail.html", data=data)

@app.route("/stadium")
def stadium():
    return render_template("stadium.html", stadiums=STADIUMS)

@app.route("/stadium/<stadium_id>")
def stadium_detail(stadium_id):
    s = STADIUMS.get(stadium_id)
    if not s:
        return redirect(url_for("stadium"))
    coords = STADIUM_COORDS.get(stadium_id, (37.5665, 126.9780))
    return render_template("stadium_detail.html", s=s, lat=coords[0], lon=coords[1])

@app.route("/cheer")
def cheer():
    team = request.args.get("team", "lg")
    if team not in CHEER_DATA:
        team = "lg"
    return render_template("cheer.html", cheer=CHEER_DATA, team=team, cur=CHEER_DATA[team])

@app.route("/schedule")
def schedule():
    from datetime import timedelta
    today = datetime.now()
    date_str = request.args.get("date", today.strftime("%Y%m%d"))
    if not re.match(r"^\d{8}$", date_str):
        date_str = today.strftime("%Y%m%d")
    games = get_games_by_date(date_str)
    dt        = datetime.strptime(date_str, "%Y%m%d")
    prev_date = (dt - timedelta(days=1)).strftime("%Y%m%d")
    next_date = (dt + timedelta(days=1)).strftime("%Y%m%d")
    display   = dt.strftime("%Y년 %m월 %d일")
    return render_template("schedule.html", games=games, date_str=date_str,
                           display=display, prev_date=prev_date, next_date=next_date,
                           now_str=today.strftime("%Y%m%d"),
                           yesterday_str=(today - timedelta(days=1)).strftime("%Y%m%d"),
                           week_ago_str=(today - timedelta(days=7)).strftime("%Y%m%d"))

@app.route("/tips")
def tips():
    return render_template("tips.html")

# ── 인증 ────────────────────────────────────────────────
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email    = request.form.get("email","").strip()
        password = request.form.get("password","")
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password or "", password):
            login_user(user)
            return redirect(url_for("index"))
        flash("이메일 또는 비밀번호가 올바르지 않아요.")
    return render_template("login.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        email    = request.form.get("email","").strip()
        name     = request.form.get("name","").strip()
        password = request.form.get("password","")
        if User.query.filter_by(email=email).first():
            flash("이미 가입된 이메일이에요.")
            return redirect(url_for("register"))
        user = User(email=email, name=name, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for("index"))
    return render_template("register.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

# ── Kakao OAuth ──────────────────────────────────────────
@app.route("/auth/kakao")
def kakao_login():
    redirect_uri = url_for("kakao_callback", _external=True)
    kakao_auth_url = (
        "https://kauth.kakao.com/oauth/authorize"
        f"?client_id={KAKAO_CLIENT_ID}"
        f"&redirect_uri={redirect_uri}"
        "&response_type=code"
    )
    return redirect(kakao_auth_url)

@app.route("/auth/kakao/callback")
def kakao_callback():
    code = request.args.get("code")
    redirect_uri = url_for("kakao_callback", _external=True)
    token_res = requests.post("https://kauth.kakao.com/oauth/token", data={
        "grant_type":   "authorization_code",
        "client_id":    KAKAO_CLIENT_ID,
        "redirect_uri": redirect_uri,
        "code":         code,
    })
    access_token = token_res.json().get("access_token")
    user_res = requests.get("https://kapi.kakao.com/v2/user/me",
                            headers={"Authorization": f"Bearer {access_token}"})
    info = user_res.json()
    kakao_account = info.get("kakao_account", {})
    profile = kakao_account.get("profile", {})
    uid    = info.get("id", "unknown")
    email  = kakao_account.get("email", f"kakao_{uid}@kakao.com")
    name   = profile.get("nickname", "카카오유저")
    avatar = profile.get("profile_image_url", "")
    return _oauth_login(email, name, avatar, "kakao")

# ── Naver OAuth ──────────────────────────────────────────
@app.route("/auth/naver")
def naver_login():
    redirect_uri = url_for("naver_callback", _external=True)
    return naver.authorize_redirect(redirect_uri)

@app.route("/auth/naver/callback")
def naver_callback():
    naver.authorize_access_token()
    resp = naver.get("me")
    info = resp.json().get("response", {})
    return _oauth_login(info.get("email",""), info.get("name","네이버유저"), info.get("profile_image",""), "naver")

def _oauth_login(email, name, avatar, provider):
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email, name=name, avatar=avatar, provider=provider)
        db.session.add(user)
        db.session.commit()
    login_user(user)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5002)
