from flask import Flask, request, jsonify, render_template
import csv
import os
import math
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

app = Flask(__name__)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

# 1. Inisialisasi Stemmer Sastrawi
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# 2. Fungsi Preprocessing (Sesuai rubrik STKI)
def preprocess(text):
    # Case folding & hapus karakter selain huruf/angka
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    # Tokenization & Stemming
    tokens = text.split()
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    return stemmed_tokens

# 3. Load dan Preprocess Dataset ke Memory
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, 'dataset.csv')
dataset_dokumen = []

try:
    with open(csv_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            # Lakukan preprocessing pada konten teks saat server menyala
            row['tokens'] = preprocess(row['konten'])
            dataset_dokumen.append(row)
    print("Dataset dan Preprocessing berhasil dimuat!")
except Exception as e:
    print(f"Error memuat dataset: {e}")

# Fungsi menghitung Term Frequency (TF)
def compute_tf(term, tokens):
    count = tokens.count(term)
    return count / len(tokens) if len(tokens) > 0 else 0

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    if not query:
        return jsonify({"error": "Query kosong"}), 400

    # A. Preprocessing Query
    query_tokens = preprocess(query)
    if not query_tokens:
        return jsonify({"query_anda": query, "total_hasil": 0, "data": []})

    # Kosakata unik dari query (sebagai dimensi vektor)
    vocab = list(set(query_tokens))
    N = len(dataset_dokumen)

    # B. Menghitung IDF untuk kosakata query
    idfs = {}
    for term in vocab:
        df = sum(1 for doc in dataset_dokumen if term in doc['tokens'])
        # Jika kata tidak ada di dokumen manapun, IDF = 0
        idfs[term] = math.log10(N / df) if df > 0 else 0

    # C. Membuat Vektor Query
    query_vector = []
    for term in vocab:
        tf = compute_tf(term, query_tokens)
        query_vector.append(tf * idfs[term])

    query_magnitude = math.sqrt(sum(v**2 for v in query_vector))
    
    if query_magnitude == 0:
        return jsonify({"query_anda": query, "total_hasil": 0, "data": []})

    # D. Menghitung Vektor Dokumen & Cosine Similarity
    hasil = []
    for doc in dataset_dokumen:
        doc_vector = []
        for term in vocab:
            tf = compute_tf(term, doc['tokens'])
            doc_vector.append(tf * idfs[term])

        doc_magnitude = math.sqrt(sum(v**2 for v in doc_vector))
        
        # Perhitungan Cosine
        if doc_magnitude == 0:
            score = 0
        else:
            dot_product = sum(query_vector[i] * doc_vector[i] for i in range(len(vocab)))
            score = dot_product / (query_magnitude * doc_magnitude)

        # Hanya tampilkan dokumen yang relevan (skor > 0)
        if score > 0:
            hasil.append({
                "id": doc['id'],
                "judul": doc['judul'],
                "konten_snippet": str(doc['konten'])[:120] + "...",
                "skor_relevansi": round(score, 4), # Dibulatkan 4 desimal
                "url_sumber": doc['url_sumber']
            })

    # E. Ranking Dokumen (diurutkan dari skor tertinggi)
    hasil = sorted(hasil, key=lambda x: x['skor_relevansi'], reverse=True)

    return jsonify({
        "query_anda": query,
        "total_hasil": len(hasil),
        "data": hasil
    })
    
@app.route('/all-documents', methods=['GET'])
def all_documents():
    return jsonify({
        "total": len(dataset_dokumen),
        "data": dataset_dokumen
    })

if __name__ == '__main__':
    app.run(debug=True)