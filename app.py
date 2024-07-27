from flask import Flask, flash, redirect, render_template, request, url_for, session
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from wallet_func.wallet import wallet_bp

uri = "mongodb+srv://admin:admin@cluster0.tu1qoxk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['roticanai']
collection = db['roticanai']

app = Flask(__name__)
app.secret_key = '3ff05908-6127-4fd5-a4b5-27153ae7cf72'  # Set your secret key for sessions

app.register_blueprint(wallet_bp)

@app.route('/', methods=['GET', 'POST'])
def login_create():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash("Email and password are required.")
            return redirect(url_for('login_create'))

        user = collection.find_one({"email": email, "pass": password})
        
        if user:
            # Store user information in session
            session['userId'] = user['userId']
            session['walletAddr'] = user['walletAddr']
            session['email'] = user['email']
            return redirect(url_for('wallet'))
        else:
            flash("Invalid credentials, please try again.")
            return redirect(url_for('login_create'))

    return render_template('login_create.html')

@app.route('/index')
def index():
    # Get user information from session
    username = session.get('userId', 'Guest')
    email = session.get('email', 'Not Provided')
    walletAddr = session.get('walletAddr', 'Not Provided')
    return render_template('index.html', username=username, email=email, walletAddr=walletAddr)

@app.route('/wallet')
def wallet():
    # Get user information from session
    username = session.get('userId', 'Guest')
    email = session.get('email', 'Not Provided')
    walletAddr = session.get('walletAddr', 'Not Provided')
    return render_template('wallet.html', username=username, email=email, walletAddr=walletAddr)

@app.route('/sign_out')
def sign_out():
    # Clear session
    session.clear()
    return redirect(url_for('login_create'))

if __name__ == '__main__':
    app.run(debug=True)
