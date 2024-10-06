# Criar a estrutura do banco de dados
from datetime import datetime, timezone
from pyterest import database, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id_user):
    return User.query.get(int(id_user))

class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False, unique=True)
    email = database.Column(database.String, nullable=False, unique=True)
    password = database.Column(database.String, nullable=False)
    pictures = database.relationship("Picture", backref='user', lazy=True)


class Picture(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    image = database.Column(database.String, default='default.png')
    date = database.Column(database.DateTime, nullable=False, default=datetime.now(timezone.utc))
    id_user = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)
