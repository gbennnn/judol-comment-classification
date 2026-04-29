"""
Configuration file untuk Sistem Moderasi Preventif
"""

import os

# =====================================================
# FLASK CONFIGURATION
# =====================================================

FLASK_DEBUG = True
FLASK_ENV = 'development'
HOST = '0.0.0.0'
PORT = 5000

# =====================================================
# MODEL CONFIGURATION
# =====================================================

# Paths
MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')
SVM_MODEL_PATH = os.path.join(MODEL_DIR, 'svm_model.pkl')
TFIDF_VECTORIZER_PATH = os.path.join(MODEL_DIR, 'tfidf_vectorizer.pkl')
PREPROCESSING_DICT_PATH = os.path.join(MODEL_DIR, 'preprocessing_dict.pkl')

# =====================================================
# DECISION ENGINE CONFIGURATION
# =====================================================

# Threshold untuk decision making
# Jika probability_judi > THRESHOLD → BLOKIR
# Jika probability_judi <= THRESHOLD → PUBLIKASI
THRESHOLD = 0.50

# Decision labels
DECISION_BLOCK = "BLOKIR OTOMATIS"
DECISION_PUBLISH = "PUBLIKASI NORMAL"

ACTION_BLOCK = "Komentar disembunyikan dan tidak akan dipublikasikan"
ACTION_PUBLISH = "Komentar akan dipublikasikan normalmente"

SEVERITY_HIGH = "high"
SEVERITY_LOW = "low"

# =====================================================
# PREPROCESSING CONFIGURATION
# =====================================================

# Minimum dan maximum panjang komentar
MIN_COMMENT_LENGTH = 3
MAX_COMMENT_LENGTH = 1000

# =====================================================
# TF-IDF CONFIGURATION
# =====================================================

TFIDF_MAX_FEATURES = 5000
TFIDF_NGRAM_RANGE = (1, 1)

# =====================================================
# MODEL TRAINING CONFIGURATION (untuk save_model.py)
# =====================================================

DATASET_PATH = '../dataset/dataset_judol_clean.csv'
DATASET_COLUMN_TEXT = 'comment_text_clean'
DATASET_COLUMN_LABEL = 'label'

# Train/Test split
TEST_SIZE = 0.2
RANDOM_STATE = 42
STRATIFY = True

# =====================================================
# SVM CONFIGURATION
# =====================================================

SVM_KERNEL = 'linear'
SVM_CLASS_WEIGHT = 'balanced'
SVM_PROBABILITY = True
SVM_RANDOM_STATE = 42

# =====================================================
# API CONFIGURATION
# =====================================================

API_VERSION = 'v1'
API_PREFIX = '/api'

# Response status
RESPONSE_SUCCESS = 'success'
RESPONSE_ERROR = 'error'

# =====================================================
# LOGGING CONFIGURATION (Optional untuk future)
# =====================================================

LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# =====================================================
# SECURITY CONFIGURATION
# =====================================================

JSON_SORT_KEYS = False
JSONIFY_PRETTYPRINT_REGULAR = True

# =====================================================
# PREPROCESSING PIPELINE CONFIGURATION
# =====================================================

PREPROCESSING_STEPS = [
    'unicode_normalization',
    'obfuscation_replacement',
    'url_normalization',
    'text_cleaning',
]

# Character replacements untuk obfuscation
OBFUSCATION_DICT = {
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

# =====================================================
# SYSTEM INFORMATION
# =====================================================

SYSTEM_NAME = "Sistem Moderasi Preventif Judi Online"
SYSTEM_VERSION = "1.0.0"
MODEL_TYPE = "Support Vector Machine (SVM) Baseline"
VECTORIZER_TYPE = "TF-IDF"

# =====================================================
# EXAMPLE COMMENTS (untuk testing)
# =====================================================

EXAMPLE_COMMENTS = [
    {
        "text": "Nonton vidio nih keren banget",
        "category": "normal",
        "description": "Contoh komentar normal"
    },
    {
        "text": "Buruan join casino online kami sekarang",
        "category": "judi",
        "description": "Contoh komentar judi"
    },
    {
        "text": "Mau main togel? klik link iniiii 🅿️🅻 jaminan jackpot",
        "category": "judi",
        "description": "Contoh dengan obfuscation"
    }
]
