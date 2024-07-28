from flask import Flask, flash, redirect, render_template, request, url_for, session
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from wallet_func.wallet import wallet_bp
import requests

uri = "mongodb+srv://admin:admin@cluster0.tu1qoxk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['roticanai']
collection = db['roticanai']

app = Flask(__name__)
app.secret_key = '3ff05908-6127-4fd5-a4b5-27153ae7cf72'  # Set your secret key for sessions

app.register_blueprint(wallet_bp)

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

@app.route('/', methods=['GET', 'POST'])
def login_create():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash("Email and password are required.")
            return redirect(url_for('login_create'))

        # Fetch user from the database
        user = collection.find_one({"email": email, "pass": password})
        
        if user:
            # Handle wallet creation and update if necessary
            if not user.get('walletId'):
                wallet_response = create_wallet(user['userId'], user['email'])
                
                if wallet_response.get('status') == 200:
                    wallet_result = wallet_response.get('result')
                    wallet_data = wallet_result.get('wallet')
                    collection.update_one(
                        {"userId": user['userId']},
                        {"$set": {
                            "walletId": wallet_data['wallet_id'],
                            "walletAddr": wallet_data['wallet_address'],
                            "balance": 3000
                        }}
                    )
                    session['walletAddr'] = wallet_data['wallet_address']  # Update session with new wallet address
                else:
                    flash("Failed to create wallet. Please try again.")
                    return redirect(url_for('login_create'))

            # Store user information in session
            session['userId'] = user['userId']
            session['email'] = user['email']
            session['walletAddr'] = user.get('walletAddr', '')

            # Redirect based on email pattern
            if email.startswith('admin'):
                return redirect(url_for('admin_wallet'))
            elif email.startswith('user'):
                return redirect(url_for('wallet'))
            else:
                return redirect(url_for('index'))
        else:
            flash("Invalid credentials, please try again.")
            return redirect(url_for('login_create'))

    return render_template('login_create.html')


@app.route('/admin_dashboard')
def admin_dashboard():
    username = session.get('userId', 'Guest')
    email = session.get('email', 'Not Provided')
    walletAddr = session.get('walletAddr', 'Not Provided')
    return render_template('admin_dashboard.html', username=username, email=email, walletAddr=walletAddr)

@app.route('/index')
def index():
    # Get user information from session
    username = session.get('userId', 'Guest')
    email = session.get('email', 'Not Provided')
    walletAddr = session.get('walletAddr', 'Not Provided')
    return render_template('main.html', username=username, email=email, walletAddr=walletAddr)

@app.route('/wallet')
def wallet():
    # Get user information from session
    username = session.get('userId', 'Guest')
    email = session.get('email', 'Not Provided')
    walletAddr = session.get('walletAddr', 'Not Provided')
    return render_template('wallet.html', username=username, email=email, walletAddr=walletAddr)

@app.route('/adminwallet')
def admin_wallet():
    # Get user information from session
    username = session.get('userId', 'Guest')
    email = session.get('email', 'Not Provided')
    walletAddr = session.get('walletAddr', 'Not Provided')
    return render_template('admin_wallet.html', username=username, email=email, walletAddr=walletAddr)

@app.route('/org_cert')
def org_cert():
    # Get user information from session
    username = session.get('userId', 'Guest')
    email = session.get('email', 'Not Provided')
    walletAddr = session.get('walletAddr', 'Not Provided')
    return render_template('org_cert.html', username=username, email=email, walletAddr=walletAddr)

@app.route('/org_pass_cert')
def org_pass_cert():
    # Get user information from session
    username = session.get('userId', 'Guest')
    email = session.get('email', 'Not Provided')
    walletAddr = session.get('walletAddr', 'Not Provided')
    return render_template('org_pass_cert.html', username=username, email=email, walletAddr=walletAddr)

@app.route('/viewCert')
def viewCert():
    # Get user information from session
    username = session.get('userId', 'Guest')
    email = session.get('email', 'Not Provided')
    walletAddr = session.get('walletAddr', 'Not Provided')
    return render_template('viewCert.html', username=username, email=email, walletAddr=walletAddr)

@app.route('/main')
def main():
    # Get user information from session
    username = session.get('userId', 'Guest')
    email = session.get('email', 'Not Provided')
    walletAddr = session.get('walletAddr', 'Not Provided')
    return render_template('main.html', username=username, email=email, walletAddr=walletAddr)

@app.route('/donation')
def donation():
    # Get user information from session
    username = session.get('userId', 'Guest')
    email = session.get('email', 'Not Provided')
    walletAddr = session.get('walletAddr', 'Not Provided')
    return render_template('donation.html', username=username, email=email, walletAddr=walletAddr)

@app.route('/redemption')
def redemption():
    # Get user information from session
    username = session.get('userId', 'Guest')
    email = session.get('email', 'Not Provided')
    walletAddr = session.get('walletAddr', 'Not Provided')
    return render_template('redemption.html', username=username, email=email, walletAddr=walletAddr)

@app.route('/sign_out')
def sign_out():
    app.logger.info("Signing out user")
    session.clear()
    return redirect(url_for('login_create'))

@app.route('/my_profile')
def my_profile():
    return render_template('myprofile.html')

@app.route('/testing')
def testing():
    return render_template('animatedlogin.html')

@app.route('/certificate')
def certificate():
    return render_template('certificate.html')

@app.route('/volunteer')
def admin_volunteer():
    return render_template('admin_volunteer.html')

if __name__ == '__main__':
    app.run(debug=True)
