from flask import Flask
from flask_cors import CORS
from controllers.authController import auth
from controllers.transactionController import transaction_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(transaction_bp, url_prefix='/api/transactions')

@app.route('/')
def home():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080)
