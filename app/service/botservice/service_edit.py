from app.routes.blueprint import edit
from app.models.dbutil import db
from app.models.bot_models import Bot_Content,Bot_View
from flask import request


@edit.route('/updateBot/<int:botid>',methods=["POST"])
def update_bot_content(botid):
        data=request.get_json()
        botupdate=Bot_Content.query.filter_by(botid=botid).first()
        botupdate.etag=data["etag"]
        db.session.commit()
        return "success"


@edit.route('/updateView/<int:botid>',methods=["POST"])
def update_view(botid):
        botview=Bot_View.query.filter_by(bot_id=botid).first()
        botview.view=botview.view+1
        db.session.commit()
        return "success"




