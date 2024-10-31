from flask import Flask, jsonify, request

app = Flask(__name__)
sums = []

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