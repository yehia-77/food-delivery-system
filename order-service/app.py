from flask import Flask, jsonify, request
import pika, json, os

app = Flask(__name__)

orders = []

def publish_to_rabbitmq(message):
    try:
        rabbitmq_host = os.getenv('RABBITMQ_HOST', 'rabbitmq')
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=rabbitmq_host)
        )
        channel = connection.channel()
        channel.queue_declare(queue='payment_queue')
        channel.basic_publish(
            exchange='',
            routing_key='payment_queue',
            body=json.dumps(message)
        )
        connection.close()
        return True
    except Exception as e:
        print(f"RabbitMQ error: {e}")
        return False

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "service": "order-service"})

@app.route('/orders', methods=['POST'])
def place_order():
    data = request.json
    order = {
        "id": len(orders) + 1,
        "user_id": data['user_id'],
        "restaurant_id": data['restaurant_id'],
        "items": data['items'],
        "total": data['total'],
        "status": "pending"
    }
    orders.append(order)
    publish_to_rabbitmq({
        "order_id": order['id'],
        "total": order['total'],
        "user_id": order['user_id']
    })
    return jsonify({"message": "Order placed!", "order": order}), 201

@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify(orders)

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = next((o for o in orders if o['id'] == order_id), None)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(order)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
