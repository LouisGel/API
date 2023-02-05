from apps.models.DatabaseManager import db, func

class State(db.Model):
    __tablename__ = 'State'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)

    def __init__(self, label, description):
            self.label = label
            self.description = description

    def toJson(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def pushToDB(self, db):
        db.session.add(self) 
        db.session.commit()

        try:
            return True
        except:
            return False

    @classmethod
    def exist(self, id):
        return bool(State.query.get(id))

    @classmethod
    def getByLabel(self, label):
        return State.query.filter(func.lower(State.label) == func.lower(label)).first()

    @classmethod
    def getById(self, id):
        return State.query.get(id)
    
    @classmethod
    def getAll(self):
        return State.query.all()