from app.routes.blueprint import myhome
from flask import render_template
from app.models.dbutil import db
from app.models.bot_models import Bot,Bot_View
from flask import session
from sqlalchemy import text

@myhome.route("",methods=["GET"])
def landing_page():
   sql=text('select bot.id,bot.botname,bot.description,bot.bot_pic,botv.view from mybot as bot join botview as botv on (bot.id=botv.bot_id) order by view desc limit 5')
   results=db.session.execute(sql)
   if "logged_in" not in session:
      session["logged_in"]=False
   print(session["logged_in"])
   return render_template("base.html",results=results,loggedin=session["logged_in"])