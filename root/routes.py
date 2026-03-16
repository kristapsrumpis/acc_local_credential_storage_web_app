from flask import Blueprint, redirect, render_template, request, url_for

from root import db
from root.modules import AccountCredentials

home_bp = Blueprint("home", __name__)


@home_bp.route("/", methods=["GET"])
def home():
    title = "ACC Credentials"
    data = AccountCredentials.query.all()
    return render_template("home.html", title=title, data=data)


@home_bp.route("/add-credenials", methods=["POST", "GET"])
def add_credentials():
    title = "ADD Credentials"
    if request.method == "POST":
        email = request.form["email"]
        account = request.form["account"]
        password = request.form["password"]
        AccCredentials = accountCredentials(email=email,  account=account,  password=password)

        db.session.add(AccCredentials)
        db.session.commit()
        return redirect("/")
    else:
        return render_template("add-account.html", title=title)


@home_bp.route("/delete-record/<int:id>", methods=["POST"])
def delete_record(id):
    if request.method == "POST":
        credential = AccountCredentials.query.get_or_404(id)
        db.session.delete(credential)
        db.session.commit()
        return redirect("/")
    else:
        return redirect("/")


@home_bp.route("/edite-record/<int:id>", methods=["GET", "POST"])
def edite_record(id):
    title = "EDITE RECORD"
    credential = AccountCredentials.query.get_or_404(id)
    if request.method == "POST":
        credential.mail = request.form["email"]
        credential.account = request.form["account"]
        credential.password = request.form["password"]
        db.session.commit()
        return redirect("/")

    return render_template("edite.html", title=title, credential=credential)


@home_bp.route("/login", methods=["GET", "POST"])
def loging():
    title = "Log In"
    if request.method == "POST":
        email = request.form.get('email')
        password1 = request.form.get('password1')
        print(email,password1)
    return render_template("login.html", title=title)
