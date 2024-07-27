from flask import Flask, flash, redirect, render_template, request, url_for
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from wallet_func.wallet import wallet_bp

uri = "mongodb+srv://admin:admin@cluster0.tu1qoxk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['roticanai']
collection = db['roticanai']

app = Flask(__name__)
app.secret_key = '3ff05908-6127-4fd5-a4b5-27153ae7cf72'

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
            return redirect(url_for('main_page'))
        else:
            flash("Invalid credentials, please try again.")
            return redirect(url_for('login_create'))

    return render_template('login_create.html')


@app.route('/main_page')
def main_page():
    return render_template('main_page.html')

@app.route('/sign_out')
def sign_out():
    return render_template('sign_out.html')


if __name__ == '__main__':
    app.run(debug=True)
