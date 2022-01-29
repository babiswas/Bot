from app.routes.blueprint import add
from app.models.dbutil import db
from app.models.bot_models import Bot,Bot_Content,Bot_View
from flask import request,redirect,render_template,url_for
from app.forms.form import BotForm
from app.path_settings import bot_path
import feedparser
import os


@add.route('/addBot',methods=["POST","GET"])
def add_bot():
        botpicpath=""
        form=BotForm(request.form)
        if request.method=="POST" and form.validate:
            url=request.form.get("url")
            botname=request.form.get("botname")
            description=request.form.get("description")
            filepath=os.path.join(bot_path,botname)
            print(filepath)
            if not os.path.exists(filepath):
                os.mkdir(filepath)
            uploaded_file=request.files['file']
            if uploaded_file.filename!='':
               botpicpath=os.path.join(filepath,uploaded_file.filename)
               uploaded_file.save(botpicpath)
            bot=Bot(url,botname,description,uploaded_file.filename)
            db.session.add(bot)
            db.session.commit()
            feed=feedparser.parse(url)
            content=Bot_Content(feed.etag,bot.id)
            botview=Bot_View(bot.id)
            db.session.add(botview)
            db.session.add(content)
            db.session.commit()
            return redirect(url_for("read.bot_list"))
        return render_template("addbot.html",form=form)











