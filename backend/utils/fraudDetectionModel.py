import tensorflow as tf
import numpy as np
import os

MODEL_PATH = 'fraud_detection_model.h5'

def create_and_save_model():
    """
    Tạo và lưu mô hình phát hiện gian lận.
    """
    if os.path.exists(MODEL_PATH):
        print(f"Model already exists at '{MODEL_PATH}'.")
        return

    # Tạo dữ liệu giả để huấn luyện
    np.random.seed(42)
    X_train = np.random.random((5000, 3))  # 5000 mẫu, mỗi mẫu có 3 đặc trưng
    y_train = np.random.randint(0, 2, 5000)  # Nhãn nhị phân

    # Xây dựng mô hình
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(32, activation='relu', input_shape=(3,)),
        tf.keras.layers.Dense(16, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    # Compile và huấn luyện mô hình
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=1)

    # Lưu mô hình
    model.save(MODEL_PATH)
    print(f"Model saved to '{MODEL_PATH}'.")

def detect_fraud(transaction_data):
    """
    Kiểm tra giao dịch có gian lận hay không.
    """
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file '{MODEL_PATH}' not found. Please train the model first.")

    model = tf.keras.models.load_model(MODEL_PATH)
    transaction_data = np.array([transaction_data])
    prediction = model.predict(transaction_data, verbose=0)[0][0]

    return prediction > 0.5  # Ngưỡng 0.5 để phát hiện gian lận
