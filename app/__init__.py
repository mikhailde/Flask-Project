from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Инициализация базы данных и создание пользователя администратора по умолчанию
from app.models import User

with app.app_context():
    db.create_all()

    # Проверяем, существует ли пользователь с ролью админа
    admin_user = User.query.filter_by(username='admin').first()

    # Если нет, создаем пользователя с ролью админа
    if not admin_user:
        admin_user = User(username='admin', email='admin@example.com', is_admin=True)
        admin_user.set_password('admin_password')
        db.session.add(admin_user)
        db.session.commit()

from app import routes, models

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))
