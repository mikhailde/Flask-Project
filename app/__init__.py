from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_restful import Api
from flask_jwt_extended import JWTManager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
jwt = JWTManager(app)
api = Api(app)

api.init_app(app)

from app.models import User
from app import admin_routes, auth_routes, main_routes, models, api_routes

with app.app_context():
    db.create_all()

    def create_admin():
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(username='admin', email='admin@example.com', is_admin=True)
            admin_user.set_password('admin_password')
            db.session.add(admin_user)
            db.session.commit()

    create_admin()


@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))
