# project/models.py
import datetime
from project import db
from werkzeug import generate_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=False, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    #presence = db.Column(db.ARRAY(WorkDay), nullable=True)

    def __init__(self, email, password, name, admin=False):
        self.email = email
        self.password = generate_password_hash(password)
        self.name = name
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    def serialize(self):
        import json

        user_dict = {}
        user_dict['email'] = self.email
        user_dict['name'] = self.name
        return json.dumps(user_dict)

    # UserMixin berisi fungsi ini semua,
    # SEHARUSNYA tanpa definisi dibawah tetap bisa jalan
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def __repr__(self):
        return '<User {0}>'.format(self.email)

# Request
# Berisi request  yang dibuat melalui API oleh perangkat IoT
# Request hanya dapat disetujui oleh admin
class Request(db.Model):
    from enum import IntEnum

    __tablename__ = "request"

    status_enum = IntEnum('Status_enum', 'UNRESPONDED GRANTED REJECTED')

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.Integer, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    updated_on = db.Column(db.DateTime, nullable=False)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    photo = db.Column(db.String(255), unique=True, nullable=True)

    def __init__(self, status=int(status_enum.UNRESPONDED), updated_by=None, photo=None):
        self.status = int(status)
        self.created_on = datetime.datetime.now()
        self.updated_on = datetime.datetime.now()
        self.updated_by = updated_by
        self.photo = photo

    def get_dict(self):
        request_dict = {}

        if (updated_by!=None):
            user = User.query.get(self.updated_by)
            request_dict['updated_by'] = user.name
        else:
            request_dict['updated_by'] = None

        request_dict['status'] = self.status
        request_dict['created_on'] = self.created_on
        request_dict['updated_on'] = self.updated_on
        request_dict['photo'] = self.photo

        return request_dict

    def update_status(self, status, updated_by):
        if status in status_enum:
            self.status = int(status)
            self.updated_by = updated_by
            self.updated_on = datetime.datetime.now()
            return True # success
        else:
            return False # unsuccessful

    def update_photo(self, photo, updated_by):
        self.photo = photo
        self.updated_by = updated_by
        self.updated_on = datetime.datetime.now()

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<Request {0}>'.format(self.id)
