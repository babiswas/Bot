from app.models.dbutil import db
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from app.models.bot_models import Bot
from app.models.prime_models import Prime

bot=db.Table('bots',db.Column('user_id',db.Integer,db.ForeignKey('users.id')),db.Column('bot_id',db.Integer,db.ForeignKey('mybot.id')))


class Account(db.Model):
        __tablename__='accounts'
        id=db.Column(db.Integer,primary_key=True,autoincrement=True)
        name=db.Column(db.String(200),nullable=False)
        email=db.Column(db.String(200),unique=True)
        user=db.relationship('User',backref='owner',uselist=False)
        prime=db.relationship('Prime',backref='primeowner',uselist=False)
        box=db.relationship('Box',backref='boxowner',uselist=False)

        def __init__(self,name,email):
            self.name=name
            self.email=email


        def __str__(self):
            return f"{self.name}"


class User(db.Model):
        __tablename__='users'
        id=db.Column(db.Integer,primary_key=True,autoincrement=True)
        username=db.Column(db.String(200),unique=True)
        email=db.Column(db.String(200),nullable=False)
        firstname=db.Column(db.String(200),nullable=False)
        lastname=db.Column(db.String(200),nullable=False)
        password=db.Column(db.String(200))
        is_active=db.Column(db.Boolean,nullable=False)
        mybots=db.relationship('Bot',secondary=bot,backref=db.backref('addbot',lazy='dynamic'))
        account_id=db.Column(db.Integer,db.ForeignKey('accounts.id'))
        

        
        def __init__(self,username,email,firstname,lastname,password,accountId,is_active):
            self.firstname=firstname
            self.lastname=lastname
            self.email=email
            self.username=username
            self.password=generate_password_hash(password)
            self.account_id=accountId
            self.is_active=is_active

        def check_password(self,password):
            return check_password_hash(self.password,password)

        def __str__(self):
            return f"{self.username}"


