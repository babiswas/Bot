from app.routes.blueprint import add,edit,read,myhome
from app.models.dbutil import db
from app.models.bot_models import Bot,Bot_Content
from app.models.task_models import Task
from app.models.user_models import User
from app.models.prime_models import Prime
from flask import redirect,render_template,url_for,session
from app.path_settings import content_path
from requests import get,post
import csv
import feedparser
import os.path
import os
from datetime import datetime,timedelta
import time
import random


@read.route('/tasklist',methods=["GET"])
def get_tasklist():
    if session["logged_in"]==True:
        task=Task.query.filter_by(created_by=session["userid"])
        return render_template("tasklist.html",task=task)
    else:
        return redirect(url_for('add.login'))



@read.route('/botread/<int:botid>',methods=["GET"])
def read_bot(botid):
        print("Bot Reading")
        dt=datetime.utcnow()
        datemodified=dt-timedelta(days=2)
        datemodified=datemodified.isoformat().split('.')[0]+'.000Z'
        ms=dt.microsecond
        print("Micosecond")
        if session["logged_in"]==True:
            user=User.query.get(session["userid"])
            bot=Bot.query.get(botid)
            task=Task(bot.id,user.id)
            db.session.add(task)
            db.session.commit()
            print("Task Commited")
            content=Bot_Content.query.filter_by(bot_id=botid).first()
            feed=feedparser.parse(bot.url)
            print("Etag")
            print(feed.etag)
            if feed.etag!=content.etag:
                print("feed block")
                response=get("http://127.0.0.1:5000/read/userfiles/"+str(session["userid"]))
                if response.status_code!=200:
                    raise Exception
                data=response.json()
                if len(data)!=0:
                    path1=os.path.join(os.path.join(content_path,user.username),"job_aid.csv")
                    path2=os.path.join(os.path.join(content_path,user.username),"job_aid_version.csv")
                    if os.path.exists(path1) and os.path.exists(path2):
                        with open(path1,'a',newline='') as file1,open(path2,'a',newline='') as file2:
                            writer1=csv.DictWriter(file1,fieldnames=["id","jobAidName","description","state","lastModifiedDate","visibility"])
                            writer2=csv.DictWriter(file2,fieldnames=["jobAidId","jobAidVersion","contentType","dateCreated","duration","desiredDuration","contentUrl"])
                            for obj in feed.entries:
                                ms=ms+1
                                writer2.writerow({"jobAidId":ms,"jobAidVersion":8,"contentType":"HYPERLINK","dateCreated":datetime.utcnow().isoformat().split('.')[0]+'.000Z.',"duration":60,"desiredDuration":30,"contentUrl":obj['links'][0]['href']})
                                writer1.writerow({"id":ms,"jobAidName":"Autobot_"+bot.botname,"description":"mybot","state":"Published","lastModifiedDate":datetime.utcnow().isoformat().split('.')[0]+'.000Z.',"visibility":"Shared"})
                            task.status=True
                            db.session.commit()
                        return redirect(url_for('read.get_tasklist'))         
                else:
                    print("Else Block")
                    path1=os.path.join(os.path.join(content_path,user.username),"job_aid.csv")
                    path2=os.path.join(os.path.join(content_path,user.username),"job_aid_version.csv")
                    with open(path1,'w',newline='') as file1,open(path2,'w',newline='') as file2:
                            writer1=csv.DictWriter(file1,fieldnames=["id","jobAidName","description","state","lastModifiedDate","visibility"])
                            writer2=csv.DictWriter(file2,fieldnames=["jobAidId","jobAidVersion","contentType","dateCreated","duration","desiredDuration","contentUrl"])
                            writer1.writeheader()
                            writer2.writeheader()
                            for obj in feed.entries:
                                ms=ms+1
                                writer2.writerow({"jobAidId":ms,"jobAidVersion":8,"contentType":"HYPERLINK","dateCreated":datemodified,"duration":60,"desiredDuration":30,"contentUrl":obj['links'][0]['href']})
                                writer1.writerow({"id":ms,"jobAidName":"Autobot_"+bot.botname,"description":"mybot","state":"Published","lastModifiedDate":datemodified,"visibility":"Shared"})
                            task.status=True
                            db.session.commit()
                    return redirect(url_for('read.get_tasklist'))
                task.status=False
                db.session.commit()
                return redirect(url_for('read.get_tasklist'))
            else:
                return redirect(url_for('read.get_subscribed_bot_data',botid=bot.id))
        else:
            return redirect(url_for('add.login'))


@read.route('/migrate',methods=["GET"])
def migrate_csv():
    if session["logged_in"]==True:
        prime=Prime.query.filter_by(account_id=session["accountId"]).first()
        print(prime.id)
        token=post(prime.server+"oauth/token/refresh",params={"client_id":prime.clientid,"client_secret":prime.clientsecret,"refresh_token":prime.refreshtoken},headers={"Content-type":"application/x-www-form-urlencoded"})
        if token.status_code!=200:
            raise Exception
        access_token=token.json()["access_token"]
        cansync=get(prime.server+"primeapi/v2/bulkimport/cansync",headers={"Authorization":"oauth "+access_token})
        if cansync.status_code!=200:
            raise Exception
        if cansync.json()["status"]=="OK" and cansync.json()["title"]=="BULKIMPORT_CAN_SYNC_NOW" and cansync.json()["source"]["info"]=="Yes" :
            migrate=post(prime.server+"primeapi/v2/bulkimport/startrun",headers={"Authorization":"oauth "+access_token})
            if migrate.status_code!=200:
                raise Exception
            else:
                if migrate.json()["status"]=="OK" and migrate.json()["title"]=="BULKIMPORT_RUN_INITIATED_SUCCESSFULLY":
                    return redirect(url_for('read.get_tasklist'))
        else:
            raise Exception
    else:
        return redirect(url_for('add.login'))


