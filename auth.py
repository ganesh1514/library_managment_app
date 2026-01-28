# auth.py
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    make_response,
)
import jwt
import datetime
import bcrypt
from functools import wraps
from database import get_db_connection

auth_bp = Blueprint("auth", __name__)

SECRET_KEY = "jwt-secret-key"
TOKEN_EXP_MINUTES = 30


def generate_token(user_id, role):
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.datetime.utcnow()
        + datetime.timedelta(minutes=TOKEN_EXP_MINUTES),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def token_required(role=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = request.cookies.get("token")
            if not token:
                flash("Login required", "danger")
                return redirect(url_for("auth.login"))

            try:
                data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                if role and data["role"] != role:
                    flash("Unauthorized access", "danger")
                    return redirect(url_for("auth.login"))
            except jwt.ExpiredSignatureError:
                flash("Session expired", "danger")
                return redirect(url_for("auth.login"))
            except jwt.InvalidTokenError:
                flash("Invalid token", "danger")
                return redirect(url_for("auth.login"))

            return f(*args, **kwargs)

        return wrapper

    return decorator


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()

        if user and bcrypt.checkpw(password.encode(), user["password"]):
            token = generate_token(user["id"], user["role"])
            resp = make_response(
                redirect(
                    url_for("admin.dashboard")
                    if user["role"] == "admin"
                    else url_for("member.dashboard")
                )
            )
            resp.set_cookie("token", token, httponly=True)
            return resp

        flash("Invalid credentials", "danger")

    return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = bcrypt.hashpw(request.form["password"].encode(), bcrypt.gensalt())
        role = request.form["role"]

        conn = get_db_connection()
        try:
            conn.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, password, role),
            )
            conn.commit()
            flash("Registration successful", "success")
            return redirect(url_for("auth.login"))
        except:  # noqa: E722
            flash("Username already exists", "danger")
        finally:
            pass

    return render_template("register.html")


@auth_bp.route("/logout")
def logout():
    resp = make_response(redirect(url_for("auth.login")))
    resp.delete_cookie("token")
    return resp
