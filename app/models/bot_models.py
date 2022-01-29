from app.models.dbutil import db


class Bot(db.Model):
        __tablename__="mybot"
        id=db.Column(db.Integer,primary_key=True,autoincrement=True)
        url=db.Column(db.String(200),nullable=False)
        botname=db.Column(db.String(200),nullable=False,unique=True)
        description=db.Column(db.String(200),nullable=False)
        bot_pic=db.Column(db.String(200),nullable=False)
        content=db.relationship('Bot_Content',backref='botcontent',uselist=False)
        botview=db.relationship('Bot_View',backref='botview',uselist=False)

        def __init__(self,url,botname,description,botpic):
            self.url=url
            self.botname=botname
            self.description=description
            self.bot_pic=botpic

        def __str__(self):  
            return f"{self.botname}"


class Bot_Content(db.Model):
        __tablename__="botupdate"
        id=db.Column(db.Integer,primary_key=True,autoincrement=True)
        etag=db.Column(db.String(200),nullable=False)
        bot_id=db.Column(db.Integer,db.ForeignKey('mybot.id'))
        

        def __init__(self,etag,botid):
            self.etag=etag
            self.bot_id=botid
        
        def __str__(self):
            return f"{self.etag}"


class Bot_View(db.Model):
    __tablename__="botview"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    view=db.Column(db.Integer,nullable=False)
    bot_id=db.Column(db.Integer,db.ForeignKey('mybot.id'))


    def __init__(self,botid):
        self.view=0
        self.bot_id=botid

    def __str__(self):
        return f"{self.view}"









