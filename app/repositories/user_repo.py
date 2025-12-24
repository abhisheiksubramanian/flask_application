from app.models.user import User
from app.extensions.db import db

def find_by_username(username):
    return User.query.filter_by(username=username).first()

def save(user):
    db.session.add(user)
    db.session.commit()
