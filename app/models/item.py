from app.models.baseModel import BaseModel, db


class Item(BaseModel):
    '''This class represents the item model'''

    name = db.Column(db.Text, nullable=False)
    done = db.Column(db.Boolean, default=False)
    bucketlist_id = db.Column(db.Integer,
                              db.ForeignKey('bucketlist.id'), nullable=False)

    def delete_item(self, deep_delete=False):
        ''' Method to delete item '''
        if not deep_delete:
            if self.deactivate():
                return True
            return False        
        if self.exists():
            self.delete()
            return True
        return False

    def save_item(self):
        ''' Method to save item '''
        item = self.exists()
        if item:
            if item.active:
                return False
            else:
                item.active = True
        self.save()
        return True

    def exists(self):
        ''' Check if item exists '''
        item = Item.query.filter_by(name=self.name).first()
        return item if item else False

    def __repr__(self):
        return "<Item: {}>".format(self.name)

    def __str__(self):
        return '{0}'.format(self.name)
