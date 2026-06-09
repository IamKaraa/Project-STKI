from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load dataset ke dalam memory saat server menyala
try:
    df = pd.read_csv('dataset.csv')
    print("Dataset berhasil dimuat!")
except Exception as e:
    print(f"Error memuat dataset: {e}")
    df = pd.DataFrame()

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "success",
        "message": "API Mesin Pencari STKI Berjalan Lancar!"
    })

@app.route('/search', methods=['GET'])
def search():
    
    query = request.args.get('q', '')
    
    if not query:
        return jsonify({"error": "Query pencarian tidak boleh kosong"}), 400

    # SKELETON: Saat ini algoritma mengembalikan data secara mentah
    # Algoritma TF-IDF dan Cosine Similarity akan disuntikkan di sini nanti
    
    hasil = []
    for index, row in df.iterrows():
        hasil.append({
            "id": row['id'],
            "judul": row['judul'],
            # Memotong teks agar menjadi snippet abstrak singkat
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
    # Mode debug dimatikan saat nanti jalan di production (Render)
    app.run(host='0.0.0.0', port=5000, debug=True)
