from app.models.dbutil import db
from datetime import datetime


class Task(db.Model):
        __tablename__="mytask"
        id=db.Column(db.Integer,primary_key=True,autoincrement=True)
        datecreated=db.Column(db.DateTime(),nullable=False)
        status=db.Column(db.Boolean,nullable=False)
        botid=db.Column(db.Integer,nullable=False)
        created_by=db.Column(db.Integer,nullable=False)

        def __init__(self,botid,userid):
            self.datecreated=datetime.utcnow().isoformat()
            self.status=False
            self.botid=botid
            self.created_by=userid

        def __str__(self):
            return f"{self.id}"