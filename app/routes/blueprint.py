from flask import Blueprint

add=Blueprint('add',__name__,url_prefix="/add")
read=Blueprint('read',__name__,url_prefix="/read")
edit=Blueprint('update',__name__,url_prefix="/edit")
myhome=Blueprint('myhome',__name__,url_prefix="/myhome")