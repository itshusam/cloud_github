from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from Marshmallow import fields
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
app = Flask(__name__)
sums = []
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://sum_user:ttxs0KON6UbhoG9lLass6sKD5ENEo1wp@dpg-cshvt41u0jms73f798ng-a.oregon-postgres.render.com/sum'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

@app.route('/sum', methods=['POST'])
def add_sum():
    data = request.json
    result = data.get('result')
    sums.append(result)
    return jsonify({'message': 'Sum added!', 'result': result}), 201

@app.route('/sum', methods=['GET'])
def get_all_sums():
    return jsonify(sums), 200

@app.route('/sum/result/<int:result>', methods=['GET'])
def get_sums_by_result(result):
    filtered_sums = [s for s in sums if s == result]
    return jsonify(filtered_sums), 200

if __name__ == '__main__':
    app.run(debug=True)

