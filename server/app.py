#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()
    bakeries_list = []
    for bakery in bakeries:
        bakery_dict ={
            'id' : bakery.id,
            'name' : bakery.name,
            'created_at' : bakery.created_at,
            'updated_at' : bakery.updated_at,
        }
        bakeries_list.append(bakery_dict)
    return jsonify(bakeries_list)
    

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()

    bakery_dict = bakery.to_dict()
    response = make_response(jsonify(
        bakery_dict
    ),200
        )
    
    response.headers['Content-Type'] = 'application/json'
    return response
    

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    goods_list=[]
    for good in goods:
         b_dict = good.to_dict()
         goods_list.append(b_dict)
    return jsonify(goods_list)

    

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    goods = BakedGood.query.order_by(BakedGood.price.desc()).first()
    b_dict = {
             'id' : goods.id,
             'name': goods.name,
             'price': goods.price,
             'created_at' : goods.created_at,
             'updated_at' : goods.updated_at,
         }
    response = make_response(jsonify(b_dict))
    return response
    

if __name__ == '__main__':
    app.run(port=5555, debug=True)
