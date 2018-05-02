from app import db

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(4000))
    #submitted = db.Column(db.Boolean)

    def __init__(self, title, body):  
        self.title = title
        self.body = body

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    owner = db.Column(db.String(120))
    #submitted = db.Column(db.Boolean)

    def __init__(self, title, body):  
        self.username = username
        self.password = password
        self.owner = owner