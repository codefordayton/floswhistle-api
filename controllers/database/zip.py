import uuid

from extensions import db

class Zip(db.Model):
    __tablename__ = 'zips'

    id = db.Column(db.String(64), primary_key=True)
    zip = db.Column(db.String(6), nullable=False, index=True)
    state = db.Column(db.String(2), nullable=False)
    district = db.Column(db.String(2), nullable=False)
    factor = db.Column(db.Float(8), nullable=False)

    def __init__(self, zip=None, state=None, district=None,
                 factor=None, **kwargs):
        self.id = str(uuid.uuid4())
        self.zip = zip
        self.state = state
        self.district = district
        self.factor = factor

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

