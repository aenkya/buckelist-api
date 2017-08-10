from app import db


class BaseModel(db.Model):
    ''' A model detailing the base properties to be inherited '''
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def delete(self):
        '''delete data from database'''
        db.session.delete(self)
        db.session.commit()

    def __init__(self, name):
        '''initialize with name'''
        self.name = name

    def save(self):
        '''save data to database'''
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def __item_exists():
        pass
