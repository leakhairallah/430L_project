import datetime
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
import jwt

from .db_config import DB_CONFIG

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONFIG
db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
CORS(app)

SECRET_KEY = "b'|\xe7\xbfU3`\xc4\xec\xa7\xa9zf:}\xb5\xc7\xb9\x139^3@Dv'"

from .model.user import User, user_schema
from .model.transaction import Transaction, transaction_schema, transactions_schema


@app.route('/exchangeRate', methods=['GET'])
def exchangeRate():
    avg_usd_lbp = Transaction.query.filter(
        Transaction.added_date.between(datetime.datetime.now() - datetime.timedelta(days=3), datetime.datetime.now()),
        Transaction.usd_to_lbp == True).all()
    avg_lbp_usd = Transaction.query.filter(
        Transaction.added_date.between(datetime.datetime.now() - datetime.timedelta(days=3), datetime.datetime.now()),
        Transaction.usd_to_lbp == False).all()

    sell = []
    buy = []

    for el in avg_usd_lbp:
        buy.append(el.lbp_amount / el.usd_amount)
    for el in avg_lbp_usd:
        sell.append(el.lbp_amount / el.usd_amount)

    if len(buy) > 0:
        usd_to_lbp = round((sum(buy) / len(buy)), 2)
    else:
        usd_to_lbp = 0
    if len(sell) > 0:
        lbp_to_usd = round((sum(sell) / len(sell)), 2)
    else:
        lbp_to_usd = 0

    return jsonify({"usd_to_lbp": usd_to_lbp, "lbp_to_usd": lbp_to_usd})


@app.route('/stats', methods=['GET'])
def stats():
    d = datetime.datetime.now()
    diff = datetime.timedelta(days=1)

    sell_per_day_count = []
    buy_per_day_count = []
    sell_per_day_avg = []
    buy_per_day_avg = []

    for i in range(20):
        avg_usd_lbp = Transaction.query.filter(Transaction.added_date.between(d - i * diff, d),
                                               Transaction.usd_to_lbp == True).all()
        avg_lbp_usd = Transaction.query.filter(Transaction.added_date.between(d - i * diff, d),
                                               Transaction.usd_to_lbp == True).all()
        sell = []
        buy = []

        for el in avg_usd_lbp:
            buy.append(el.lbp_amount / el.usd_amount)
        for el in avg_lbp_usd:
            sell.append(el.lbp_amount / el.usd_amount)

        if len(buy) > 0:
            usd_to_lbp = round((sum(buy) / len(buy)), 2)
        else:
            usd_to_lbp = 0
        if len(sell) > 0:
            lbp_to_usd = round((sum(sell) / len(sell)), 2)
        else:
            lbp_to_usd = 0

        sell_per_day_count.append(avg_lbp_usd.count())
        buy_per_day_count.append(avg_usd_lbp.count())
        sell_per_day_avg.append(lbp_to_usd)
        buy_per_day_avg.append(usd_to_lbp)
        
    return jsonify({"sell_count": sell_per_day_count, "buy_count": buy_per_day_count, "avg_sell": sell_per_day_avg, "avg_buy": buy_per_day_avg})


@app.route('/addMoney', methods=['POST'])
def addMoney():
    amount_lbp = request.json['amount_lbp']
    amount_usd = request.json['amount_usd']
    username = request.json['username']

    u = User.query.filter_by(user_name=username).first()

    if u:
        if amount_lbp:
            u.balance_LBP += amount_lbp
        if amount_usd:
            u.balance_USD += amount_usd
        db.session.commit()
        return jsonify(user_schema.dump(u))
    else:
        return jsonify({"Error": "User input not valid"})


@app.route('/transaction', methods=['POST'])
def transaction():
    usd_amount = request.json["usd_amount"]
    lbp_amount = request.json["lbp_amount"]
    usd_to_lbp = request.json["usd_to_lbp"]

    token = extract_auth_token(request)

    if token is None:
        t = Transaction(usd_amount, lbp_amount, usd_to_lbp, None)
        db.session.add(t)
        db.session.commit()
        return jsonify(transaction_schema.dump(t))

    else:
        try:
            decoded = decode_token(token)
            t = Transaction(usd_amount, lbp_amount, usd_to_lbp, decoded)
            db.session.add(t)
            db.session.commit()
            return jsonify(transaction_schema.dump(t))

        except jwt.ExpiredSignatureError:
            abort(403)
        except jwt.InvalidTokenError:
            abort(403)


@app.route('/transaction', methods=['GET'])
def transactionG():
    token = extract_auth_token(request)

    if token is None:
        abort(403)
    else:
        try:
            decoded = decode_token(token)
            all_trans = Transaction.query.filter_by(user_id=decoded).all()
            return jsonify(transactions_schema.dump(all_trans))

        except jwt.ExpiredSignatureError:
            abort(403)
        except jwt.InvalidTokenError:
            abort(403)


@app.route('/user', methods=['POST'])
def user():
    user_name = request.json["user_name"]
    password = request.json["password"]

    u = User(user_name, password)

    db.session.add(u)
    db.session.commit()

    return jsonify(user_schema.dump(u))


@app.route('/authentication', methods=['POST'])
def authentication():
    username = request.json["user_name"]
    password = request.json["password"]

    if username is None or password is None:
        abort(400)

    auth = User.query.filter_by(user_name=username).first()

    if auth is None:
        abort(403)

    if not bcrypt.check_password_hash(auth.hashed_password, password):
        abort(403)
    else:
        token = create_token(auth.id)
        return jsonify({"token": token})


def create_token(user_id):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=4),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm='HS256'
    )


def extract_auth_token(authenticated_request):
    auth_header = authenticated_request.headers.get('Authorization')
    if auth_header:
        return auth_header.split(" ")[1]
    else:
        return None


def decode_token(token):
    payload = jwt.decode(token, SECRET_KEY, 'HS256')
    return payload['sub']
