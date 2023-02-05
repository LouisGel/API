from apps.models.DatabaseManager import db, func
from datetime import datetime

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(200), nullable=False)
    lname = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    exp = db.Column(db.Integer, nullable=False)

    def __init__(self, fname, lname, email):
        user = User.getUserbyEmail(email)
        if user != None : 
            self = user
        else:
            self.fname = fname
            self.lname = lname
            self.email = email
            self.exp = 0

    def toJson(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def pushToDB(self, db):
        if User.exist(self.email): return False
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False

    @classmethod
    def exist(self, email):
        return bool(User.query.filter(func.lower(User.email) == func.lower(email)).first())

    @classmethod
    def getUserbyEmail(self, email):
        return User.query.filter(func.lower(User.email) == func.lower(email)).first()

    @classmethod
    def getById(self, id):
        return User.query.get(id)
    
    @classmethod
    def getAll(self):
        return User.query.all()