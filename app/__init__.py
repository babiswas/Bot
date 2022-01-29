from flask import Flask
from app.routes.blueprint import add,edit,read,myhome
from config import Config
from app.models.dbutil import db
from app.models import prime_models,user_models,box_models,bot_models,task_models
from app.service.botservice import service_add,service_edit,service_read
from app.service.userservice import service_add,service_edit,service_read
from app.service.primeservice import service_prime
from app.service.boxservice import service_box
from app.service.user_actions import service_action
from app.service import home


def create_app():
   app=Flask(__name__)
   app.config.from_object(Config)
   db.init_app(app)
   with app.app_context():
      db.create_all()
   app.register_blueprint(add)
   app.register_blueprint(edit)
   app.register_blueprint(read)
   app.register_blueprint(myhome)
   return app