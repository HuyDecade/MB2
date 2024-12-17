from flask import Flask
from flask_cors import CORS
from controllers.authController import auth
from controllers.fraudDetectionController import fraud_detection
from controllers.transactionController import transaction_bp
app = Flask(__name__)
CORS(app)

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(fraud_detection, url_prefix='/fraud_detection')
app.register_blueprint(transaction_bp, url_prefix='/api/transactions')

if __name__ == '__main__':
    app.run(debug=True)
