from apps.models.DatabaseManager import db, func
from datetime import datetime



class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(200), nullable=False)
    prenom = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    level = db.Column(db.Integer, nullable=False)
    exp = db.Column(db.Integer, nullable=False)

    def __init__(self, email, password):
        user = User.getUserbyEmail(email)
        if user != None : 
            self = user
        else:
            self.email = email
            self.password = sha256_crypt.encrypt(password)



    def pushToDB(self, db):
        if self.alreadyExist(): return False
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
