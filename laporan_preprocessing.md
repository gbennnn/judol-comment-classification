# Laporan Tahap Preprocessing Data

## 1. Pendahuluan
Tahap preprocessing merupakan komponen kunci dalam penelitian klasifikasi komentar YouTube terkait promosi judi online. Data teks mentah umumnya mengandung variasi penulisan, karakter Unicode, simbol obfuscation, serta inkonsistensi format yang dapat menurunkan performa model machine learning. Oleh karena itu, preprocessing dilakukan untuk menghasilkan representasi teks yang lebih bersih, konsisten, dan informatif sebelum memasuki tahap ekstraksi fitur dan pemodelan.

Pada notebook penelitian ini, preprocessing difokuskan pada normalisasi teks komentar agar pola linguistik yang relevan terhadap kelas target (label 0 dan label 1) dapat ditangkap model secara lebih akurat.

## 2. Tujuan Preprocessing
Secara khusus, tahap preprocessing bertujuan untuk:

1. Mengidentifikasi keberadaan karakter non-ASCII/Unicode dalam komentar.
2. Menormalkan bentuk karakter Unicode agar konsisten.
3. Mengurangi teknik penyamaran kata (obfuscation) yang lazim digunakan pada komentar promosi judi online.
4. Membersihkan teks dari simbol yang tidak relevan.
5. Menstandarkan format teks (huruf kecil dan spasi).
6. Memastikan keluaran preprocessing bebas nilai kosong (null) pada kolom yang digunakan untuk analisis lanjutan.

## 3. Ruang Lingkup Data yang Diproses
Objek preprocessing adalah kolom teks komentar pada dataset berlabel, terutama:

- `comment_text` (teks mentah utama),
- `comment_text_unicode` (hasil normalisasi Unicode),
- `comment_text_clean` (hasil pembersihan akhir yang dipakai untuk EDA pasca-preprocessing dan tahap berikutnya).

Berdasarkan output notebook, jumlah data yang diproses adalah 37.216 komentar.

## 4. Tahapan Preprocessing yang Dilakukan

### 4.1. Audit Karakter Unicode pada Data Mentah
Langkah awal adalah mendeteksi komentar yang mengandung karakter non-ASCII menggunakan pola regex `[^\x00-\x7F]`. Tujuan langkah ini adalah memetakan tingkat heterogenitas karakter sebelum normalisasi.

Secara implementasi, sistem menghitung:

- jumlah komentar dengan karakter Unicode,
- persentase terhadap total data,
- contoh komentar Unicode untuk inspeksi manual.

Output notebook menunjukkan adanya 20.098 komentar yang mengandung karakter Unicode, sehingga normalisasi Unicode menjadi langkah yang sangat relevan.

### 4.2. Normalisasi Unicode Tahap Pertama (NFKC)
Setelah audit, dilakukan normalisasi Unicode menggunakan `unicodedata.normalize('NFKC', text)` pada setiap komentar. Normalisasi NFKC digunakan untuk menyatukan representasi karakter yang secara visual serupa tetapi memiliki kode Unicode berbeda, sehingga variasi penulisan dapat dikurangi.

Hasil normalisasi disimpan ke kolom baru `comment_text_unicode`, sehingga data asli pada `comment_text` tetap tersedia sebagai referensi.

### 4.3. Penyesuaian Struktur Kolom Sementara
Pada fase transisi preprocessing, kolom `text_length` (yang sebelumnya digunakan dalam EDA awal) dihapus dari DataFrame. Tujuannya adalah menjaga struktur data tetap fokus pada variabel yang relevan untuk pembersihan teks dan klasifikasi.

### 4.4. Inspeksi Manual Komentar Label 1
Notebook menampilkan sampel komentar label 1 sebelum dan sesudah transformasi untuk memverifikasi apakah normalisasi benar-benar memperbaiki keterbacaan token. Inspeksi manual ini penting karena komentar promosi judi online sering memanfaatkan karakter simbolik atau bentuk Unicode dekoratif untuk menghindari moderasi.

### 4.5. Normalisasi Obfuscation (Pemetaan Karakter Tersamar)
Tahap ini merupakan inti preprocessing domain-spesifik. Penelitian membangun `obfuscation_dict` untuk memetakan karakter tersamar menjadi bentuk standar, contohnya:

- huruf enclosed/circled seperti `🅿`, `ⓐ`, `Ⓐ` menjadi huruf alfabet biasa,
- angka emoji/circled seperti `4️⃣`, `⑦`, `❶` menjadi digit numerik standar,
- simbol substitusi umum seperti `@` menjadi `a`, `$` menjadi `s`, `!` menjadi `i`.

Penerapan dilakukan dengan pola regex gabungan (`re.compile("|".join(map(re.escape, keys)))`) agar seluruh pasangan karakter dapat diganti secara sistematis pada teks.

Signifikansi langkah ini tinggi karena pola promosi judi online sering menulis kata kunci secara tersamar untuk lolos dari filtering berbasis kata sederhana.

### 4.6. Normalisasi Unicode Tahap Lanjutan (NFKD + Penghapusan Combining Marks)
Setelah de-obfuscation, dilakukan normalisasi tambahan dengan `NFKD`, kemudian karakter combining (diakritik/penanda tambahan) dihapus. Tujuannya adalah menyederhanakan representasi karakter ke bentuk yang lebih stabil untuk tokenisasi dan vektorisasi.

Secara konseptual, langkah ini menurunkan noise ortografis tanpa mengubah makna inti teks.

### 4.7. Pembersihan Teks Akhir
Data yang telah dinormalisasi kemudian diproses melalui fungsi pembersihan final:

1. `lowercase`: seluruh teks diubah menjadi huruf kecil,
2. penghapusan karakter non alfanumerik: regex `[^a-z0-9\s]` diganti spasi,
3. normalisasi spasi: regex `\s+` menjadi satu spasi dan `strip()` untuk menghapus spasi tepi.

Output tahap ini disimpan pada kolom `comment_text_clean` yang menjadi representasi teks utama untuk analisis pasca-preprocessing.

### 4.8. Validasi Kualitas Hasil Preprocessing
Tahap validasi dilakukan dengan:

- pengecekan `df.info()` pada kolom hasil,
- pemeriksaan jumlah dan persentase null values per kolom,
- verifikasi khusus `comment_text_clean.isnull().sum()`.

Output notebook menunjukkan nilai null pada `comment_text_unicode` dan `comment_text_clean` adalah 0, sehingga data siap digunakan pada tahap EDA lanjutan dan pemodelan.

## 5. Ringkasan Alur Transformasi
Alur preprocessing yang diterapkan dapat diringkas sebagai berikut:

1. Deteksi komentar dengan karakter Unicode.
2. Normalisasi Unicode awal (NFKC) ke `comment_text_unicode`.
3. Pemetaan karakter obfuscation (regex + dictionary).
4. Normalisasi Unicode lanjutan (NFKD) dan penghapusan combining marks.
5. Pembersihan teks akhir (lowercase, hapus simbol, normalisasi spasi) ke `comment_text_clean`.
6. Validasi kualitas data (null check dan inspeksi output).

## 6. Kontribusi Tahap Preprocessing terhadap Klasifikasi
Preprocessing pada penelitian ini memberikan kontribusi metodologis sebagai berikut:

1. Meningkatkan konsistensi representasi teks sehingga fitur linguistik lebih mudah ditangkap model.
2. Mengurangi sparsity kosakata akibat variasi karakter Unicode dan teknik penyamaran.
3. Meningkatkan sensitivitas deteksi terhadap istilah promosi judi online yang ditulis secara obfuscated.
4. Menurunkan noise noninformatif yang berpotensi mengganggu proses pembelajaran model.

Dengan demikian, preprocessing tidak hanya bersifat teknis, tetapi juga strategis karena disesuaikan dengan karakteristik domain masalah (komentar promosi judi online).

## 7. Catatan Metodologis
Notebook menunjukkan beberapa eksperimen berulang selama proses pengembangan (misalnya pembaruan kamus obfuscation dan pengujian beberapa fungsi normalisasi). Dalam konteks laporan akademik, praktik tersebut dapat dipahami sebagai iterasi validasi metode untuk memperoleh konfigurasi preprocessing yang paling efektif sebelum tahap pemodelan.

## 8. Kesimpulan
Tahap preprocessing telah dilaksanakan secara bertahap dan komprehensif, dimulai dari audit karakter, normalisasi Unicode, de-obfuscation berbasis kamus, pembersihan teks, hingga validasi kualitas hasil. Keluaran utama berupa kolom `comment_text_clean` yang bersih, konsisten, dan bebas null menjadi fondasi yang kuat bagi tahap ekstraksi fitur serta pembangunan model klasifikasi Logistic Regression, Random Forest, dan SVM pada penelitian ini.
