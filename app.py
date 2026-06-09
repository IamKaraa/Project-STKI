from flask import Flask, request, jsonify
import csv
import os

app = Flask(__name__)

# Ambil path absolut agar Vercel pasti menemukan file CSV
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, 'dataset.csv')

# Variabel penampung data
dataset_dokumen = []

try:
    # Membaca CSV menggunakan modul bawaan Python
    with open(csv_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            dataset_dokumen.append(row)
    print("Dataset berhasil dimuat tanpa Pandas!")
except Exception as e:
    print(f"Error memuat dataset: {e}")

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "success",
        "message": "API Mesin Pencari STKI Berjalan Super Ringan di Vercel!"
    })

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    
    if not query:
        return jsonify({"error": "Query pencarian tidak boleh kosong"}), 400

    hasil = []
    # Looping array biasa, bukan dataframe Pandas
    for row in dataset_dokumen:
        hasil.append({
            "id": row['id'],
            "judul": row['judul'],
            # Pastikan kolom 'konten' ada di CSV-mu
            "konten_snippet": str(row['konten'])[:80] + "...", 
            "skor_relevansi": 0.99, # Skor dummy sementara
            "url_sumber": row['url_sumber']
        })

    return jsonify({
        "query_anda": query,
        "total_hasil": len(hasil),
        "data": hasil
    })

if __name__ == '__main__':
    app.run(debug=True)