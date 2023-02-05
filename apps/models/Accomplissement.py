from apps.models.DatabaseManager import db, func

class Accomplissement(db.Model):
    __tablename__ = 'Accomplissement'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    exp_value = db.Column(db.Integer, nullable=False)

    def __init__(self, label, description, exp_value):
        self.label = label
        self.description = description
        self.exp_value = exp_value

    def toJson(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def pushToDB(self, db):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False
        
    @classmethod
    def exist(self, id):
        return bool(Accomplissement.query.get(id))

    @classmethod
    def getByLabel(self, label):
        return Accomplissement.query.filter(func.lower(Accomplissement.label) == func.lower(label)).first()

    @classmethod
    def getById(self, id):
        return Accomplissement.query.get(id)
    
    @classmethod
    def getAll(self):
        return Accomplissement.query.all()