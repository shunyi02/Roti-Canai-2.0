from flask import Blueprint, request, jsonify,session
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

#done check
# Function to create a new wallet
def create_wallet(name, email):
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

#done check
@wallet_bp.route('/api/check-wallet', methods=['POST'])
def check_wallet():
    userId = request.json.get('userId')
    #print(userId)
    #user_id = session['userId']
    user = collection.find_one({"userId": userId})
    
    if user and not user.get('walletId'):
        name = userId
        email = user.get('email')
        # name = session['userId']
        # email = session['email']
        
        wallet_response = create_wallet(name, email)
        #print(wallet_response)
        
        if wallet_response.get('status') == 200:
            wallet_result = wallet_response.get('result')
            wallet_data = wallet_result.get('wallet')
            print(wallet_data)
            collection.update_one(
                {"userId": userId},
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

#done check
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
        "contract_address": "0x7b583DAfB2C3b57940d22053AEE07669325808DE"
    }
    
    response = requests.post(api_url, headers=headers, json=data)
    balance_data = response.json()
    print(balance_data)
    if balance_data.get('status') == 200:
        return jsonify({
            "balance_in_db": float(user.get('balance')),
            "balance_from_api": float(balance_data.get('result'))
        }), 200
    else:
        return jsonify({"message": "Failed to retrieve balance"}), 400

#done check
@wallet_bp.route('/api/top-up', methods=['POST'])
def top_up_balance():
    user_id = request.json.get('userId')
    top_up_amount = float(request.json.get('amount'))
    
    if not user_id or not top_up_amount:
        return jsonify({"message": "User ID and top-up amount are required"}), 400
    
    user = collection.find_one({"userId": user_id})
    
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    new_balance = float(user.get('balance', 0)) + top_up_amount
    collection.update_one(
        {"userId": user_id},
        {"$set": {"balance": new_balance}}
    )
    
    return jsonify({"message": "Balance topped up successfully", "new_balance": new_balance}), 200

#done check
@wallet_bp.route('/api/remove-funds', methods=['POST'])
def remove_funds():
    user_id = request.json.get('userId')
    amount_to_remove = float(request.json.get('amount'))
    
    # Validate input
    if not user_id or not amount_to_remove:
        return jsonify({"message": "User ID and amount to remove are required"}), 400
    
    try:
        amount_to_remove = float(amount_to_remove)
        if amount_to_remove <= 0:
            return jsonify({"message": "Amount must be greater than zero"}), 400
    except ValueError:
        return jsonify({"message": "Invalid amount format"}), 400
    
    # Find the user
    user = collection.find_one({"userId": user_id})
    
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    current_balance = float(user.get('balance', 0))
    
    # Check if there are sufficient funds
    if amount_to_remove > current_balance:
        return jsonify({"message": "Insufficient funds"}), 400
    
    # Update the balance
    new_balance = current_balance - amount_to_remove
    collection.update_one(
        {"userId": user_id},
        {"$set": {"balance": new_balance}}
    )
    
    return jsonify({"message": "Funds removed successfully", "new_balance": new_balance, "status": "Success"}), 200

#done
@wallet_bp.route('/api/transfer-token-after-purchase', methods=['POST'])
def mint_token_after_fund_purchase():
    user_id = request.json.get('userId')
   
    wallet_address = "0x6E84d9eD84A98460F090E8A337507F1cC4000564"  # Fixed wallet address
    contract_address = "0x7b583DAfB2C3b57940d22053AEE07669325808DE" #need modify (find)
    callback_url = "https://postman-echo.com/post?"

    amount_to_transfer = request.json.get('amount')
    
    # Validate input
    if not user_id or not amount_to_transfer:
        return jsonify({"message": "User ID and amount to transfer are required"}), 400

    # Find the user
    user = collection.find_one({"userId": user_id})
    
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    wallet_addr = user.get('walletAddr')
    
    if not wallet_addr:
        return jsonify({"message": "User's wallet address not found"}), 404

    # API request to mint tokens
    api_url = "https://service-testnet.maschain.com/api/token/mint"
    headers = {
        "client_id": "bdcd674b4307ae68fc8b115e4354fed29659deccc4a17b2c5d8ce37beb5e8a5c",
        "client_secret": "sk_0d1dcea6180c1376f5b1a7fa67e0d4acfdffd1c0f27a69a4a1f2012a74b0155a",
        "content-type": "application/json"
    }
    data = {
        "wallet_address": wallet_address,
        "to": wallet_addr,
        "amount": float(amount_to_transfer),
        "contract_address": contract_address,
        "callback_url": callback_url
    }

    response = requests.post(api_url, headers=headers, json=data)
    print(response.json())
    return jsonify(response.json()), response.status_code

#done check
@wallet_bp.route('/api/remove-tokens', methods=['POST'])
def remove_tokens():
    user_id = request.json.get('userId')
    amount_to_burn = request.json.get('amount')  # amount in smallest unit
    
    if not user_id or not amount_to_burn:
        return jsonify({"message": "User ID and amount to burn are required"}), 400
    
    try:
        amount_to_burn = str(float(amount_to_burn))  # Ensure the amount is in string format
    except ValueError:
        return jsonify({"message": "Invalid amount format"}), 400
    
    # Find the user
    user = collection.find_one({"userId": user_id})
    
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    wallet_address = user.get('walletAddr')
    if not wallet_address:
        return jsonify({"message": "User's wallet address not found"}), 404

    contract_address = "0x7b583DAfB2C3b57940d22053AEE07669325808DE"
    
    # Check token balance
    balance_api_url = "https://service-testnet.maschain.com/api/token/balance"
    headers = {
        "client_id": "bdcd674b4307ae68fc8b115e4354fed29659deccc4a17b2c5d8ce37beb5e8a5c",
        "client_secret": "sk_0d1dcea6180c1376f5b1a7fa67e0d4acfdffd1c0f27a69a4a1f2012a74b0155a",
        "content-type": "application/json"
    }
    balance_data = {
        "wallet_address": wallet_address,
        "contract_address": contract_address
    }
    
    balance_response = requests.post(balance_api_url, headers=headers, json=balance_data)
    balance_result = balance_response.json()
    
    if balance_response.status_code != 200 or balance_result.get('status') != 200:
        return jsonify({"message": "Failed to check token balance"}), 500
    
    current_balance = float(balance_result.get('result', 0))
    print(current_balance)
    
    if float(amount_to_burn) > current_balance:
        return jsonify({"message": "Insufficient tokens"}), 400
    
    # Burn the tokens
    burn_api_url = "https://service-testnet.maschain.com/api/token/burn"
    burn_data = {
        "wallet_address": "0x6E84d9eD84A98460F090E8A337507F1cC4000564", #org wallet
        "to": wallet_address,
        "amount": amount_to_burn,
        "contract_address": contract_address,
        "callback_url": "https://postman-echo.com/post?"
    }
    burn_response = requests.post(burn_api_url, headers=headers, json=burn_data)
    return jsonify(burn_response.json()), burn_response.status_code

from flask import request, jsonify
import requests

@wallet_bp.route('/api/org_create_cert', methods=['POST'])
def org_create_cert():
    # Extract data from the request JSON
    data = request.json
    wallet_address = "0x6E84d9eD84A98460F090E8A337507F1cC4000564"
    name = data.get('name')
    wallet_address_owner = "0x6E84d9eD84A98460F090E8A337507F1cC4000564"
    max_supply = data.get('max_supply')
    certificate_name = data.get('certificate_name')
    symbol = data.get('symbol')
    image = data.get('image', "")
    callback_url = data.get('callback_url', "")

    # Validate required fields
    if not wallet_address or not name or not wallet_address_owner or not max_supply or not certificate_name or not symbol:
        return jsonify({"message": "All required fields must be provided"}), 400

    # Prepare the field object
    field = {
        "wallet_address_owner": wallet_address_owner,
        "max_supply": max_supply,
        "name": certificate_name,
        "symbol": symbol
    }

    # Prepare the data payload for the API request
    payload = {
        "wallet_address": wallet_address,
        "name": name,
        "field": field
    }
    
    print("Payload Data: ", payload)
    
    # Set up the headers
    headers = {
        "client_id": "bdcd674b4307ae68fc8b115e4354fed29659deccc4a17b2c5d8ce37beb5e8a5c",
        "client_secret": "sk_0d1dcea6180c1376f5b1a7fa67e0d4acfdffd1c0f27a69a4a1f2012a74b0155a",
        "content-type": "application/json"
    }

    try:
        # Make the API request to create the smart contract
        response = requests.post("https://service-testnet.maschain.com/api/certificate/create-smartcontract", json=payload, headers=headers)
        response_data = response.json()
        
        print("API Response: ", response_data)
        
        # Return the API response
        return jsonify(response_data)
    except requests.RequestException as e:
        print("Request Exception: ", e)
        return jsonify({"message": "An error occurred while making the API request"}), 500



@wallet_bp.route('/api/pass_cert', methods=['POST'])
def pass_cert():
    # Extract data from the form
    wallet_address = "0x6E84d9eD84A98460F090E8A337507F1cC4000564"
    to = "0xe8c785f47244704D45B76E70Da1DF6C78FA07440"
    contract_address = "0x131aE01B9cE60b41B053e370B9B42cB1Ea43ab0d"
    name = request.form.get('name')
    description = request.form.get('description')
    callback_url = "https://postman-echo.com/post?"
    file = request.files.get('file')  # File upload

    # Validate required fields
    if not wallet_address or not to or not contract_address or not name or not description or not callback_url or not file:
        return jsonify({"message": "All required fields must be provided"}), 400

    # Prepare the payload for the API request
    data = {
        "wallet_address": wallet_address,
        "to": to,
        "contract_address": contract_address,
        "name": name,
        "description": description,
        "callback_url": callback_url
    }

    print(data)
    # Create a multipart/form-data payload
    files = {
        "file": (file.filename, file, file.mimetype)
    }

    print(files)
    
    # Set up the headers
    headers = {
        "client_id": "bdcd674b4307ae68fc8b115e4354fed29659deccc4a17b2c5d8ce37beb5e8a5c",
        "client_secret": "sk_0d1dcea6180c1376f5b1a7fa67e0d4acfdffd1c0f27a69a4a1f2012a74b0155a"
    }

    # Make the API request to mint the certificate
    response = requests.post(
        "https://service-testnet.maschain.com/api/certificate/mint-certificate",
        data=data,
        files=files,
        headers=headers
    )
    response_data = response.json()

    # Print API response for debugging
    print("API Response: ", response_data)

    # Return the API response
    return jsonify(response_data), response.status_code