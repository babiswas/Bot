from wtforms import Form,StringField

class BotForm(Form):
            url=StringField("Bot Url")
            botname=StringField("Bot Name")
            description=StringField("Description")


class PrimeForm(Form):
            appname=StringField("Appname")
            clientid=StringField("Clientid")
            clientsecret=StringField("ClientSecret")
            server=StringField("Server Adress")
            email=StringField("Email")
            redirecturi=StringField("Redirect URI")
            primeaccount=StringField("Prime Account")



class BoxForm(Form):
            appname=StringField("Appname")
            clientid=StringField("Clientid")
            clientsecret=StringField("ClientSecret")
            folderid=StringField("Folder Config")

class RegisterForm(Form):
            firstname=StringField("Firstname")
            lastname=StringField("Lastname")
            username=StringField("Username")
            password=StringField("Password")
            confirm=StringField("Confirm Password")

class AccountForm(Form):
            name=StringField("Account Name")
            email=StringField("Root User Mail")


class LoginForm(Form):
            username=StringField("Username")
            password=StringField("Password")











    
      




