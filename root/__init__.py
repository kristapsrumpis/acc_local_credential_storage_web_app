from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# create flask app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "there-will-be-secret-key"

# create db
db = SQLAlchemy()

# initialize flask login menager
login_manager = LoginManager(app)
login_manager.login_view = "login"  # ignore type:


# importe routes
from root.routes import home_bp

# register routes
app.register_blueprint(home_bp)

# initialize db
db.init_app(app)


# migrations db
migrate = Migrate(app, db)


# import user model from models for user loader function\
from root.models import User

# user loader function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
