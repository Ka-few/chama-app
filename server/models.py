from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin


db = SQLAlchemy()


membership = db.Table(
'membership',
db.Column('chama_id', db.Integer, db.ForeignKey('chama.id'), primary_key=True),
db.Column('member_id', db.Integer, db.ForeignKey('member.id'), primary_key=True)
)


class Chama(db.Model, SerializerMixin):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120), nullable=False, unique=True)
	description = db.Column(db.String(300))
	members = db.relationship('Member', secondary=membership, back_populates='chamas')
	contributions = db.relationship('Contribution', back_populates='chama', cascade='all, delete-orphan')
	serialize_rules = ('-members.chamas', '-contributions.chama')


class Member(db.Model, SerializerMixin):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120), nullable=False)
	email = db.Column(db.String(120), nullable=False, unique=True)
	phone = db.Column(db.String(20))
	chamas = db.relationship('Chama', secondary=membership, back_populates='members')
	contributions = db.relationship('Contribution', back_populates='member', cascade='all, delete-orphan')
	serialize_rules = ('-chamas.members', '-contributions.member')


class Contribution(db.Model, SerializerMixin):
	id = db.Column(db.Integer, primary_key=True)
	amount = db.Column(db.Float, nullable=False)
	date = db.Column(db.DateTime, default=datetime.utcnow)
	note = db.Column(db.String(250))
	member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
	chama_id = db.Column(db.Integer, db.ForeignKey('chama.id'), nullable=False)
	member = db.relationship('Member', back_populates='contributions')
	chama = db.relationship('Chama', back_populates='contributions')
	serialize_rules = ('-member.contributions', '-chama.contributions')