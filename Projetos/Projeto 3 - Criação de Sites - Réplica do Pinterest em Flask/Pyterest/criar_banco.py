from pyterest import database, app
from pyterest.models import User, Picture

with app.app_context():
    database.create_all()
