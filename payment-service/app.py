from flask import Flask, jsonify, request
import pika, json, os, threading

app = Flask(__name__)

payments = []

def consume_orders():
    try:
        rabbitmq_host = os.getenv('RABBITMQ_HOST', 'rabbitmq')
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=rabbitmq_host)
        )
        channel = connection.channel()
        channel.queue_declare(queue='payment_queue')

        def callback(ch, method, properties, body):
            order_data = json.loads(body)
            payment = {
                "id": len(payments) + 1,
                "order_id": order_data['order_id'],
                "amount": order_data['total'],
                "status": "completed"
            }
            payments.append(payment)
            print(f"Payment processed: {payment}")

        channel.basic_consume(
            queue='payment_queue',
            on_message_callback=callback,
            auto_ack=True
        )
        channel.start_consuming()
    except Exception as e:
        print(f"RabbitMQ consumer error: {e}")

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "service": "payment-service"})

@app.route('/payments', methods=['GET'])
def get_payments():
    return jsonify(payments)

@app.route('/pay', methods=['POST'])
def manual_pay():
    data = request.json
    payment = {
        "id": len(payments) + 1,
        "order_id": data['order_id'],
        "amount": data['amount'],
        "status": "completed"
    }
    payments.append(payment)
    return jsonify({"message": "Payment successful!", "payment": payment}), 201

if __name__ == '__main__':
    thread = threading.Thread(target=consume_orders, daemon=True)
    thread.start()
    app.run(host='0.0.0.0', port=5000, debug=True)
