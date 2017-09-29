from app.models.baseModel import BaseModel, db
from .item import Item


class Bucketlist(BaseModel):
    '''This class represents the bucketlist model'''

    __table__name = 'bucketlist'

    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    items = db.relationship(
        'Item', cascade='all, delete', backref='item', uselist=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def save_bucketlist(self):
        ''' Method to save bucketlist '''
        bucket = self.exists()
        if bucket:
            if bucket.active:
                return False
            else:
                bucket.active = True
        self.save()
        return True

    def delete_bucketlist(self, deep_delete=False):
        ''' Method to delete bucketlist '''
        if not deep_delete:
            if self.deactivate():
                return True
            return False
        if self.exists():
            self.delete()
            return True
        return False

    def exists(self):
        ''' Check if bucketlist exists '''
        bucket = Bucketlist.query.filter_by(name=self.name).first()
        return bucket if bucket else False

    def __repr__(self):
        return "<Bucketlist: {}>".format(self.name)

    def __str__(self):
        return '{0}'.format(self.name)
