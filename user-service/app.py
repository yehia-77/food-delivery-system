from flask import Flask, jsonify, request
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

users = []

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "service": "user-service"})

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "name and email required"}), 400
    user = {
        "id": len(users) + 1,
        "name": data['name'],
        "email": data['email'],
        "role": data.get('role', 'customer')
    }
    users.append(user)
    return jsonify({"message": "User registered!", "user": user}), 201

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
