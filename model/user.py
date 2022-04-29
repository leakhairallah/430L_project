from ..app import db, ma, bcrypt


class User(db.Model):
    def __init__(self, user_name, password):
        super(User, self).__init__(user_name=user_name)
        self.hashed_password = bcrypt.generate_password_hash(password)
	  self.balance_lbp = 0
	  self.balance_usd = 0

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30), unique=True)
    hashed_password = db.Column(db.String(128))
    balance_lbp = db.Column(db.Integer)
    balance_usd = db.Column(db.Integer)
    is_admin = db.Column(db.Boolean)


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "user_name")
        model = User


user_schema = UserSchema()
