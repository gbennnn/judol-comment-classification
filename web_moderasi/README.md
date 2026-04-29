# 🛡️ Simulasi Sistem Moderasi Preventif - Judi Online Detection

Website simulasi sistem moderasi preventif untuk mendeteksi komentar promosi judi online pada platform YouTube menggunakan Model Machine Learning **SVM Baseline**.

## 📋 Daftar Isi

- [Fitur](#fitur)
- [Arsitektur Sistem](#arsitektur-sistem)
- [Instalasi](#instalasi)
- [Cara Penggunaan](#cara-penggunaan)
- [Komponen Sistem](#komponen-sistem)
- [Pipeline Preprocessing](#pipeline-preprocessing)
- [Decision Engine](#decision-engine)

## ✨ Fitur

- **Real-time Comment Analysis**: Analisis komentar secara real-time
- **Multi-stage Preprocessing**: Normalisasi unicode, obfuscation removal, URL normalization
- **TF-IDF Vectorization**: Konversi teks menjadi representasi numerik
- **SVM Classification**: Model SVM Baseline untuk prediksi
- **Decision Engine**: Sistem keputusan berbasis threshold probabilitas
- **Beautiful UI**: Interface modern dengan Tailwind CSS
- **Responsive Design**: Kompatibel dengan desktop dan mobile
- **Real-time Visualization**: Visualisasi probabilitas dan hasil prediksi

## 🏗️ Arsitektur Sistem

```
┌─────────────────┐
│  Input Komentar │
└────────┬────────┘
         │
    ┌────▼──────────────────┐
    │ Modul Pra-pemrosesan  │
    │  - Unicode Normalize  │
    │  - Obfuscation Removal│
    │  - URL Normalization  │
    │  - Text Cleaning      │
    └────┬──────────────────┘
         │
    ┌────▼──────────────────┐
    │ Ekstraksi Fitur      │
    │  (TF-IDF Vectorizer)  │
    └────┬──────────────────┘
         │
    ┌────▼──────────────────┐
    │ Model Klasifikasi    │
    │ (SVM Baseline)        │
    │ Output: Probability   │
    └────┬──────────────────┘
         │
    ┌────▼──────────────────┐
    │ Decision Engine       │
    │ Threshold = 50%       │
    └────┬──────────────────┘
         │
    ┌────▼──────────────────┐
    │ Tindakan Preventif   │
    │ - Publikasi Normal    │
    │ - Blokir Otomatis     │
    └──────────────────────┘
```

## 🚀 Instalasi

### Prasyarat
- Python 3.8+
- pip (Python package manager)

### Step 1: Persiapan Environment

```bash
# Masuk ke folder project
cd web_moderasi

# Buat virtual environment (opsional tapi recommended)
python -m venv venv

# Activate virtual environment
# Untuk Windows:
venv\Scripts\activate
# Untuk Linux/Mac:
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Menyimpan Model

Sebelum menjalankan aplikasi, Anda perlu menyimpan model SVM dan TF-IDF vectorizer:

```bash
# Jalankan script untuk save model
python save_model.py
```

**Catatan**: Script ini akan membaca file `dataset/dataset_judol_clean.csv` dari folder parent dan menyimpan model di folder `models/`.

**Output yang diharapkan**:
```
Loading dataset...
Dataset shape: (xxx, 4)
Training set: (xxx, 1)
Test set: (xxx, 1)

Creating TF-IDF vectorizer...
TF-IDF shape: (xxx, 5000)

Training SVM Baseline Model...
Training Score: 0.xxxx
Test Score: 0.xxxx

Saving model and vectorizer...
✓ Model saved: models/svm_model.pkl
✓ Vectorizer saved: models/tfidf_vectorizer.pkl
✓ Preprocessing dict saved: models/preprocessing_dict.pkl

✓ All models saved successfully!
```

## 💻 Cara Penggunaan

### Menjalankan Aplikasi

```bash
# Jalankan Flask app
python app.py
```

Aplikasi akan berjalan di `http://localhost:5000`

### Menggunakan Interface Web

1. **Buka Browser**: Navigasi ke `http://localhost:5000`
2. **Input Komentar**: Masukkan komentar di textarea
3. **Klik "Analisis Komentar"**: Submit untuk analisis
4. **Lihat Hasil**: Sistem akan menampilkan:
   - Prediksi klasifikasi
   - Probabilitas (Non-Judi vs Judi)
   - Decision (Publikasi Normal / Blokir Otomatis)
   - Teks setelah preprocessing

### Contoh Input

**Contoh 1 - Komentar Normal** (Expected: Publikasi Normal)
```
Nonton vidio nih keren banget
```

**Contoh 2 - Komentar Judi** (Expected: Blokir Otomatis)
```
Buruan join casino online kami sekarang
```

**Contoh 3 - Dengan Obfuscation** (Expected: Blokir Otomatis)
```
Mau main togel? klik link iniiii 🅿️🅻 jaminan jackpot
```

## 🔧 Komponen Sistem

### 1. **Backend (Flask)**

**File**: `app.py`

- Load model SVM dan TF-IDF vectorizer
- Implement preprocessing pipeline
- API endpoint `/api/predict` untuk prediksi
- Decision engine dengan threshold 50%
- Error handling dan validation

**API Endpoints**:

- `GET /`: Halaman utama (HTML)
- `POST /api/predict`: Submit komentar untuk analisis
  - Request: `{"comment": "teks komentar"}`
  - Response: Prediction results + decision
- `GET /api/info`: Informasi sistem

### 2. **Frontend (HTML/CSS/JS)**

**File**: `templates/index.html`

- Beautiful UI dengan Tailwind CSS
- Real-time character counter
- Input validation
- Visualization of probabilities
- Display decision dan action
- Example comments untuk testing

### 3. **Model Training & Saving**

**File**: `save_model.py`

- Load dataset bersih dari CSV
- Split data (80% train, 20% test)
- Create TF-IDF vectorizer
- Train SVM model
- Save model dan vectorizer ke pickle files

## 🔄 Pipeline Preprocessing

### 1. Unicode Normalization (NFKD)
Mengubah karakter unicode yang tidak standard menjadi bentuk canonical.

**Contoh**:
```
Input: "café" (dengan kombinasi characters)
Output: "cafe" (normalized)
```

### 2. Obfuscation Character Replacement
Mengganti karakter yang sengaja diubah untuk menghindari deteksi.

**Contoh Obfuscation Characters**:
- 🅿️ → "p" (Judi → Jud i → J ud i)
- 🅻 → "l"
- ⓤ → "u"
- 4️⃣ → "4"
- @ → "a"

**Contoh**:
```
Input: "🅿️🅻 jaminan jackpot"
Output: "pl jaminan jackpot"
```

### 3. URL Normalization
Mengganti semua URL dengan placeholder "iniurl".

**Contoh**:
```
Input: "join sekarang di https://example.com/judi"
Output: "join sekarang di iniurl"
```

### 4. Text Cleaning
- Lowercase semua teks
- Hapus karakter special (keep hanya alphanumeric + space)
- Hapus spasi berlebih

**Contoh**:
```
Input: "Join!!!  SEKARANG @@ Link #$%"
Output: "join sekarang link"
```

## ⚙️ Decision Engine

### Threshold-based Decision System

```
IF probability_judi > 0.50:
    decision = "BLOKIR OTOMATIS"
    action = "Komentar disembunyikan dan tidak akan dipublikasikan"
    severity = "high"
ELSE:
    decision = "PUBLIKASI NORMAL"
    action = "Komentar akan dipublikasikan normalmente"
    severity = "low"
```

### Interpretation

| Probability Range | Decision | Tindakan |
|---|---|---|
| 0 - 50% | PUBLIKASI NORMAL | ✓ Komentar dipublikasikan |
| 50% - 100% | BLOKIR OTOMATIS | ✗ Komentar disembunyikan |

## 📊 Output Prediksi

Sistem mengembalikan response JSON dengan struktur:

```json
{
    "error": false,
    "original_comment": "teks asli",
    "cleaned_comment": "teks setelah preprocessing",
    "prediction": {
        "class": "Promosi Judi Online",
        "class_code": 1,
        "probability_non_judi": 0.25,
        "probability_judi": 0.75,
        "confidence": 0.75
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

## 📁 Struktur Folder

```
web_moderasi/
├── app.py                          # Flask main app
├── save_model.py                   # Script untuk save model
├── requirements.txt                # Dependencies
├── README.md                       # Dokumentasi ini
├── models/                         # Folder untuk menyimpan model
│   ├── svm_model.pkl              # Model SVM (dibuat saat save_model.py dijalankan)
│   ├── tfidf_vectorizer.pkl       # TF-IDF vectorizer (dibuat saat save_model.py dijalankan)
│   └── preprocessing_dict.pkl     # Obfuscation dict (dibuat saat save_model.py dijalankan)
└── templates/
    └── index.html                  # Frontend interface
```

## 🧪 Testing

### Gunakan Example Comments

Website menyediakan beberapa contoh komentar:

1. **Normal Comment**: "Nonton vidio nih keren banget"
2. **Judi Comment**: "Buruan join casino online kami sekarang"
3. **Obfuscated**: "Mau main togel? klik link iniiii..." (dengan emoji obfuscation)

Klik salah satu untuk auto-fill textarea, lalu klik "Analisis Komentar".

### API Testing dengan cURL

```bash
# Test prediksi
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"comment": "Buruan join casino online kami sekarang"}'

# Get system info
curl http://localhost:5000/api/info
```

## ⚠️ Troubleshooting

### Error: Model not found

**Solusi**: Jalankan `python save_model.py` terlebih dahulu untuk generate model files.

### Error: Dataset not found

**Solusi**: Pastikan file `dataset/dataset_judol_clean.csv` ada di folder parent (`../dataset/`).

### Port sudah digunakan

**Solusi**: Ubah port di `app.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)  # Change 5000 to 5001
```

### Model performance rendah

**Solusi**: Periksa:
1. Dataset sudah di-preprocessing dengan benar
2. Train/test split ratio sudah sesuai
3. Model sudah converged saat training

## 📝 License

Proyek ini merupakan bagian dari skripsi untuk klasifikasi komentar judi online.

## 👨‍💻 Author

Dibuat sebagai simulasi sistem moderasi preventif untuk penelitian skripsi.

---

**Last Updated**: 2026
**Status**: ✓ Production Ready
