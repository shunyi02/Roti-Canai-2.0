from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import requests

# Blueprint setup
wallet_bp = Blueprint('wallet', __name__)

# MongoDB connection
uri = "mongodb+srv://admin:admin@cluster0.tu1qoxk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['roticanai']  # replace with your database name
collection = db['roticanai']  # replace with your collection name

# Function to create a new wallet
def create_wallet(name, email, ic, phone, entity_id):
    api_url = "https://service-testnet.maschain.com/api/wallet/create-user"
    headers = {
        "client_id": "bdcd674b4307ae68fc8b115e4354fed29659deccc4a17b2c5d8ce37beb5e8a5c",
        "client_secret": "sk_0d1dcea6180c1376f5b1a7fa67e0d4acfdffd1c0f27a69a4a1f2012a74b0155a",
        "content-type": "application/json"
    }
    data = {
        "name": name,
        "email": email
    }
    response = requests.post(api_url, headers=headers, json=data)
    return response.json()

@wallet_bp.route('/api/check-wallet', methods=['POST'])
def check_wallet():
    user_id = request.json.get('userId')
    user = collection.find_one({"userId": user_id})
    
    if user and not user.get('walletId'):
        name = user.get('name')
        email = user.get('email')
        
        wallet_response = create_wallet(name, email)
        
        if wallet_response.get('status') == 200:
            wallet_data = wallet_response.get('wallet')
            collection.update_one(
                {"userId": user_id},
                {"$set": {
                    "walletId": wallet_data['wallet_id'],
                    "walletAddr": wallet_data['wallet_address'],
                    "balance": 3000
                }}
            )
            return jsonify({"message": "Wallet created and updated successfully", "wallet": wallet_data}), 200
        else:
            return jsonify({"message": "Failed to create wallet"}), 400
    
    return jsonify({"message": "User already has a wallet or user not found"}), 400

@wallet_bp.route('/api/check-balance', methods=['POST'])
def check_balance():
    user_id = request.json.get('userId')
    user = collection.find_one({"userId": user_id})
    
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    wallet_addr = user.get('walletAddr')
    
    if not wallet_addr:
        return jsonify({"message": "Wallet address not found"}), 404
    
    api_url = "https://service-testnet.maschain.com/api/token/balance"
    headers = {
        "client_id": "bdcd674b4307ae68fc8b115e4354fed29659deccc4a17b2c5d8ce37beb5e8a5c",
        "client_secret": "sk_0d1dcea6180c1376f5b1a7fa67e0d4acfdffd1c0f27a69a4a1f2012a74b0155a",
        "content-type": "application/json"
    }
    data = {
        "wallet_address": wallet_addr,
        "contract_address": "0x6E84d9eD84A98460F090E8A337507F1cC4000564"
    }
    
    response = requests.post(api_url, headers=headers, json=data)
    balance_data = response.json()
    
    if balance_data.get('status') == 200:
        return jsonify({
            "balance_in_db": user.get('balance'),
            "balance_from_api": balance_data.get('result')
        }), 200
    else:
        return jsonify({"message": "Failed to retrieve balance"}), 400
