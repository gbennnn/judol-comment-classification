#!/usr/bin/env markdown
# 🚀 GETTING STARTED - Simulasi Sistem Moderasi Preventif

> Panduan lengkap untuk memulai dalam **5 menit**

---

## ⚡ Quick Start (3 Langkah)

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Save Model
```bash
python save_model.py
```
**Tunggu hingga muncul:**
```
✓ All models saved successfully!
```

### 3️⃣ Run Application
```bash
python app.py
```
**Buka browser ke:**
```
http://localhost:5000
```

---

## 📚 Dokumentasi (Pilih sesuai kebutuhan)

| Kebutuhan | File | Waktu |
|-----------|------|-------|
| **Setup cepat** | `SETUP_GUIDE.md` | 5 min |
| **Dokumentasi lengkap** | `README.md` | 30 min |
| **Index lengkap** | `INDEX.md` | 15 min |
| **File reference** | `SUMMARY.md` | 10 min |
| **Checklist** | `CHECKLIST.md` | 5 min |

---

## 🧪 Test Langsung

Setelah app running, coba contoh ini:

**✅ Contoh 1 (Publikasi):**
```
Nonton vidio nih keren banget
```

**❌ Contoh 2 (Blokir):**
```
Buruan join casino online kami sekarang
```

---

## 📁 Apa yang Telah Dibuat

### Backend
- ✓ `app.py` - Flask application
- ✓ `save_model.py` - Save trained model
- ✓ `config.py` - Configuration

### Frontend
- ✓ `templates/index.html` - Beautiful UI

### Documentation
- ✓ `README.md` - Full docs
- ✓ `SETUP_GUIDE.md` - Quick setup
- ✓ `INDEX.md` - Documentation index
- ✓ `SUMMARY.md` - Overview
- ✓ `CHECKLIST.md` - Verification list
- ✓ `GETTING_STARTED.md` - This file

---

## ⚠️ Penting!

🔴 **HARUS** jalankan `python save_model.py` sebelum `python app.py`

```bash
# ✓ Benar
python save_model.py  # 1. Save model first
python app.py         # 2. Then run app

# ✗ Salah
python app.py         # ❌ Model belum ada!
```

---

## 🎯 Fitur Utama

✅ Real-time comment analysis
✅ Multi-stage preprocessing  
✅ SVM classification dengan probabilitas
✅ Decision engine (threshold 50%)
✅ Beautiful Tailwind UI
✅ Responsive design
✅ Smooth animations

---

## 🆘 Troubleshooting

### Port sudah digunakan?
Edit `app.py`, ubah:
```python
port=5000  # ubah ke 5001, 5002, dst
```

### Model tidak ditemukan?
Jalankan:
```bash
python save_model.py
```

### Dataset tidak ditemukan?
Pastikan file ada di:
```
../dataset/dataset_judol_clean.csv
```

---

## 📞 Need Help?

1. Check `SETUP_GUIDE.md` untuk setup issues
2. Check `README.md` untuk detailed information
3. Check `CHECKLIST.md` untuk verification
4. Check `SUMMARY.md` untuk quick reference

---

## 🎓 What You'll Learn

- Machine Learning pipeline
- Text preprocessing techniques
- TF-IDF vectorization
- SVM classification
- Flask web development
- Real-time prediction system

---

## ✨ Ready?

```bash
# 1. Install
pip install -r requirements.txt

# 2. Save model
python save_model.py

# 3. Run
python app.py

# 4. Enjoy!
# Open http://localhost:5000
```

---

**Next:** Read `SETUP_GUIDE.md` untuk setup lengkap atau langsung jalankan 3 langkah di atas!

🚀 **Let's go!**
