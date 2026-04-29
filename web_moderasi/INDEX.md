# 📚 INDEX - Dokumentasi Lengkap Sistem Moderasi Preventif

## 🎯 Ringkasan Proyek

Website simulasi **Sistem Moderasi Preventif Judi Online** untuk platform YouTube menggunakan Model Machine Learning **SVM Baseline**. Sistem dirancang untuk mendeteksi dan mengklasifikasi komentar yang mengandung promosi judi online secara real-time.

---

## 📂 Struktur File Proyek

```
web_moderasi/
├── 📄 app.py                      # Flask backend application
├── 📄 save_model.py               # Script untuk save model dari notebook
├── 📄 config.py                   # Centralized configuration
├── 📄 requirements.txt            # Python dependencies
│
├── 📖 README.md                   # Dokumentasi lengkap
├── 🚀 SETUP_GUIDE.md             # Quick setup guide
├── 📚 INDEX.md                    # File ini - dokumentasi index
│
├── 📁 models/                     # Folder untuk menyimpan trained models
│   ├── svm_model.pkl             # SVM trained model
│   ├── tfidf_vectorizer.pkl      # TF-IDF vectorizer
│   └── preprocessing_dict.pkl    # Dictionary karakter obfuscation
│
└── 📁 templates/
    └── 🌐 index.html             # Frontend HTML dengan Tailwind CSS
```

---

## 🗂️ Penjelasan File-File

### 🔴 **Backend Files**

#### `app.py` (Main Flask Application)
**Ukuran**: ~350 lines | **Type**: Python

**Fungsi Utama**:
- Initialize Flask app
- Load SVM model dan TF-IDF vectorizer
- Implement preprocessing pipeline
- Define API endpoints
- Decision engine untuk classification

**Key Components**:
```python
# Preprocessing functions
- replace_obfuscation()
- normalize_unicode()
- normalize_urls()
- clean_text()
- preprocess_text()

# API endpoints
- GET  /                  # Main page
- POST /api/predict       # Prediction endpoint
- GET  /api/info         # System info

# Decision engine
- make_decision(probability_judi)
```

**Konfigurable**:
- `THRESHOLD = 0.50` - Decision threshold
- Port: 5000 (dapat diubah)

---

#### `save_model.py` (Model Training & Saving)
**Ukuran**: ~150 lines | **Type**: Python

**Fungsi Utama**:
- Load dataset bersih dari CSV
- Split data (80% train, 20% test)
- Create TF-IDF vectorizer
- Train SVM baseline model
- Save model, vectorizer, dan preprocessing dict

**Output Files**:
- `models/svm_model.pkl`
- `models/tfidf_vectorizer.pkl`
- `models/preprocessing_dict.pkl`

**HARUS DIJALANKAN SEBELUM**: `app.py`

---

#### `config.py` (Configuration File)
**Ukuran**: ~200 lines | **Type**: Python (Optional)

**Berisi**:
- Flask configuration
- Model paths
- Decision engine settings
- Preprocessing configuration
- TF-IDF settings
- SVM model parameters
- Obfuscation dictionary
- Example comments

**Kegunaan**: Centralized configuration untuk future improvements

---

### 🔵 **Frontend Files**

#### `templates/index.html` (Web Interface)
**Ukuran**: ~450 lines | **Type**: HTML + CSS + JavaScript

**Fitur**:
- Beautiful UI dengan Tailwind CSS via CDN
- Input textarea dengan character counter
- Real-time form validation
- Submit button dengan loading state
- Results display section
- Probability visualization (progress bars)
- Decision display (color-coded)
- System info panel
- Preprocessing pipeline info
- Decision guide
- Example comments

**Key JavaScript Functions**:
```javascript
- predictComment()        // Main prediction function
- displayResults()        // Display results on page
- updateCharCount()       // Update char counter
- clearForm()             // Clear input
- useExample()            // Fill textarea dengan example
- showNotification()      // Show toast notifications
```

---

### 📋 **Configuration & Documentation Files**

#### `config.py`
Centralized configuration untuk:
- Flask settings
- Model paths dan parameters
- Decision engine thresholds
- Preprocessing settings
- TF-IDF configuration
- SVM parameters

#### `requirements.txt`
Python dependencies:
```
Flask==2.3.3
pandas==2.0.3
numpy==1.24.3
scikit-learn==1.3.0
imbalanced-learn==0.10.1
```

#### `README.md`
Dokumentasi lengkap yang mencakup:
- Fitur sistem
- Arsitektur sistem
- Instalasi step-by-step
- Cara penggunaan
- Komponen sistem
- Pipeline preprocessing
- Decision engine explanation
- Troubleshooting

#### `SETUP_GUIDE.md`
Quick setup guide (5 menit):
- Install dependencies
- Save model
- Run app
- Open browser
- Quick testing

#### `INDEX.md` (File ini)
Overview dokumentasi lengkap

---

## 🔄 Alur Kerja Sistem

### 1️⃣ **Setup Phase** (Sekali waktu)
```
save_model.py
    ↓
Load dataset → Split data → Create TF-IDF → Train SVM
    ↓
Save: svm_model.pkl, tfidf_vectorizer.pkl
```

### 2️⃣ **Runtime Phase** (Berulang)
```
User Input Komentar
    ↓
app.py (Flask)
    ↓
Preprocessing (5 stages)
    ↓
TF-IDF Vectorization
    ↓
SVM Prediction (dengan probability)
    ↓
Decision Engine (threshold 50%)
    ↓
Display Result (JSON + HTML)
```

---

## 🔧 Komponen Teknis

### Preprocessing Pipeline (5 Stages)

| Stage | Input | Output | Fungsi |
|---|---|---|---|
| 1 | Raw text | Unicode normalized | Normalisasi unicode (NFKD) |
| 2 | Normalized text | Obfuscation removed | Hapus karakter obfuscasi |
| 3 | Clean text | URL replaced | Ganti URL dengan "iniurl" |
| 4 | URL-replaced | Lowercase, no special chars | Hapus karakter khusus |
| 5 | Clean text | TF-IDF vector | Convert ke numerical features |

### Model Components

**Input**: Text komentar (raw)
```
"Buruan join casino online kami sekarang"
```

**Processing**:
```
Preprocessing → TF-IDF → SVM Model → Probability
```

**Output**: JSON dengan prediction + decision
```json
{
    "prediction": {
        "class": "Promosi Judi Online",
        "probability_judi": 0.85
    },
    "decision": {
        "verdict": "BLOKIR OTOMATIS",
        "action": "Komentar disembunyikan..."
    }
}
```

---

## 🚀 Quick Start (TL;DR)

```bash
# 1. Install
pip install -r requirements.txt

# 2. Save model
python save_model.py

# 3. Run
python app.py

# 4. Open browser
# http://localhost:5000
```

---

## ⚙️ Configuration Guide

### Mengubah Threshold Decision

**File**: `app.py` atau `config.py`

**Current**: 50% (if prob > 0.50 → BLOKIR)

**Cara mengubah**:
```python
# app.py line ~96
THRESHOLD = 0.60  # Ubah dari 0.50 ke 0.60
```

### Mengubah Port

**File**: `app.py` line terakhir

```python
# Dari:
app.run(debug=True, host='0.0.0.0', port=5000)

# Menjadi:
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Menambah Contoh Komentar

**File**: `templates/index.html` 

Cari section "Contoh Komentar", tambahkan:
```html
<button onclick="useExample('Komentar baru di sini')">
    Komentar baru
</button>
```

---

## 📊 Output Format

### HTML Response (GET /)
Halaman utama dengan interface

### JSON Response (POST /api/predict)

```json
{
    "error": false,
    "original_comment": "Buruan join casino online kami",
    "cleaned_comment": "buruan join casino online kami",
    "prediction": {
        "class": "Promosi Judi Online",
        "class_code": 1,
        "probability_non_judi": 0.15,
        "probability_judi": 0.85,
        "confidence": 0.85
    },
    "decision": {
        "verdict": "BLOKIR OTOMATIS",
        "action": "Komentar disembunyikan dan tidak akan dipublikasikan",
        "severity": "high",
        "color": "red"
    },
    "threshold": 0.5
}
```

### Error Response

```json
{
    "error": true,
    "message": "Komentar terlalu pendek (minimal 3 karakter)"
}
```

---

## 🧪 Testing Examples

### Test 1 - Normal Comment
```
Input: "Nonton vidio nih keren banget"
Expected: PUBLIKASI NORMAL (prob ≤ 50%)
```

### Test 2 - Judi Comment
```
Input: "Buruan join casino online kami sekarang"
Expected: BLOKIR OTOMATIS (prob > 50%)
```

### Test 3 - With Obfuscation
```
Input: "Mau main togel? klik link 🅿️🅻 jaminan jackpot"
Expected: BLOKIR OTOMATIS (prob > 50%)
```

---

## 🔍 API Reference

### Endpoint: POST /api/predict

**Request**:
```http
POST /api/predict HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
    "comment": "Teks komentar di sini"
}
```

**Response** (Success - 200):
```json
{
    "error": false,
    "original_comment": "...",
    "cleaned_comment": "...",
    "prediction": {...},
    "decision": {...}
}
```

**Response** (Error - 400/500):
```json
{
    "error": true,
    "message": "Deskripsi error"
}
```

### Endpoint: GET /api/info

**Request**:
```http
GET /api/info HTTP/1.1
Host: localhost:5000
```

**Response**:
```json
{
    "sistem": "Sistem Moderasi Preventif Judi Online YouTube",
    "model": "Support Vector Machine (SVM) Baseline",
    "threshold": 0.5,
    "preprocessing": [...],
    "feature_extraction": "TF-IDF Vectorization",
    "status": "ready"
}
```

---

## 🐛 Common Issues

| Issue | Solution |
|---|---|
| `ModuleNotFoundError: No module named 'flask'` | Run `pip install -r requirements.txt` |
| `FileNotFoundError: models/svm_model.pkl` | Run `python save_model.py` |
| `FileNotFoundError: dataset/dataset_judol_clean.csv` | Ensure dataset exists in parent folder |
| `Address already in use` | Change port in `app.py` |
| `Model performance is bad` | Check preprocessing dan training data |

---

## 📈 Performance Metrics

**Model**: SVM Baseline
**Vectorizer**: TF-IDF (5000 features)
**Threshold**: 50%

Expected performance (dari training):
- Training Accuracy: ~95-98%
- Test Accuracy: ~92-95%
- F1-Score: ~90-95%

---

## 🔐 Security Notes

1. **Input Validation**: Min/max length check
2. **Preprocessing**: Removes URLs dan special characters
3. **Model**: Deterministic untuk consistent results
4. **No Data Storage**: Comments tidak disimpan

---

## 🎓 Educational Purpose

Proyek ini adalah simulasi sistem moderasi untuk penelitian skripsi. Bertujuan untuk:
- Demonstrate ML pipeline (preprocessing → vectorization → classification)
- Implement decision engine untuk automated moderation
- Create user-friendly interface untuk model testing

---

## 📞 Quick Reference

### Key Parameters

```python
THRESHOLD = 0.50              # Decision threshold
MIN_COMMENT_LENGTH = 3        # Minimum input length
MAX_COMMENT_LENGTH = 1000     # Maximum input length
TFIDF_MAX_FEATURES = 5000     # TF-IDF features
SVM_KERNEL = 'linear'         # SVM kernel type
```

### File Sizes (Approximate)

| File | Size |
|---|---|
| `app.py` | ~12 KB |
| `save_model.py` | ~6 KB |
| `templates/index.html` | ~18 KB |
| `config.py` | ~8 KB |
| `svm_model.pkl` | ~5-10 MB |
| `tfidf_vectorizer.pkl` | ~3-5 MB |

---

## 📚 Related Documents

- **README.md** - Full documentation
- **SETUP_GUIDE.md** - Quick 5-minute setup
- **config.py** - All configurable parameters
- **app.py** - Backend implementation
- **templates/index.html** - Frontend UI

---

## ✅ Checklist Sebelum Production

- [ ] Install all dependencies
- [ ] Run `save_model.py` successfully
- [ ] Test dengan example comments
- [ ] Check threshold value
- [ ] Verify preprocessing works correctly
- [ ] Test API endpoints dengan cURL
- [ ] Check error handling
- [ ] Test di berbagai browser
- [ ] Verify model loading time (<5 sec)

---

**Last Updated**: 2026
**Status**: ✅ Ready for Use
**Version**: 1.0.0

---

## 🎯 Next Steps

1. **Setup**: Ikuti SETUP_GUIDE.md
2. **Testing**: Gunakan example comments
3. **Customization**: Edit threshold atau port sesuai kebutuhan
4. **Deployment**: Deploy ke server jika diperlukan

---

**Enjoy menggunakan Simulasi Sistem Moderasi Preventif! 🚀**
