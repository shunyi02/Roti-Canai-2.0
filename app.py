from flask import Flask, render_template
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

app = Flask(__name__)

# Initialize Firebase
cred = credentials.Certificate('database.json')
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

@app.route('/')
def main_page():
    return render_template('main_page.html')

@app.route('/database_testing')
def db_test():
    # Perform Firestore operations
    try:
        # Add a test document
        doc_ref = db.collection('test').document('testDoc')
        doc_ref.set({'message': 'Hello from Firebase!'})

        # Read the document
        doc = doc_ref.get()
        if doc.exists:
            message = f'Connected to Firebase successfully! Document data: {doc.to_dict()}'
        else:
            message = 'No such document!'
    except Exception as e:
        message = f'Error: {str(e)}'
    
    return render_template('dbtest.html', message=message)

@app.route('/login_create')
def login_create():
    return render_template('login_create.html')

@app.route('/sign_out')
def sign_out():
    return render_template('sign_out.html')

if __name__ == '__main__':
    app.run(debug=True)
