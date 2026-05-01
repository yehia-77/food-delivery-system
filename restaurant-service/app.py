from flask import Flask, jsonify, request

app = Flask(__name__)

restaurants = []
menus = {}

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "service": "restaurant-service"})

@app.route('/restaurants', methods=['POST'])
def add_restaurant():
    data = request.json
    restaurant = {
        "id": len(restaurants) + 1,
        "name": data['name'],
        "cuisine": data.get('cuisine', 'General')
    }
    restaurants.append(restaurant)
    menus[restaurant['id']] = []
    return jsonify({"message": "Restaurant added!", "restaurant": restaurant}), 201

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    return jsonify(restaurants)

@app.route('/restaurants/<int:restaurant_id>/menu', methods=['POST'])
def add_menu_item(restaurant_id):
    data = request.json
    item = {
        "id": len(menus.get(restaurant_id, [])) + 1,
        "name": data['name'],
        "price": data['price']
    }
    if restaurant_id not in menus:
        menus[restaurant_id] = []
    menus[restaurant_id].append(item)
    return jsonify({"message": "Item added!", "item": item}), 201

@app.route('/restaurants/<int:restaurant_id>/menu', methods=['GET'])
def get_menu(restaurant_id):
    return jsonify(menus.get(restaurant_id, []))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
