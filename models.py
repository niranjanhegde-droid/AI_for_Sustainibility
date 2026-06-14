from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

class Complaint(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200))

    description = db.Column(db.Text)

    category = db.Column(db.String(50))

    priority = db.Column(db.String(50))

    status = db.Column(
        db.String(50),
        default="Open"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


class SustainabilityScore(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    overall_score = db.Column(db.Integer)

    energy_score = db.Column(db.Integer)

    water_score = db.Column(db.Integer)

    waste_score = db.Column(db.Integer)

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )