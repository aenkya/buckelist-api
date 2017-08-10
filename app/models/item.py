from app.models.baseModel import BaseModel
from app import db


class Item(BaseModel):
    '''This class represents the item model'''

    __table__name = 'item'

    name = db.Column(db.Text, nullable=False)
    done = db.Column(db.Boolean, default=False)
    bucketlist_id = db.Column(db.Integer,
                              db.ForeignKey('bucketlist.id'), nullable=False)

    def save_item(self):
        ''' method to save bucketlist item '''
        self.add_data_set()
        return True

    def delete_item(self):
        ''' method to delete bucketlist item '''
        self.delete_data_set()
        db.session.commit()
        return True

    def __repr__(self):
        return "<Item: {}>".format(self.name)

    def __str__(self):
        return '{0}'.format(self.name)
