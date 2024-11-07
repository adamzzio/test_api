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

# Endpoint untuk menerima gambar dan mengubahnya menjadi hitam putih
@app.route('/convert_to_bw', methods=['POST'])
def convert_to_bw():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    # Cek apakah file benar-benar diunggah
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    # Periksa apakah file adalah gambar
    if file and file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        try:
            # Baca gambar menggunakan PIL
            img = Image.open(file.stream)
            
            # Konversi gambar menjadi hitam putih
            bw_img = img.convert('L')

            # Simpan gambar hitam putih ke dalam buffer
            buffered = io.BytesIO()
            bw_img.save(buffered, format="JPEG")
            buffered.seek(0)
            
            # Encode gambar hitam putih dalam base64
            img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

            # Kirimkan hasil sebagai JSON
            return jsonify({
                'message': 'Image converted to black and white successfully',
                'bw_image': img_base64
            })
        except Exception as e:
            return jsonify({'error': 'Failed to process image file', 'details': str(e)}), 500

    else:
        return jsonify({'error': 'Unsupported file format. Please upload a JPG or PNG image.'}), 400


# Menjalankan aplikasi
if __name__ == '__main__':
    app.run(debug=True)
