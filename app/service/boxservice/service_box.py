from app.routes.blueprint import add,read,edit
from app.models.dbutil import db
from app.models.box_models import Box,Box_Upload
from app.models.user_models import User
from flask import request,redirect,render_template,url_for,session
from app.forms.form import BoxForm
from app.routes.blueprint import add,read,edit
from requests import post
from boxsdk import OAuth2,Client
from app.path_settings import content_path
from os.path import isfile,join
from datetime import datetime
from requests import get,post
from flask import jsonify
from flask import flash
import json
import os


@add.route('/configBox',methods=["POST","GET"])
def add_box_config():
        if session["logged_in"]==True:
                form=BoxForm(request.form)
                if request.method=="POST" and form.validate:
                    appname=request.form.get("appname")
                    clientid=request.form.get("clientid")
                    clientsecret=request.form.get("clientsecret")
                    folderid=request.form.get("folderid")
                    box=Box(appname,clientid,clientsecret,'',session["accountId"],'',folderid)
                    db.session.add(box)
                    db.session.commit()
                    return redirect(url_for('read.box_config',boxid=box.id))
                return render_template("boxconfig.html",form=form)
        else:
            return redirect(url_for('add.login'))



@read.route('/boxConfig/<int:boxid>',methods=["GET"])
def box_config(boxid):
        box=Box.query.get(boxid)
        return render_template("boxdetail.html",box=box)



@edit.route('/boxConfig/<int:boxid>',methods=["POST","GET"])
def edit_box_config(boxid):
        if session["logged_in"]==True:
            box=Box.query.get(boxid)
            form=BoxForm(obj=box)
            if request.method=="POST" and form.validate:
                    box.clientid=request.form.get("clientid")
                    box.clientsecret=request.form.get("clientsecret")
                    box.folderid=request.form.get("folderid")
                    db.session.commit()
                    return redirect(url_for('read.box_config',boxid=box.id))
            return render_template("boxconfig.html",form=form)
        else:
            return redirect(url_for('add.login'))


@read.route('/boxoauth',methods=["GET"])
def box_oauth():
        if session["logged_in"]==True:
                box=Box.query.filter_by(account_id=session["accountId"]).first()
                url="https://account.box.com/api/oauth2/authorize?"
                url+="response_type=code&"
                url+="state=authenticated&"
                url+="client_id="+box.clientid
                return redirect(url,code=302,Response=None)
        else:
                return redirect(url_for('add.login'))



@read.route('/boxtoken',methods=["GET"])
def configure_box():
    code=request.args.get("code")
    box=Box.query.filter_by(account_id=session["accountId"]).first()
    if session["logged_in"]==True:
        oauth=OAuth2(client_id=box.clientid,client_secret=box.clientsecret)
        access_token,refresh_token=oauth.authenticate(code)
        res=post("http://127.0.0.1:5000/edit/boxRefresh/"+str(box.id),params={"access_token":access_token,"refresh_token":refresh_token})
        if res.status_code!=200:
            raise Exception
        return redirect(url_for('read.box_config',boxid=box.id))
    else:
        return redirect(url_for('add.login'))


@edit.route('/boxRefresh/<int:boxid>',methods=["POST"])
def update_box_token(boxid):
    box=Box.query.get(boxid)
    access_token=request.args.get("access_token")
    refresh_token=request.args.get("refresh_token")
    box.refreshtoken=refresh_token
    box.accesstoken=access_token
    db.session.commit()
    return "success"


@read.route('/uploadBox',methods=["GET"])
def get_box_access_token():
    if session["logged_in"]==True:
        res=post('http://127.0.0.1:5000/add/uploadTask',data=json.dumps({"status":True,"datecreated":datetime.utcnow().isoformat(),"userid":session["userid"]}),headers={"Content-Type":"application/vnd.api+json"})
        if res.status_code!=200:
            raise Exception
        box=Box.query.filter_by(account_id=session["accountId"]).first()
        user=User.query.get(session["userid"])
        oauth=OAuth2(client_id=box.clientid,client_secret=box.clientsecret,access_token=box.accesstoken,refresh_token=box.refreshtoken)
        client=Client(oauth)
        items=client.folder(folder_id=box.folderid).get_items()
        for item in items:
            client.file(file_id=item.id).delete()
        filepath=os.path.join(content_path,user.username)
        files=[join(filepath,f) for f in os.listdir(filepath) if isfile(join(filepath,f))]
        for file in files:
            client.folder(box.folderid).upload(file)
        res1=post('http://127.0.0.1:5000/edit/uploadTask/'+str(res.json()["id"]),headers={"Content-Type":"application/vnd.api+json"})
        if res1.status_code!=200:
            raise Exception
        return redirect(url_for('read.box_tasklist'))
    else:
        return redirect(url_for('add.login'))


@add.route('/uploadTask',methods=["POST"])
def task_box_upload():
        print("upload box task")
        data=request.get_json(silent=True)
        print(data)
        boxupload=Box_Upload(data["status"],data["datecreated"],data["userid"])
        db.session.add(boxupload)
        db.session.commit()
        uploaddata=dict()
        uploaddata["id"]=boxupload.id
        uploaddata["status"]=boxupload.status
        uploaddata["datecreated"]=boxupload.datecreated
        uploaddata["userid"]=boxupload.userid
        return jsonify(uploaddata)


@read.route('/uploadTask',methods=["GET"])
def box_tasklist():
    if session["logged_in"]==True:
        uploadlist=Box_Upload.query.all()
        return render_template("uploadtask.html",tasklist=uploadlist)
    else:
        return redirect(url_for('add.login'))


@edit.route('/uploadTask/<int:taskid>',methods=["POST"])
def update_tasklist(taskid):
        uploadlist=Box_Upload.query.get(taskid)
        uploadlist.status=True
        db.session.commit()
        return "success"


@read.route('/readbox',methods=["GET"])
def read_box():
    if session["logged_in"]==True:
        box=Box.query.filter_by(account_id=session["accountId"]).first()
        if not box:
            flash("Your box account is not configured")
        return render_template("boxdetail.html",box=box)
    else:
        return redirect(url_for("add.login"))







    
