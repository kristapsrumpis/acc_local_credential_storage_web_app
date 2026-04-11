from flask import Blueprint, redirect, render_template, request, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from root import db
from root.models import AccountCredentials, User
from root.encryption import Encription
from cryptography.fernet import Fernet


home_bp = Blueprint("home", __name__)


@home_bp.route("/", methods=["GET"])
@login_required
def home():
    title = "ACC Credentials"
    key = session.get("fernet_key")
    if not key:
        flash("Session expired. Please log in again.", "warning")
        return redirect(url_for("home.login"))
    f = Fernet(key.encode())

    data = AccountCredentials.query.filter_by(user_id=current_user.id).all()
    for item in data:
        try:
            item.password = f.decrypt(item.password).decode()
        except Exception:
            item.password = "[DECRYPTION FAILED]"

    return render_template("home.html", title=title, data=data)


@home_bp.route("/add-credenials", methods=["POST", "GET"])
@login_required
def add_credentials():
    title = "ADD Credentials"
    if request.method == "POST":
        email = request.form["email"]
        account = request.form["account"]
        password = request.form["password"]

        key = session.get("fernet_key")
        enc = Fernet(key.encode())
        enc_password = enc.encrypt(password.encode())

        AccCredentials = AccountCredentials(email=email,  account=account,  password=enc_password, user_id=current_user.id)

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
    key = session.get("fernet_key")
    if not key:
        flash("Session expired. Please log in again.", "warning")
        return redirect(url_for("home.login"))
    f = Fernet(key.encode())

    credential = AccountCredentials.query.get_or_404(id)
    credential.password = f.decrypt(credential.password).decode()

    if request.method == "POST":
        credential.mail = request.form["email"]
        credential.account = request.form["account"]
        credential.password = f.encrypt(request.form["password"].encode())
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
        enc = Encription(password1)
        del user.password_hash
        login_user(user)
        session["fernet_key"] = enc.key.decode()
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
                flash("Email not provided", "danger")
            if not password1:
                flash("Pasdword not provided", "danger")
            if not password2:
                flash("Password confirmation not provided", "danger")
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
    session.clear() 
    flash("Logged out", "success")
    return redirect(url_for("home.login"))


@home_bp.route("/account/<int:id>", methods=["GET", "POST"])
@login_required
def account(id):
    title = "Account"
    user = User.query.get(id)
    if not user:
        flash("Uses do not exist!", "danger")
        return redirect(url_for("home.login"))

    if request.method == "POST":
        email = request.form.get('email')
        if not email:
           flash("Email not provided", "danger")
           return redirect(url_for('home.account', id=user.id))
        try:
            user.email = email
            db.session.commit()
            flash("Account Updated succesfuly", 'success')
        except Encription as err:
            print(err)
            flash("Update Account Failled!", 'danger')
            return redirect(url_for('home.account', id=user.id))

        return redirect(url_for('home.home'))

    return render_template("edite-account.html", title=title, user=user)


@home_bp.route("/account/change-password/<int:id>", methods=['POST'])
@login_required
def change_password(id):
    if request.method == "POST":
        password_old = request.form.get('passwordOld')
        password_new = request.form.get('passwordNew')
        password_confirm = request.form.get('passwordConfirm')

        if not password_old or not password_new or not password_confirm:
            if not password_old:
                flash('Old password is incorrect', 'danger')
            if not password_new:
                flash('New password is provided', 'danger')
            if not password_confirm:
                flash('Password confirm is not provided', 'danger')
            return redirect(url_for('home.account', id=id))

        if password_new != password_confirm:
            flash('Password confirmation no mach new password', 'danger')
            return redirect(url_for('home.account', id=id))

        if not id:
            flash("Faill changing password", 'danger')
            return redirect(url_for('home.home'))

        user = User.query.get(id)
        if not user:
            flash('No user found!', 'danger')
            return redirect(url_for('home.home'))

        if not check_password_hash(password_old, user.password_hash):
            flash('Old password is incorrect', 'danger')
            return redirect(url_for('home.home'))

        key = session.get("fernet_key")
        if not key:
            flash('Faill changing password', 'danger')
            return redirect(url_for('home.home'))

        enc = Fernet(key.encode())
        new_key = Encription()
        enc_new = Fernet(new_key.encode())

        data = AccountCredentials.query.filter_by(user_id=current_user.id).all()
        try:
            user.password_hash = generate_password_hash(password_new, method="pbkdf2:sha256")
            for item in data:
                try:
                    item.password = enc_new.encrypt(enc.decrypt(item.password))
                except Exception as e:
                   print("Decrypt error:", e)

            db.session.commit()
            session["fernet_key"] = enc_new.key.decode()

            flash("Password changed successfully", "success")
            return redirect(url_for('home.account', id=id))
            
        except Exception as e:
            print(e)
            flash("Failled change password", 'danger')
            return redirect(url_for('home.home'))
    
    return redirect(url_for('home.home'))


    
