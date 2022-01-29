from app.routes.blueprint import read
from app.models.dbutil import db
from app.models.bot_models import Bot, Bot_Content,Bot_View
from app.models.user_models import User,bot
from flask import request,redirect,render_template,url_for,session,jsonify
from app.forms.form import AccountForm,RegisterForm
from app.path_settings import content_path
from os.path import join,isfile
from datetime import datetime
from flask import flash
import os



@read.route('/home',methods=["GET"])
def home():
    return render_template("home.html")


@read.route('/logout',methods=["GET"])
def logout():
    session.clear()
    flash("You have logged out sucessfully")
    return redirect(url_for('add.login'))


@read.route('/user/<int:userid>/bots',methods=["GET"])
def my_bots(userid):
        print("Display userid")
        print(userid)
        user=User.query.get(userid)
        bots=Bot.query.join(bot).filter(bot.c.bot_id==Bot.id).filter(bot.c.user_id==userid).all()
        print(bots)
        if not bots:
            flash("You haven't subscribed any bots")
        return render_template("subscribedbots.html",bots=bots,user=user)


@read.route('/mybots/<int:userid>',methods=["GET"])
def get_bots(userid):
        user=User.query.get(userid)
        bots=Bot.query.join(bot).filter(bot.c.bot_id==Bot.id).filter(bot.c.user_id==userid).all()
        mybots=list()
        for b in bots:
            mybots.append({"botid":b.id,"url":b.url,"description":b.description,"name":b.name,"pic":b.bot_pic})
        return jsonify(mybots)


@read.route('/userfiles/<int:userid>',methods=["GET"])
def get_users_file(userid):
    user=User.query.get(userid)
    filepath=join(content_path,user.username)
    print(filepath)
    files=[join(filepath,f) for f in os.listdir(filepath) if isfile(join(filepath,f))]
    print(files)
    myfiles=[{"filename":str(path),"datemodified":datetime.fromtimestamp(os.path.getmtime(path)),"datemodified":datetime.fromtimestamp(os.path.getctime(path))} for path in files]
    return jsonify(myfiles)


@read.route('/userHome',methods=["GET"])
def get_user_home():
    if session["logged_in"]==True:
        user=User.query.get(session["userid"])
        return render_template("userhome.html",user=user)
    else:
        flash("You are not logged in")
        return redirect(url_for('add.login'))

@read.route('/subscribedBot/<int:botid>',methods=["GET"])
def get_subscribed_bot_data(botid):
    if session["logged_in"]==True:
        user=User.query.get(session["userid"])
        if user:
            bots=Bot.query.join(bot).filter(bot.c.bot_id==botid).filter(bot.c.user_id==user.id).all()
            mybots=[bot.id for bot in bots]
            if botid in mybots:
                yourbot=Bot.query.get(botid)
                botview=Bot_View.query.filter_by(bot_id=yourbot.id).first()
                botcontent=Bot_Content.query.filter_by(bot_id=yourbot.id).first()
                return render_template("subscribedbotdetail.html",bot=yourbot,botview=botview,botcontent=botcontent)
        else:
            flash("You haven't subscribed the bot")
            return redirect(url_for('read.get_user_home'))
    else:
        return redirect(url_for('add.login'))

