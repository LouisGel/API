from apps.models.DatabaseManager import db
from datetime import datetime

class Todo(db.Model):
    __tablename__ = 'Todo'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    id_accomplissement = db.Column(db.Integer, db.ForeignKey("Accomplissement.id"), nullable=False)
    id_state = db.Column(db.Integer, db.ForeignKey("State.id"), nullable=False)
    finish_date = db.Column(db.DateTime, nullable=True)

    def __init__(self, id_user, id_accomplissement, id_state):
        self.id_user = id_user
        self.id_accomplissement = id_accomplissement
        self.id_state = id_state
        
    def toJson(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def pushToDB(self, db):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False

    def finished(self):
        self.finish_date = datetime.utcnow()
        try:
            db.session.commit()
            return True
        except:
            return False

    @classmethod
    def getById(self, id):
        return Todo.query.get(id)
    
    @classmethod
    def getAll(self):
        return Todo.query.all()