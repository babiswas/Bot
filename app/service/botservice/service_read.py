from app.routes.blueprint import read
from app.models.bot_models import Bot,Bot_Content,Bot_View
from flask import render_template,jsonify,session,request,url_for
from app.path_settings import bot_path
from requests import post


@read.route('/botList',methods=["GET"])
def bot_list():
        page=request.args.get('page',1,type=int)
        bots=Bot.query.paginate(page=page,per_page=3)
        next_url=url_for('read.bot_list',page=bots.next_num) if bots.has_next else None
        prev_url=url_for('read.bot_list',page=bots.prev_num) if bots.has_prev else None
        return render_template('botlist.html',bots=bots,next_url=next_url,prev_url=prev_url,bot_path=bot_path)

@read.route('/bot/<int:botid>',methods=["GET"])
def bot_detail(botid):
        bot=Bot.query.get(botid)
        botcontent=Bot_Content.query.filter_by(bot_id=bot.id).first()
        botview=Bot_View.query.filter_by(bot_id=bot.id).first()
        res=post("http://127.0.0.1:5000/edit/updateView/"+str(bot.id))
        if res.status_code!=200:
                raise Exception
        return render_template('botdetail.html',bot=bot,botview=botview,botcontent=botcontent)


@read.route('/botupdate/<int:botid>',methods=["GET"])
def bot_update(botid):
        bot=Bot.query.get(botid)
        botupdate=Bot_Content.query.filter_by(botid=bot.id).first()
        bot_obj=dict()
        bot_obj["botid"]=bot.id
        bot_obj["etag"]=botupdate.etag
        return jsonify(bot_obj)


@read.route('/botIds',methods=["GET"])
def get_bot_ids():
        botetags=Bot_Content.query.all()
        data=dict()
        for tag in botetags:
            data[str(tag.bot_id)]=tag.etag
        return jsonify(data)


@read.route('/botSubscriber',methods=["GET"])
def get_subscribers():
        subscriber_list=dict()
        bots=Bot.query.all()
        for bot in bots:
           subscriber_list[str(bot.id)]=[str(obj.id) for obj in bot.addbot]
        return jsonify(subscriber_list)










    




