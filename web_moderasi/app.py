"""
Flask Application untuk Simulasi Sistem Moderasi Preventif
Menggunakan Model SVM Baseline
"""

from flask import Flask, render_template, request, jsonify
import pickle
import re
import unicodedata
import os
import json

# =====================================================
# INITIALIZE FLASK APP
# =====================================================

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# =====================================================
# PREPROCESSING FUNCTIONS
# =====================================================

obfuscation_dict = {
    # === HURUF (ENCLOSED / SQUARE) ===
    "🅰": "a", "🅱": "b", "🅲": "c", "🅳": "d", "🅴": "e",
    "🅵": "f", "🅶": "g", "🅷": "h", "🅸": "i", "🅹": "j",
    "🅺": "k", "🅻": "l", "🅼": "m", "🅽": "n", "🅾": "o",
    "🅿": "p", "🆀": "q", "🆁": "r", "🆂": "s", "🆃": "t",
    "🆄": "u", "🆅": "v", "🆆": "w", "🆇": "x", "🆈": "y",
    "🆉": "z",
    "🅰️": "a", "🅱️": "b", "🅾️": "o", "🅿️": "p",
    # === HURUF LINGKARAN ===
    "ⓐ": "a", "ⓑ": "b", "ⓒ": "c", "ⓓ": "d", "ⓔ": "e",
    "ⓕ": "f", "ⓖ": "g", "ⓗ": "h", "ⓘ": "i", "ⓙ": "j",
    "ⓚ": "k", "ⓛ": "l", "ⓜ": "m", "ⓝ": "n", "ⓞ": "o",
    "ⓟ": "p", "ⓠ": "q", "ⓡ": "r", "ⓢ": "s", "ⓣ": "t",
    "ⓤ": "u", "ⓥ": "v", "ⓦ": "w", "ⓧ": "x", "ⓨ": "y",
    "ⓩ": "z",
    # === HURUF LINGKARAN KAPITAL ===
    "Ⓐ": "a", "Ⓑ": "b", "Ⓒ": "c", "Ⓓ": "d", "Ⓔ": "e",
    "Ⓕ": "f", "Ⓖ": "g", "Ⓗ": "h", "Ⓘ": "i", "Ⓙ": "j",
    "Ⓚ": "k", "Ⓛ": "l", "Ⓜ": "m", "Ⓝ": "n", "Ⓞ": "o",
    "Ⓟ": "p", "Ⓠ": "q", "Ⓡ": "r", "Ⓢ": "s", "Ⓣ": "t",
    "Ⓤ": "u", "Ⓥ": "v", "Ⓦ": "w", "Ⓧ": "x", "Ⓨ": "y",
    "Ⓩ": "z",
    # === ANGKA LINGKARAN ===
    "⓪": "0", "①": "1", "②": "2", "③": "3", "④": "4",
    "⑤": "5", "⑥": "6", "⑦": "7", "⑧": "8", "⑨": "9",
    "❶": "1", "❷": "2", "❸": "3", "❹": "4", "❺": "5",
    "❻": "6", "❼": "7", "❽": "8", "❾": "9",
    # === EMOJI ANGKA ===
    "0️⃣": "0", "1️⃣": "1", "2️⃣": "2", "3️⃣": "3",
    "4️⃣": "4", "5️⃣": "5", "6️⃣": "6",
    "7️⃣": "7", "8️⃣": "8", "9️⃣": "9",
    # === SIMBOL UMUM ===
    "@": "a", "$": "s", "!": "i", "€": "e",
}

pattern = re.compile("|".join(map(re.escape, obfuscation_dict.keys())))

def replace_obfuscation(text):
    """Replace obfuscation characters"""
    return pattern.sub(lambda x: obfuscation_dict[x.group()], text)

def normalize_unicode(text):
    """Normalize unicode characters"""
    text = unicodedata.normalize('NFKD', text)
    text = ''.join(c for c in text if not unicodedata.combining(c))
    return text

def normalize_urls(text):
    """Replace URLs with 'iniurl'"""
    url_pattern = r'(https?://\S+|www\.\S+)'
    return re.sub(url_pattern, 'iniurl', text)

def clean_text(text):
    """Clean text: lowercase, remove special chars, handle spacing"""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def preprocess_text(text):
    """Complete preprocessing pipeline"""
    # 1. Unicode normalization
    text = normalize_unicode(text)
    # 2. Replace obfuscation
    text = replace_obfuscation(text)
    # 3. Normalize unicode again
    text = normalize_unicode(text)
    # 4. Replace URLs
    text = normalize_urls(text)
    # 5. Clean text
    text = clean_text(text)
    return text

# =====================================================
# LOAD MODELS
# =====================================================

try:
    # Load SVM model
    with open('models/svm_model.pkl', 'rb') as f:
        svm_model = pickle.load(f)
    print("✓ SVM model loaded successfully")
except FileNotFoundError:
    print("✗ Error: SVM model not found. Run save_model.py first!")
    svm_model = None

try:
    # Load TF-IDF vectorizer
    with open('models/tfidf_vectorizer.pkl', 'rb') as f:
        tfidf_vectorizer = pickle.load(f)
    print("✓ TF-IDF vectorizer loaded successfully")
except FileNotFoundError:
    print("✗ Error: TF-IDF vectorizer not found. Run save_model.py first!")
    tfidf_vectorizer = None

# =====================================================
# DECISION ENGINE
# =====================================================

THRESHOLD = 0.50

def make_decision(probability_judi):
    """
    Decision Engine untuk menentukan tindakan preventif
    
    Input: probability_judi (float) - Probabilitas prediksi kelas 1 (Promosi Judi)
    Output: dict berisi keputusan dan tindakan
    """
    
    if probability_judi > THRESHOLD:
        decision = "BLOKIR OTOMATIS"
        action = "Komentar disembunyikan dan tidak akan dipublikasikan"
        color = "red"
        severity = "high"
    else:
        decision = "PUBLIKASI NORMAL"
        action = "Komentar akan dipublikasikan normalmente"
        color = "green"
        severity = "low"
    
    return {
        "decision": decision,
        "action": action,
        "color": color,
        "severity": severity
    }

# =====================================================
# FLASK ROUTES
# =====================================================

@app.route('/')
def index():
    """Halaman utama"""
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    """API endpoint untuk prediksi"""
    
    try:
        # Get JSON data
        data = request.get_json()
        comment = data.get('comment', '').strip()
        
        # Validate input
        if not comment:
            return jsonify({
                'error': True,
                'message': 'Silakan masukkan komentar terlebih dahulu'
            }), 400
        
        if len(comment) < 3:
            return jsonify({
                'error': True,
                'message': 'Komentar terlalu pendek (minimal 3 karakter)'
            }), 400
        
        if len(comment) > 1000:
            return jsonify({
                'error': True,
                'message': 'Komentar terlalu panjang (maksimal 1000 karakter)'
            }), 400
        
        # Check if models are loaded
        if svm_model is None or tfidf_vectorizer is None:
            return jsonify({
                'error': True,
                'message': 'Model belum dimuat. Silakan jalankan save_model.py terlebih dahulu'
            }), 500
        
        # =========== PREPROCESSING ==========
        original_comment = comment
        comment_clean = preprocess_text(comment)
        
        if not comment_clean:
            return jsonify({
                'error': True,
                'message': 'Komentar tidak valid setelah preprocessing'
            }), 400
        
        # =========== FEATURE EXTRACTION ==========
        comment_tfidf = tfidf_vectorizer.transform([comment_clean])
        
        # =========== PREDICTION ==========
        prediction = svm_model.predict(comment_tfidf)[0]
        probabilities = svm_model.predict_proba(comment_tfidf)[0]
        
        prob_non_judi = probabilities[0]  # Class 0
        prob_judi = probabilities[1]      # Class 1
        
        # =========== DECISION ENGINE ==========
        decision_data = make_decision(prob_judi)
        
        # =========== RESPONSE ==========
        response = {
            'error': False,
            'original_comment': original_comment,
            'cleaned_comment': comment_clean,
            'prediction': {
                'class': 'Promosi Judi Online' if prediction == 1 else 'Non-Promosi',
                'class_code': int(prediction),
                'probability_non_judi': float(prob_non_judi),
                'probability_judi': float(prob_judi),
                'confidence': float(max(prob_non_judi, prob_judi))
            },
            'decision': {
                'verdict': decision_data['decision'],
                'action': decision_data['action'],
                'severity': decision_data['severity'],
                'color': decision_data['color']
            },
            'threshold': THRESHOLD
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        print(f"Error in predict endpoint: {str(e)}")
        return jsonify({
            'error': True,
            'message': f'Terjadi kesalahan: {str(e)}'
        }), 500

@app.route('/api/info', methods=['GET'])
def info():
    """Endpoint untuk mendapatkan informasi sistem"""
    
    return jsonify({
        'sistem': 'Sistem Moderasi Preventif Judi Online YouTube',
        'model': 'Support Vector Machine (SVM) Baseline',
        'threshold': THRESHOLD,
        'threshold_description': f'Probabilitas > {THRESHOLD}: Blokir, Probabilitas ≤ {THRESHOLD}: Publikasi',
        'preprocessing': [
            'Unicode Normalization',
            'Obfuscation Character Replacement',
            'URL Normalization',
            'Text Cleaning (lowercase, remove special chars)',
        ],
        'feature_extraction': 'TF-IDF Vectorization (max_features=5000, ngram=(1,1))',
        'status': 'ready' if (svm_model is not None and tfidf_vectorizer is not None) else 'error'
    }), 200

# =====================================================
# ERROR HANDLERS
# =====================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': True, 'message': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': True, 'message': 'Internal server error'}), 500

# =====================================================
# RUN APP
# =====================================================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
