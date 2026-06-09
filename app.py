from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

# Ambil path absolut agar Vercel pasti menemukan file CSV
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, 'dataset.csv')

try:
    df = pd.read_csv(csv_path)
    print("Dataset berhasil dimuat!")
except Exception as e:
    print(f"Error memuat dataset: {e}")
    df = pd.DataFrame()

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "success",
        "message": "API Mesin Pencari STKI Berjalan Lancar di Vercel!"
    })

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    
    if not query:
        return jsonify({"error": "Query pencarian tidak boleh kosong"}), 400

    hasil = []
    for index, row in df.iterrows():
        hasil.append({
            "id": row['id'],
            "judul": row['judul'],
            "konten_snippet": str(row['konten'])[:80] + "...", 
            "skor_relevansi": 0.99, # Skor dummy
            "url_sumber": row['url_sumber']
        })

    return jsonify({
        "query_anda": query,
        "total_hasil": len(hasil),
        "data": hasil
    })

if __name__ == '__main__':
    app.run(debug=True)