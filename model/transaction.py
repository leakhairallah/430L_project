import datetime
from ..app import db, ma, bcrypt


class Transaction(db.Model):
    def __init__(self, usd_amount, lbp_amount, usd_to_lbp, user_id):
        super(Transaction, self).__init__(usd_amount=usd_amount,
                                          lbp_amount=lbp_amount,
                                          usd_to_lbp=usd_to_lbp,
                                          user_id=user_id,
                                          added_date=datetime.datetime.now())

    id = db.Column(db.Integer, primary_key=True)
    usd_amount = db.Column(db.Float, nullable=False)
    lbp_amount = db.Column(db.Float, nullable=False)
    usd_to_lbp = db.Column(db.Boolean, nullable=False)
    added_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)


class TransactionSchema(ma.Schema):
    class Meta:
        fields = ("id", "usd_amount", "lbp_amount", "usd_to_lbp", "user_id", "added_date")
        model = Transaction


transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)
