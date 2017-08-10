from app import db


class Item(db.Model):
    '''This class represents the item model'''

    __table__name = 'item'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    done = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    bucketlist_id = db.Column(db.Integer,
                              db.ForeignKey('bucketlist.id'), nullable=False)

    def __init__(self, name):
        '''initialize with name'''
        self.name = name

    def save(self):
        '''save data to database'''
        db.session.add(self)
        db.session.commit()

    def delete(self):
        '''delete data from database'''
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Item: {}>".format(self.name)

    def __str__(self):
        return '{0}'.format(self.name)
