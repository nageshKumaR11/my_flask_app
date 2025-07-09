import json
from flask import Flask, request, jsonify

app = Flask(__name__)

file_path = 'my_flask_app\data\items.json'

# In-memory item list
with open(file_path, 'r') as file:
    items = json.load(file)

print(f"Items : {items}")    
#  
@app.route('/')
def home():
    return "Welcome to the Flask App!"

@app.route('/greet/<name>', methods=['GET'])
def greet(name):
    return f"Hello, {name}!"

@app.route('/add', methods=['POST'])
def add_numbers():
    data = request.get_json()
    a = data.get('a', 0)
    b = data.get('b', 0)
    return jsonify({"result": a + b})

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items)

@app.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()
    new_id = max(item["id"] for item in items) + 1 if items else 1
    new_item = {"id": new_id, "name": data["name"]}
    items.append(new_item)
    with open(file_path, 'w') as file:
        json.dump(items, file, indent=4)
    return jsonify(new_item), 201

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global items
    items = [item for item in items if item["id"] != item_id]
    return jsonify({"message": f"Item {item_id} deleted."})

if __name__ == '__main__':
    app.run(debug=True)