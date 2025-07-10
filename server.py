#! /usr/bin/env python3.6
"""
Python 3.6 or newer required.
"""
import http.client
import json
import os
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS  # ✅ Tambahkan ini

app = Flask(__name__,
            static_folder='public',
            static_url_path='',
            template_folder='public')

CORS(app)  # ✅ Aktifkan CORS untuk semua endpoint (bisa dibatasi kalau mau)

def calculate_order_amount(items):
    # Replace this constant with a calculation of the order's amount
    # Calculate the order total on the server to prevent
    # people from directly manipulating the amount on the client
    return 1400

@app.route('/create-payment', methods=['POST'])
def create_payment():
    try:
        conn = http.client.HTTPSConnection("sandbox.hyperswitch.io")

        # If you have two or more “business_country” + “business_label” pairs configured in your Hyperswitch dashboard,
        # please pass the fields business_country and business_label in this request body.
        # For accessing more features, you can check out the request body schema for payments-create API here :
        # https://api-reference.hyperswitch.io/docs/hyperswitch-api-reference/60bae82472db8-payments-create        

        payload = "{\n \"amount\": 100,\n \"currency\": \"USD\",\n\"customer_id\": \"hyperswitch_customer\"\n}"
        headers = {
            'Content-Type': "application/json",
            'Accept': "application/json",
            'api-key': "HYPERSWITCH_API_KEY",
        }
        conn.request("POST", "/payments", payload, headers)
        res = conn.getresponse()
        data = json.loads(res.read())
        return jsonify({'client_secret': data['client_secret']})
    except Exception as e:
        return jsonify(error=str(e)), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4242)  # ✅ Pastikan bisa diakses publik dari IP VPS
