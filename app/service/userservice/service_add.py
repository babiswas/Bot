from app.routes.blueprint import add
from app.models.dbutil import db
from app.models.bot_models import Bot
from app.models.user_models import User,Account
from app.models.box_models import Box
from flask import request,redirect,render_template,url_for,session
from app.forms.form import AccountForm,RegisterForm,LoginForm
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from app.path_settings import content_path
from requests import post
from flask import flash
import os.path
import json
import os


@add.route('/account',methods=['GET','POST'])
def create_account():
    try:
        form=AccountForm(request.form)
        if request.method=='POST' and form.validate:
            name=request.form["name"]
            email=request.form["email"]
            account=Account(name,email)
            db.session.add(account)
            db.session.commit()
            return redirect(url_for('add.add_root',accountId=account.id))
        return render_template('account.html',form=form)
    except Exception as e:
        print(e)



@add.route('/root/<int:accountId>',methods=["GET","POST"])
def add_root(accountId):
    form=RegisterForm(request.form)
    account=Account.query.get(accountId)
    if request.method=="POST" and form.validate:
        firstname=request.form["firstname"]
        lastname=request.form["lastname"]
        username=request.form["username"]
        email=account.email
        password=request.form["password"]
        user=User(username,email,firstname,lastname,password,account.id,True)
        db.session.add(user)
        db.session.commit()
        user_content_path=os.path.join(content_path,user.username)
        if not os.path.exists(user_content_path):
            os.mkdir(user_content_path)
        return redirect(url_for('add.login'))
    return render_template("root.html",form=form,email=account.email)


@add.route('/login',methods=["GET","POST"])
def login():
        form=LoginForm(request.form)
        if request.method=="POST" and form.validate:
            username=request.form["username"]
            password=request.form["password"]
            user=User.query.filter_by(username=username).first()
            if user:
                    if check_password_hash(user.password,password):
                            session["accountId"]=user.account_id
                            session["userid"]=user.id
                            session["logged_in"]=True
                            box=Box.query.filter_by(account_id=user.account_id).first()
                            if box:
                                data={"grant_type":"refresh_token","client_id":box.clientid,"client_secret":box.clientsecret,"refresh_token":box.refreshtoken}
                                headers={"Content-Type":"application/vnd.api+json"}
                                res=post('https://api.box.com/oauth2/token',data=json.dumps(data),headers=headers)
                                print(res.json())
                                if res.status_code!=200:
                                    raise Exception
                                params=dict()
                                params["refresh_token"]=res.json()["refresh_token"]
                                params["access_token"]=res.json()["access_token"]
                                update_box_data=post("http://127.0.0.1:5000/edit/boxRefresh/"+str(box.id),params=params)
                                if update_box_data.status_code!=200:
                                    raise Exception
                            return redirect(url_for('read.get_user_home'))
                    else:
                        return redirect(url_for('add.login'))
        return render_template('login.html',form=form)



@add.route('/subscribe/<int:botid>/user/<int:userid>',methods=["POST"])
def subscribe(botid,userid):
    user=User.query.get(userid)
    bot=Bot.query.filter_by(id=botid).first()
    bot.addbot.append(user)
    db.session.commit()
    return "success"


@add.route('/subscribeBot/<int:botid>',methods=["GET","POST"])
def subscribe_bot(botid):
    if session["logged_in"]==True:
        obj=post("http://127.0.0.1:5000/add/subscribe/"+str(botid)+"/user/"+str(session["userid"]))
        if obj.status_code!=200:
            raise Exception
        return redirect(url_for('read.my_bots',userid=session["userid"]))
    else:
            flash("you haven't logged in")
            return redirect(url_for('add.login'))

