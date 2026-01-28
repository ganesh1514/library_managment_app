from flask import Blueprint, render_template
from database import get_db_connection
from auth import token_required

member_bp = Blueprint("member", __name__)


# ---------------- MEMBER DASHBOARD ----------------
@member_bp.route("/dashboard")
@token_required(role="member")
def dashboard():
    return render_template("member/dashboard.html")


# ---------------- VIEW AVAILABLE BOOKS ----------------
@member_bp.route("/books")
@token_required(role="member")
def books():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Only available books should be visible to members
    books = cursor.execute(
        "SELECT id, title, author FROM books WHERE available = 1"
    ).fetchall()

    return render_template("member/books.html", books=books)
