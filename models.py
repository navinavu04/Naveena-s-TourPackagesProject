from datetime import datetime
from extensions import db  

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Vendor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

packages = db.relationship('Package', backref='vendor', lazy=True)

class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'), nullable=False)
    image = db.Column(db.String(100)) 

from datetime import datetime
from extensions import db

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    package_id = db.Column(db.Integer, db.ForeignKey('package.id'), nullable=False)
    date_booked = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('bookings', lazy=True))
    package = db.relationship('Package', backref=db.backref('bookings', lazy=True))

    def __repr__(self):
        return f'<Vendor {self.username}>'
