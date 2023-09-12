from flask import Flask, jsonify, request
import uuid
import math
from datetime import datetime

app = Flask(__name__)

# In-memory data store
receipts = {}

@app.route('/receipts/process', methods=['POST'])
def process_receipts():
    data = request.get_json()

    try:
        purchase_date = datetime.strptime(data['purchaseDate'], "%Y-%m-%d")
        purchase_time = datetime.strptime(data['purchaseTime'], "%H:%M")
    except ValueError as e:
        return jsonify({"error": "Invalid date or time format"}), 400

    receipt_id = str(uuid.uuid4()) # Generate a unique ID for the receipt
    receipts[receipt_id] = data # Store the receipt data in memory
    return jsonify({"id": receipt_id}), 201

def calculate_points(receipt):
    total_points = 0
    retailer_name = receipt.get('retailer')
    total = float(receipt.get('total'))
    purchase_date = datetime.strptime(receipt.get('purchaseDate'), "%Y-%m-%d")
    purchase_time = datetime.strptime(receipt.get('purchaseTime'), "%H:%M")

    # Rule 1: One point for every alphanumeric character in the retailer name.
    total_points += sum(c.isalnum() for c in retailer_name)

    # Rule 2: 50 points if the total is a round dollar amount with no cents.
    if total.is_integer():
        total_points += 50

    # Rule 3: 25 points if the total is a multiple of 0.25.
    if total % 0.25 == 0:
        total_points += 25

    # Rule 4: 5 points for every two items on the receipt.
    total_items = len(receipt.get('items'))
    total_points += (total_items // 2) * 5

    # Rule 5: If the trimmed length of the item description is a multiple of 3,
    # multiply the price by 0.2 and round up to the nearest integer.
    for item in receipt.get('items'):
        description_length = len(item.get('shortDescription').strip())
        if description_length % 3 == 0:
            item_points = int(math.ceil(float(item.get('price')) * 0.2))
            total_points += item_points

    # Rule 6: 6 points if the day in the purchase date is odd.
    if purchase_date.day % 2 != 0:
        total_points += 6

    # Rule 7: 10 points if the time of purchase is after 2:00pm and before 4:00pm.
    if 14 <= purchase_time.hour < 16:
        total_points += 10

    return total_points

@app.route('/receipts/<string:id>/points', methods=['GET'])
def get_points(id):
    receipt = receipts.get(id)
    if receipt is None:
        return jsonify({"error": "Receipt not found"}), 404

    total_points = calculate_points(receipt)

    return jsonify({"points": total_points}), 200



if __name__ == '__main__':
    app.run(debug=True)
