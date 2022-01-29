from app.routes.blueprint import add,read,edit
from app.models.dbutil import db
from app.models.prime_models import Prime
from flask import request,redirect,render_template,url_for,session
from app.forms.form import PrimeForm
from app.routes.blueprint import add,read,edit,myhome
from requests import post
from flask import flash
import json

@add.route('/configPrime',methods=["POST","GET"])
def add_prime_config():
      if session["logged_in"]==True:
            form=PrimeForm(request.form)
            if request.method=="POST" and form.validate:
                  appname=request.form.get("appname")
                  clientid=request.form.get("clientid")
                  clientsecret=request.form.get("clientsecret")
                  server=request.form.get("server")
                  email=request.form.get("email")
                  redirecturi=request.form.get("redirecturi")
                  primeaccount=request.form.get("primeaccount")
                  prime=Prime(appname,clientid,clientsecret,'',server,session["accountId"],email,redirecturi,primeaccount)
                  db.session.add(prime)
                  db.session.commit()
                  return redirect(url_for('read.prime_config',primeid=prime.id))
            return render_template("primeconfig.html",form=form)
      else:
         return redirect(url_for('add.login'))



@read.route('/primeConfig/<int:primeid>',methods=["GET"])
def prime_config(primeid):
   prime=Prime.query.get(primeid)
   return render_template("primedetails.html",prime=prime)



@edit.route('/primeConfig/<int:primeid>',methods=["POST","GET"])
def edit_config(primeid):
      if session["logged_in"]==True:
         prime=Prime.query.get(primeid)
         form=PrimeForm(obj=prime)
         if request.method=="POST" and form.validate:
               prime.clientid=request.form.get("clientid")
               prime.clientsecret=request.form.get("clientsecret")
               db.session.commit()
               return redirect(url_for('read.prime_config',primeid=prime.id))
         return render_template("primeconfig.html",form=form)
      else:
         return redirect(url_for('add.login'))


@read.route('/oauthCode',methods=["GET"])
def prime_oauth():
      if session["logged_in"]==True:
            prime=Prime.query.filter_by(account_id=session["accountId"]).first()
            prime_url=prime.server+"oauth/o/authorize?"
            prime_url+="client_id="+prime.clientid
            prime_url+="&redirect_uri="+prime.redirecturi+"read/refreshToken"
            prime_url+="&account="+prime.primeaccount
            prime_url+="&email="+prime.email
            prime_url+="&logoutAfterAuthorize=true"
            prime_url+="&scope=admin:read,admin:write"
            return redirect(prime_url,code=302,Response=None)
      else:
            return redirect(url_for('add.login'))


@read.route('/refreshToken',methods=["GET"])
def configure_prime():
      code=request.args.get("code")
      if session["logged_in"]==True:
            prime=Prime.query.filter_by(account_id=session["accountId"]).first()
            url=prime.server+"oauth/token"
            params=dict()
            params["client_id"]=prime.clientid
            params["client_secret"]=prime.clientsecret
            params["code"]=code
            headers=dict()
            headers["Content-Type"]="application/x-www-form-urlencoded"
            res=post(url,params=params,headers=headers)
            if res.status_code!=200:
                  raise Exception
            token=post('http://127.0.0.1:5000/edit/primeRefresh/'+str(prime.id),params={"refresh_token":res.json()['refresh_token']})
            if token.status_code!=200:
                  raise Exception
            return redirect(url_for('read.prime_config',primeid=prime.id))
      else:
            return redirect(url_for('add.login'))


@edit.route('/primeRefresh/<int:primeid>',methods=["POST"])
def update_refresh_token(primeid):
      token=request.args.get('refresh_token')
      prime=Prime.query.get(primeid)
      prime.refreshtoken=token
      db.session.commit()
      return "success"


@read.route('/readPrime',methods=["GET"])
def read_prime():
      if session["logged_in"]==True:
            prime=Prime.query.filter_by(account_id=session["accountId"]).first()
            if not prime:
                  flash("Your prime account is not configured")
            return render_template("primedetails.html",prime=prime)
      else:
            return redirect(url_for("add.login"))



