from app.models.dbutil import db


class Prime(db.Model):
   __tablename__="primeconfig"
   id=db.Column(db.Integer,primary_key=True,autoincrement=True)
   appname=db.Column(db.String(200),nullable=False)
   clientid=db.Column(db.String(200),nullable=False)
   clientsecret=db.Column(db.String(200),nullable=False)
   refreshtoken=db.Column(db.String(200),nullable=False)
   server=db.Column(db.String(300),nullable=False)
   email=db.Column(db.String(300),nullable=False)
   redirecturi=db.Column(db.String(300),nullable=False)
   primeaccount=db.Column(db.String(300),nullable=False)
   account_id=db.Column(db.Integer,db.ForeignKey('accounts.id'))

   def __init__(self,appname,clientid,clientsecret,refreshtoken,server,accountid,email,redirecturi,primeaccount):
            self.appname=appname
            self.clientid=clientid
            self.clientsecret=clientsecret
            self.refreshtoken=refreshtoken
            self.server=server
            self.account_id=accountid
            self.email=email
            self.redirecturi=redirecturi
            self.primeaccount=primeaccount

   def __str__(self):
       return f"{self.appname}"