# api/index.py
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Endpoint untuk menambahkan dua angka
@app.route('/sum', methods=['GET'])
def sum_numbers():
    # Mengambil parameter 'a' dan 'b' dari URL
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)

    # Validasi bahwa 'a' dan 'b' telah diberikan
    if a is None or b is None:
        return jsonify({'error': 'Parameters a and b are required and must be numbers.'}), 400

    # Menjumlahkan angka
    result = a + b

    # Mengembalikan hasil dalam format JSON
    return jsonify({'a': a, 'b': b, 'result': result})

# Route untuk pengecekan API status
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'API is running and healthy'}), 200

# Menjalankan aplikasi
if __name__ == '__main__':
    app.run(debug=True)
