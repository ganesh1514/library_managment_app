from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import get_db_connection
from auth import token_required

admin_bp = Blueprint("admin", __name__)


# ---------------- ADMIN DASHBOARD ----------------
@admin_bp.route("/dashboard")
@token_required(role="admin")  # rbac
def dashboard():
    return render_template("admin/dashboard.html")


# ---------------- VIEW + ADD BOOKS ----------------
@admin_bp.route("/books", methods=["GET", "POST"])
@token_required(role="admin")
def books():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Add new book (only feature allowed)
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]

        cursor.execute(
            "INSERT INTO books (title, author, available) VALUES (?, ?, 1)",
            (title, author),
        )
        conn.commit()
        flash("Book added successfully", "success")

    # View ALL books (available + issued)
    books = cursor.execute("SELECT id, title, author, available FROM books").fetchall()

    return render_template("admin/books.html", books=books)
