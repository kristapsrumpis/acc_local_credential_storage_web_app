from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# create flask app 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# create db 
db = SQLAlchemy()


# importe routes
from root.routes import home_bp


# register routes
app.register_blueprint(home_bp)

# initialize db
db.init_app(app)


# migrations db
migrate = Migrate(app,db)