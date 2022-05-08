import datetime
from app import db, ma, bcrypt


class Item(db.Model):
    def __init__(self, lbpAmount, usdAmount, sell, bought, user_id):
        super(Item, self).__init__(lbpAmount=lbpAmount,
                                   usdAmount=usdAmount,
                                   sell=sell,
                                   bought=bought,
                                   user_id=user_id)

    id = db.Column(db.Integer, primary_key=True)
    lbpAmount = db.Column(db.Float, nullable=False)
    usdAmount = db.Column(db.Float, nullable=False)
    sell = db.Column(db.Boolean, nullable=False)
    bought = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="cascade", onupdate="cascade"), nullable=False, )


class ItemSchema(ma.Schema):
    class Meta:
        fields = ("lbpAmount", "usdAmount", "sell")
        model = Item



item_schema = ItemSchema()
items_schema  = ItemSchema(many=True)