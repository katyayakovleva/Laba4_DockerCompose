from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80), nullable=False)
    fullAccess = db.Column(db.Boolean)

    # def __repr__(self):
    #     return {self.fullAccess}

    def get_access(self):
        return self.fullAccess