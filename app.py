# app.py
from flask import Flask
from database import init_db, close_db_connection
from auth import auth_bp
from admin import admin_bp
from member import member_bp

app = Flask(__name__)
app.secret_key = "super-secret-key"

# Register blueprints - this is used coz the routes have been separated from the app.py file and flask needs to know that they exists
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(member_bp, url_prefix="/member")


@app.teardown_appcontext
def teardown_db(error=None):
    close_db_connection(error)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
