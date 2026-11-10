"""Student Project Portal: read sections in order, then follow STUDENT-GUIDE.md.
Teaching application with fictional data. Run only in your private lab.
"""
from functools import wraps
from pathlib import Path
import os
import re
import secrets
import sqlite3
import time
import unicodedata

from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, InvalidHashError
from flask import Flask, abort, flash, g, redirect, render_template, request, session, url_for
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from flask_wtf.csrf import CSRFProtect

# 1. SETUP: app joins URLs, Python functions and templates.
app = Flask(__name__)
instance = Path(app.instance_path)
instance.mkdir(exist_ok=True)
# A different local secret for every copy. Never commit instance/ to Git.
secret_file = instance / "secret.key"
if not secret_file.exists():
    secret_file.write_text(secrets.token_hex(32))
app.config.update(
    SECRET_KEY=os.environ.get("SECRET_KEY") or secret_file.read_text().strip(),
    DATABASE=str(instance / "portal.sqlite"),
    MAX_CONTENT_LENGTH=16 * 1024,
    SESSION_COOKIE_NAME="portal_session",
    # HTTPS is provided by the private Codespaces forwarded URL.
    SESSION_COOKIE_SECURE=os.environ.get("CODESPACES") == "true" or os.environ.get("LAB_HTTPS") == "1",
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    WTF_CSRF_ENABLED=True,
)
ph = PasswordHasher()  # Argon2id; the library generates a fresh salt each time.
DUMMY_HASH = ph.hash("Dummy account with no login")
login_manager = LoginManager(app)
login_manager.login_view = "login"

# 2. DATABASE: one connection per request, closed afterwards.
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row  # row["username"] is clearer than row[1].
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db

@app.teardown_appcontext
def close_db(error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    """Reset fictional data. Called only by an explicit CLI command or tests."""
    db = get_db()
    db.executescript(Path(__file__).with_name("schema.sql").read_text())
    for user_id, username, role in [(1,"alice","student"),(2,"bob","student"),
                                   (3,"sam","staff"),(4,"ada","admin")]:
        db.execute("INSERT INTO users (id, username, password_hash, role) VALUES (?, ?, ?, ?)",
                   (user_id, username, ph.hash("Learning-Portal-2026!"), role))

    db.commit()  # INSERT/UPDATE changes persist only when we commit them.

@app.cli.command("init-db")
def init_db_command():
    """Delete this lab's data and recreate the four demonstration accounts."""
    init_db()
    print("Lab database reset. Fictional users: alice, bob, sam, ada.")

# 3. USER: Flask-Login needs an object with an id and authentication properties.
class User(UserMixin):
    def __init__(self, row):
        self.id = row["id"]
        self.username = row["username"]
        self.role = row["role"]

@login_manager.user_loader
def load_user(user_id):
    # Flask-Login reads the signed cookie's user id. Roles come from the DB.
    row = get_db().execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    return User(row) if row else None

# 4. SECURITY FUNCTIONS: the focused student work is labelled below.
def hash_password(password):
    # TASK B1-A: return a password hash, never the original password.
    return ph.hash(password)

def verify_password(stored_hash, password):
    # TASK B1-B: verify() returns True or raises a verification exception.
    try:
        return ph.verify(stored_hash, password)
    except (VerificationError, InvalidHashError):
        return False

def role_required(*allowed_roles):
    """Wrap a route: authenticate first, then check an explicit allow-list."""
    def decorate(view):
        @wraps(view)  # Preserve the route's name for Flask and url_for().
        @login_required
        def wrapped(*args, **kwargs):
            # TASK B1-D: a hidden link does not enforce this decision.
            # Deliberately incomplete: logged-in users currently pass this check.
            # TASK B1-D: deny any role outside allowed_roles with abort(403).
            return view(*args, **kwargs)
        return wrapped
    return decorate


csrf = CSRFProtect(app)  # Validates state-changing requests before routes run.

@app.after_request
def prevent_caching(response):
    response.headers["Cache-Control"] = "no-store"
    return response

# 5. ROUTES: GET displays a page. POST processes submitted form fields.
@app.get("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        # Preserve spaces in passwords; normalise Unicode consistently at login.
        password = unicodedata.normalize("NFC", request.form.get("password", ""))
        if not re.fullmatch(r"[a-z0-9_]{3,30}", username) or not 15 <= len(password) <= 128:
            return render_template("register.html", error="Use a 3–30 character username (a-z, 0-9, _) and a 15–128 character password."), 400
        try:
            password_hash = hash_password(password)
        except NotImplementedError:
            return render_template("register.html", error="Complete TASK B1-A before registering."), 501
        db = get_db()
        try:
            # TASK B1-C: SQL placeholders separate data from SQL instructions.
            # The role is assigned here. Ignore any role sent by the browser.
            db.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                       (username, password_hash, "student"))
            db.commit()
        except sqlite3.IntegrityError:
            db.rollback()
            return render_template("register.html", error="That username is unavailable."), 409
        flash("Account created. You can now log in.")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = unicodedata.normalize("NFC", request.form.get("password", ""))
        row = get_db().execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        # Dummy verification reduces the obvious timing difference for unknown users.
        stored_hash = row["password_hash"] if row else DUMMY_HASH
        valid = len(password) <= 128 and verify_password(stored_hash, password)
        if row is not None and valid:
            if ph.check_needs_rehash(row["password_hash"]):
                get_db().execute("UPDATE users SET password_hash = ? WHERE id = ?",
                                 (ph.hash(password), row["id"]))
                get_db().commit()
            # LOGIN_SESSION
            session.clear()  # Remove pre-login state, including the old CSRF token.
            login_user(User(row), remember=False)
            # Avoid an open redirect: always go to our own account page.
            return redirect(url_for("account"))
        return render_template("login.html", error="Invalid username or password."), 401
    return render_template("login.html")

@app.get("/account")
@login_required
def account():
    # ACCOUNT_BODY
    return render_template("account.html")

@app.get("/staff")
@role_required("staff")
def staff_area():
    return render_template("area.html", title="Staff area", message="Teaching staff workspace. Administrators have no automatic access.")

@app.get("/admin")
@role_required("admin")
def admin_area():
    # Read-only overview. Changing roles is outside this lab's scope.
    users = get_db().execute("SELECT username, role FROM users ORDER BY id").fetchall()
    return render_template("admin.html", users=users)

@app.post("/logout")
@login_required
def logout():
    # LOGOUT_SESSION
    logout_user()
    session.clear()
    return redirect(url_for("login"))
