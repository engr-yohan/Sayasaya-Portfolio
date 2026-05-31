import os
import re
import smtplib
from email.mime.text import MIMEText

from flask import Flask, render_template, request

app = Flask(__name__)

CONTACT_TO_EMAIL = "villarantedenver@gmail.com"
CONTACT_SMTP_HOST = os.environ.get("CONTACT_SMTP_HOST", "smtp.gmail.com")
CONTACT_SMTP_PORT = int(os.environ.get("CONTACT_SMTP_PORT", "587"))
CONTACT_SMTP_USERNAME = os.environ.get("CONTACT_SMTP_USERNAME", "")
CONTACT_SMTP_PASSWORD = os.environ.get("CONTACT_SMTP_PASSWORD", "")
CONTACT_SMTP_USE_TLS = os.environ.get("CONTACT_SMTP_USE_TLS", "true").lower() != "false"
CONTACT_FROM_EMAIL = os.environ.get("CONTACT_FROM_EMAIL", CONTACT_SMTP_USERNAME or CONTACT_TO_EMAIL)

PERSON = {
    "name": "Denver Villarante Sayasaya",
    "title": "Future Data Engineer",
    "bio": "Computer Engineering student at the Polytechnic University of the Philippines (Main), building data-driven systems to analyze and uplift communities.",
}

NAV_ITEMS = [
    {"label": "Home", "endpoint": "home"},
    {"label": "Projects", "endpoint": "projects"},
    {"label": "Contacts", "endpoint": "contact"},
]

PROJECTS = [
    {
        "title": "Budget tracker",
        "description": "Designed and implemented an automated ETL pipeline using Python and PySpark to ingest, clean, and transform semi-structured personal financial data.",
        "tags": ["Python"],
        "code_url": "https://github.com/",
    },
    {
        "title": "Address Book 4",
        "description": "Developed a structured relational database management system using Python and SQLite to manage, organize, and query complex multi-attribute contact datasets.",
        "tags": ["Python", "SQL"],
        "code_url": "https://github.com/engr-yohan/G4-Project-PLD",
    },
    {
        "title": "Sorting Algorithms",
        "description": "Engineered custom sorting and data-filtering algorithms in Python to handle server-side data reordering and optimization tasks across large datasets.",
        "tags": ["HTML", "Python", "CSS"],
        "code_url": "https://github.com/engr-yohan/g6_qdq",
    },
]


def send_contact_email(sender_name, sender_email, message):
    subject = f"Portfolio contact from {sender_name}"
    body = (
        f"Name: {sender_name}\n"
        f"Email: {sender_email}\n\n"
        f"Message:\n{message}"
    )

    email_message = MIMEText(body, "plain", "utf-8")
    email_message["Subject"] = subject
    email_message["From"] = CONTACT_FROM_EMAIL
    email_message["To"] = CONTACT_TO_EMAIL
    email_message["Reply-To"] = sender_email

    with smtplib.SMTP(CONTACT_SMTP_HOST, CONTACT_SMTP_PORT, timeout=20) as smtp_server:
        if CONTACT_SMTP_USE_TLS:
            smtp_server.starttls()
        if CONTACT_SMTP_USERNAME and CONTACT_SMTP_PASSWORD:
            smtp_server.login(CONTACT_SMTP_USERNAME, CONTACT_SMTP_PASSWORD)
        smtp_server.send_message(email_message)

@app.route("/")
def home():
    return render_template(
        "index.html",
        nav_items=NAV_ITEMS,
        active_page="home",
        person=PERSON,
        email="hello@example.com",
    )


@app.route("/projects")
def projects():
    return render_template(
        "projects.html",
        nav_items=NAV_ITEMS,
        active_page="projects",
        projects=PROJECTS,
        person=PERSON,
    )


@app.route("/contact", methods=["GET", "POST"])
def contact():
    success_message = None
    error_message = None
    form_name = ""
    form_email = ""
    form_message = ""

    if request.method == "POST":
        form_name = request.form.get("name", "").strip()
        form_email = request.form.get("email", "").strip()
        form_message = request.form.get("message", "").strip()

        if not form_name or not form_email or not form_message:
            error_message = "Please fill in your name, email, and message."
        elif not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", form_email):
            error_message = "Please enter a valid email address."
        else:
            try:
                send_contact_email(form_name, form_email, form_message)
                success_message = "Your message was sent successfully."
                form_name = ""
                form_email = ""
                form_message = ""
            except Exception:
                error_message = "We could not send your message right now. Please try again later."

    return render_template(
        "contact.html",
        nav_items=NAV_ITEMS,
        active_page="contact",
        person=PERSON,
        email=CONTACT_TO_EMAIL,
        success_message=success_message,
        error_message=error_message,
        form_name=form_name,
        form_email=form_email,
        form_message=form_message,
    )


if __name__ == "__main__":
    app.run(debug=True)
