from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://<user>:<password>@<host>/<database>'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class Sum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    result = db.Column(db.Integer, nullable=False)

# Routes
@app.route('/sum', methods=['POST'])
def add_sum():
    data = request.json
    result = data.get('result')
    if result is None:
        return jsonify({'error': 'Result is required'}), 400
    new_sum = Sum(result=result)
    db.session.add(new_sum)
    db.session.commit()
    return jsonify({'message': 'Sum added!', 'result': result}), 201

@app.route('/sum', methods=['GET'])
def get_all_sums():
    all_sums = Sum.query.all()
    return jsonify([{'id': s.id, 'result': s.result} for s in all_sums]), 200

@app.route('/sum/result/<int:result>', methods=['GET'])
def get_sums_by_result(result):
    filtered_sums = Sum.query.filter_by(result=result).all()
    if not filtered_sums:
        return jsonify({'error': f'No sums found for result {result}'}), 404
    return jsonify([{'id': s.id, 'result': s.result} for s in filtered_sums]), 200

if __name__ == '__main__':
    app.run(debug=True)
