# 🚀 SETUP GUIDE - Simulasi Sistem Moderasi Preventif

**Total waktu setup**: ~10 menit

## ✅ Langkah-Langkah Setup

### 1. Install Dependencies
```bash
cd web_moderasi
pip install -r requirements.txt
```

### 2. Simpan Model (PENTING!)
```bash
python save_model.py
```

**Pastikan output menunjukkan:**
```
✓ Model saved: models/svm_model.pkl
✓ Vectorizer saved: models/tfidf_vectorizer.pkl
✓ Preprocessing dict saved: models/preprocessing_dict.pkl
✓ All models saved successfully!
```

### 3. Jalankan Aplikasi
```bash
python app.py
```

**Output yang diharapkan:**
```
* Serving Flask app 'app'
* Debug mode: on
* Running on http://0.0.0.0:5000
```

### 4. Buka Browser
Navigasi ke: **http://localhost:5000**

---

## 📌 Struktur File Yang Dibuat

```
web_moderasi/
├── app.py                    # ← Flask backend
├── save_model.py             # ← Script menyimpan model
├── requirements.txt          # ← Dependencies
├── README.md                 # ← Dokumentasi lengkap
├── SETUP_GUIDE.md           # ← File ini
├── models/                   # ← Folder model (auto-created)
│   ├── svm_model.pkl
│   ├── tfidf_vectorizer.pkl
│   └── preprocessing_dict.pkl
└── templates/
    └── index.html           # ← Frontend interface
```

---

## 🎯 Fitur Utama

✅ **Real-time Analysis** - Analisis komentar secara langsung
✅ **Multi-stage Preprocessing** - Normalisasi unicode, obfuscation removal, dll
✅ **TF-IDF Vectorization** - Feature extraction
✅ **SVM Baseline Model** - Prediksi dengan probabilitas
✅ **Decision Engine** - Threshold-based decision (50%)
✅ **Beautiful UI** - Tailwind CSS responsive design
✅ **Visualization** - Probability bars dan results display

---

## 🧪 Testing Cepat

### Gunakan Contoh Komentar:

**Contoh 1** (Normal → Publikasi)
```
Nonton vidio nih keren banget
```

**Contoh 2** (Judi → Blokir)
```
Buruan join casino online kami sekarang
```

**Contoh 3** (Dengan Obfuscation → Blokir)
```
Mau main togel? klik link iniiii 🅿️🅻 jaminan jackpot
```

---

## ⚙️ Sistem Decision Engine

| Probabilitas | Keputusan | Tindakan |
|---|---|---|
| **≤ 50%** | ✅ PUBLIKASI NORMAL | Komentar dipublikasikan |
| **> 50%** | ❌ BLOKIR OTOMATIS | Komentar disembunyikan |

---

## 🔧 Pipeline Preprocessing

1. **Unicode Normalization** - Normalisasi karakter unicode
2. **Obfuscation Removal** - Hapus karakter obfuscation (🅿️, @, etc)
3. **URL Normalization** - Ganti URL dengan "iniurl"
4. **Text Cleaning** - Lowercase + remove special chars
5. **TF-IDF Conversion** - Convert ke numerical features

---

## 📊 API Endpoints

### POST /api/predict
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"comment": "Isi komentar di sini"}'
```

**Response**:
```json
{
  "error": false,
  "original_comment": "...",
  "cleaned_comment": "...",
  "prediction": {
    "class": "Promosi Judi Online",
    "class_code": 1,
    "probability_judi": 0.85,
    "confidence": 0.85
  },
  "decision": {
    "verdict": "BLOKIR OTOMATIS",
    "severity": "high"
  }
}
```

### GET /api/info
Dapatkan informasi sistem

---

## 🐛 Troubleshooting

| Masalah | Solusi |
|---|---|
| Model not found | Jalankan `python save_model.py` |
| Dataset not found | Pastikan `../dataset/dataset_judol_clean.csv` ada |
| Port 5000 sudah digunakan | Edit `app.py`, ubah port ke 5001 |
| ConnectionError | Pastikan Flask app sedang berjalan |

---

## 📈 Modifikasi (Opsional)

### Mengubah Threshold
Edit di `app.py`:
```python
THRESHOLD = 0.50  # Ubah ke nilai yang diinginkan
```

### Mengubah Port
Edit di `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Ubah 5000 ke port lain
```

### Menambah Example Comments
Edit di `templates/index.html`, cari section "Contoh Komentar" dan tambahkan:
```html
<button onclick="useExample('Komentar baru di sini')">
    <i class="fas fa-arrow-right"></i>
    "Komentar baru di sini"
</button>
```

---

## ✨ Fitur Tambahan

- ✅ Real-time character counter
- ✅ Input validation
- ✅ Keyboard shortcut (Ctrl + Enter untuk submit)
- ✅ Responsive mobile design
- ✅ Dark mode UI
- ✅ Smooth animations
- ✅ Error notifications

---

## 📞 Informasi Tambahan

- **Model**: SVM Baseline with linear kernel
- **Vectorizer**: TF-IDF (5000 features, unigrams)
- **Threshold**: 50% (customizable)
- **Preprocessing**: 5 stages
- **Status**: ✅ Production Ready

---

**Enjoy! 🎉**
