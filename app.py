from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('main_page.html')

@app.route('/login_create')
def login_create():
    return render_template('login_create.html')

@app.route('/sign_out')
def sign_out():
    return render_template('sign_out.html')

if __name__ == '__main__':
    app.run(debug=True)
