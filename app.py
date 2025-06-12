#!/usr/bin/env python3
from datetime import datetime

from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

app = Flask(__name__)

app.config["SECRET_KEY"] = "myapplication123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "momobitcoin1986@gmail.com"
app.config["MAIL_PASSWORD"] = "***"
db = SQLAlchemy(app)
mail = Mail(app)


class Form(db.Model):
    # ClassModel to create database
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(80))


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def index():
    # POST Method
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        date = request.form["date"]
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        occupation = request.form["occupation"]

        form = Form(
            first_name=first_name,
            last_name=last_name,
            email=email,
            date=date_obj,
            occupation=occupation
        )
        db.session.add(form)
        db.session.commit()

        # Send Email
        message_body = f"Thank you for your submission, {first_name}. " \
            f"Here are your data: {first_name} {last_name}" \
            f"Thanks"
        message = Message(
            subject="New form submission",
            sender=app.config["MAIL_USERNAME"],
            recipients=[email],
            body=message_body
        )
        mail.send(message)

        # Show alert
        flash(f"{first_name}, Your Form was submitted successfully", "success")

    # GET Method
    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Database creation if not exist
        app.run(debug=True, port=5001)
