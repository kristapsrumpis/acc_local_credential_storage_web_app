from flask import Blueprint, redirect, render_template, request, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from root import db
from root.models import AccountCredentials, User

home_bp = Blueprint("home", __name__)


@home_bp.route("/", methods=["GET"])
@login_required
def home():
    title = "ACC Credentials"
    data = AccountCredentials.query.all()
    return render_template("home.html", title=title, data=data)


@home_bp.route("/add-credenials", methods=["POST", "GET"])
@login_required
def add_credentials():
    title = "ADD Credentials"
    if request.method == "POST":
        email = request.form["email"]
        account = request.form["account"]
        password = request.form["password"]
        AccCredentials = accountCredentials(email=email,  account=account,  password=password)

        db.session.add(AccCredentials)
        db.session.commit()
        return redirect(url_for("home.home"))
    else:
        return render_template("add-account.html", title=title)


@home_bp.route("/delete-record/<int:id>", methods=["POST"])
@login_required
def delete_record(id):
    if request.method == "POST":
        credential = AccountCredentials.query.get_or_404(id)
        db.session.delete(credential)
        db.session.commit()
        return redirect(url_for("home.home"))
    else:
        return redirect(url_for("home.home"))


@home_bp.route("/edite-record/<int:id>", methods=["GET", "POST"])
@login_required
def edite_record(id):
    title = "EDITE RECORD"
    credential = AccountCredentials.query.get_or_404(id)
    if request.method == "POST":
        credential.mail = request.form["email"]
        credential.account = request.form["account"]
        credential.password = request.form["password"]
        db.session.commit()
        return redirect(url_for("home.home"))

    return render_template("edite.html", title=title, credential=credential)


@home_bp.route("/login", methods=["GET", "POST"])
def login():
    title = "Log In"
    if request.method == "POST":
        email = request.form.get('email')
        password1 = request.form.get('password1')


        # validate form input to prevent emty
        if not email or not password1:
            if not email:
                flash("Missing email", "danger")
            if not password1:
                flash("Missing password", "danger")
            return redirect(url_for("home.login"))


        # cheks if user exist
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Uses do not exist!", "danger")
            return redirect(url_for("home.login"))


        # validate password
        if not check_password_hash(user.password_hash, password1):
            flash("Incorrect password", "danger")
            return redirect(url_for("home.login"))


        # login succesful
        del user.password_hash
        login_user(user)
        flash("Logged in successfully", "success")
        return redirect(url_for("home.home"))

        
    return render_template("login.html", title=title)


@home_bp.route("/register", methods=["GET", "POST"])
def register():
    title = "Register"
    if request.method == "POST":
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        

        # validate if user input exist
        if not email or not password1 or not password2:
            if not email:
                flash("Email not provaded", "danger")
            if not password1:
                flash("Pasdword not provaded", "danger")
            if not password2:
                flash("Password confirmation not provaded", "danger")
            return redirect(url_for("home.register"))


        # chek if email is not existing alredy in db 
        if User.query.filter_by(email=email).first():
            flash("Email alredy is taken! chouse different!", 'danger')
            return redirect(url_for("home.register"))


        # calidate if password1 and pasword2 maches
        if password1 != password2:
            flash("Passwords do not match", "danger")
            return redirect(url_for("home.register"))

        
        # hash password
        password_hash = generate_password_hash(password1, method="pbkdf2:sha256")
        

        # Add user to db
        user = User(email=email, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        flash("Account ssuccesfuly created", "success")
        return redirect(url_for("home.login"))

        
    return render_template("register.html", title=title)


@home_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out", "success")
    return redirect(url_for("home.login"))
