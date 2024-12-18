from flask import Blueprint, request, jsonify
from .. models.transaction import create_transaction, get_transactions_by_user
from  ..models.fraudAlert import create_fraud_alert
from utils.fraudDetectionModel import detect_fraud
import sys
import os

# Thêm thư mục gốc vào sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



transaction_bp = Blueprint('transaction', __name__)

@transaction_bp.route('/check_fraud', methods=['POST'])
def check_fraud():
    """
    Kiểm tra giao dịch có gian lận hay không
    """
    try:
        # Nhận dữ liệu từ request
        data = request.get_json()
        if not data or not all(key in data for key in ('user_id', 'amount', 'location', 'timestamp')):
            return jsonify({'error': 'Dữ liệu không đầy đủ'}), 400

        user_id = data['user_id']
        amount = data['amount']
        location = data['location']
        timestamp = data['timestamp']

        # Lưu giao dịch vào database
        create_transaction(user_id, amount, location, timestamp)

        # Chuẩn bị dữ liệu và kiểm tra gian lận
        transaction_data = [amount, location, timestamp]  # Tuỳ chỉnh theo mô hình của bạn
        is_fraud = detect_fraud(transaction_data)

        if is_fraud:
            create_fraud_alert(user_id, f"Giao dịch gian lận được phát hiện cho người dùng {user_id}")
            return jsonify({'alert': 'Gian lận được phát hiện! Đã tạo cảnh báo.'}), 200

        return jsonify({'alert': 'Giao dịch an toàn.'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@transaction_bp.route('/transactions/<user_id>', methods=['GET'])
def get_user_transactions(user_id):
    """
    Lấy danh sách giao dịch của người dùng
    """
    try:
        transactions = list(get_transactions_by_user(user_id))  # Chuyển Cursor thành danh sách
        if not transactions:
            return jsonify({'message': 'Không tìm thấy giao dịch nào cho người dùng này.'}), 404

        return jsonify({'transactions': transactions}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
