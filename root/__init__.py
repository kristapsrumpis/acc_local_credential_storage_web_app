from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login  import LoginManager


# create flask app 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# create db 
db = SQLAlchemy()

# initialize flask login menager
login_menager = LoginManager(app)
login_menager.login_view = "login"


# importe routes
from root.routes import home_bp


# register routes
app.register_blueprint(home_bp)

# initialize db
db.init_app(app)


# migrations db
migrate = Migrate(app,db)