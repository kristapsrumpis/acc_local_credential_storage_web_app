from flask import Blueprint, render_template,request,redirect, url_for
from root.modules import accountCredentials
from root import db

home_bp = Blueprint('home', __name__)

@home_bp.route('/', methods=['GET'])
def home():
    title = 'ACC Credentials'
    data = accountCredentials.query.all()
    return render_template('home.html', title=title, data=data)


@home_bp.route('/add-credenials', methods=['POST', 'GET'])
def add_credentials():
    title = 'ADD Credentials'
    if request.method == "POST":
        email = request.form['email']
        account = request.form['account']
        password = request.form['password']
        accCredentials = accountCredentials(email=email, account=account,pasword=password )
        db.session.add(accCredentials)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('add-account.html', title=title)
        

@home_bp.route('/delete-record/<int:id>', methods=['POST'])
def delete_record(id):
    if request.method == 'POST':
        credential = accountCredentials.query.get_or_404(id)
        db.session.delete(credential)
        db.session.commit()
        return redirect('/')
    else:
        return redirect('/')
    

@home_bp.route('/edite-record/<int:id>', methods=['GET','POST'])
def edite_record(id):
    title = 'EDITE RECORD'
    credential = accountCredentials.query.get_or_404(id)
    if request.method == 'POST':
        credential.mail = request.form['email']
        credential.account = request.form['account']
        credential.pasword = request.form['password']
        db.session.commit()
        return redirect('/')
    
    return render_template('edite.html', title=title, credential=credential)


@home_bp.route('/login', methods=['GET', 'POST'])
def loging():
    title = "Log In"
    return render_template('login.html', title=title)
   