"""Tagebbbuch prototype: session login and entries held in one process."""

from dataclasses import dataclass, field
from datetime import datetime
import json
import os
from pathlib import Path
import secrets

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session, url_for

load_dotenv()

if os.getenv("WEBSITE_SITE_NAME") and not all(
    os.getenv(name) for name in ("SECRET_KEY", "PASSWORD")
):
    raise RuntimeError(
        "Azure App Settings PASSWORD und SECRET_KEY müssen gesetzt sein."
    )

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.getenv("SECRET_KEY") or secrets.token_hex(32),
    PASSWORD=os.getenv("PASSWORD"),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=bool(os.getenv("WEBSITE_SITE_NAME")),
    MAX_CONTENT_LENGTH=64 * 1024,
)
entries = []
HAPPINESS_VALUES = ("", "😃", "😐", "😞")
MAX_ENTRY_LENGTH = 5000
build_info_path = Path(__file__).with_name("build-info.json")
BUILD_REVISION = (
    json.loads(build_info_path.read_text(encoding="utf-8"))["revision"]
    if build_info_path.exists()
    else "local"
)


@dataclass
class Entry:
    content: str
    happiness: str = ""
    timestamp: datetime = field(default_factory=datetime.now)


@app.route("/")
def index():
    visible_entries = entries if session.get("logged_in") else []
    return render_template("index.html", entries=visible_entries)


@app.route("/healthz")
def health():
    return {"status": "ok", "revision": BUILD_REVISION}


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_password = request.form.get("password", "")
        password = app.config["PASSWORD"]
        if password and secrets.compare_digest(
            user_password.encode("utf-8"), password.encode("utf-8")
        ):
            session.clear()
            session["logged_in"] = True
            flash("Erfolgreich angemeldet.", "success")
            return redirect(url_for("index"))
        flash("Falsches Passwort. Bitte erneut versuchen.", "error")
    return render_template("login.html")


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("Erfolgreich abgemeldet.", "success")
    return redirect(url_for("index"))


@app.route("/add_entry", methods=["POST"])
def add_entry():
    if not session.get("logged_in"):
        flash("Bitte zuerst anmelden.", "error")
        return redirect(url_for("login"))

    content = request.form.get("content", "").strip()
    happiness = request.form.get("happiness", "")
    if not content or len(content) > MAX_ENTRY_LENGTH:
        flash("Ein Eintrag muss zwischen 1 und 5000 Zeichen enthalten.", "error")
    elif happiness not in HAPPINESS_VALUES:
        flash("Bitte eine der angebotenen Stimmungen auswählen.", "error")
    else:
        entries.append(Entry(content=content, happiness=happiness))
        flash("Eintrag gespeichert.", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0")
