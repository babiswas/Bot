from app.models.dbutil import db

class Box(db.Model):
        __tablename__="boxconfig"
        id=db.Column(db.Integer,primary_key=True,autoincrement=True)
        appname=db.Column(db.String(200),nullable=False)
        clientid=db.Column(db.String(200),nullable=False)
        clientsecret=db.Column(db.String(200),nullable=False)
        refreshtoken=db.Column(db.String(200),nullable=False)
        accesstoken=db.Column(db.String(200),nullable=False)
        folderid=db.Column(db.String(200),nullable=False)
        account_id=db.Column(db.Integer,db.ForeignKey('accounts.id'))

        def __init__(self,appname,clientid,clientsecret,refreshtoken,accountid,accesstoken,folderid):
                self.appname=appname
                self.clientid=clientid
                self.clientsecret=clientsecret
                self.refreshtoken=refreshtoken
                self.account_id=accountid
                self.accesstoken=accesstoken
                self.folderid=folderid

        def __str__(self):
            return f"{self.appname}"


class Box_Upload(db.Model):
        __tablename__="boxupload"
        id=db.Column(db.Integer,primary_key=True,autoincrement=True)
        status=db.Column(db.Boolean,nullable=False)
        datecreated=db.Column(db.DateTime(),nullable=False)
        userid=db.Column(db.Integer,nullable=False)


        def __init__(self,status,datecreated,userid):
                self.status=status
                self.datecreated=datecreated
                self.userid=userid

        def __str__(self):
                return f"{self.id} & {self.status}"

