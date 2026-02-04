# Mataram SSTB - Setup Guide

## 🎯 Tujuan
Menghubungkan aplikasi ke Google Earth Engine untuk mendapatkan deteksi bangunan yang akurat menggunakan AI.

## ⚠️ Masalah Saat Ini
- Demo Mode: Marker bangunan hanya sampel statis (tidak akurat)
- Deteksi Real: Membutuhkan koneksi ke Google Earth Engine
- Error: "no project found" - GEE memerlukan Google Cloud Project

## 🔧 Solusi: 3 Langkah Mudah

### Langkah 1: Buat Google Cloud Project
```bash
# Jalankan file ini:
create_project.bat
```

**Di browser yang terbuka:**
1. Klik tombol **"CREATE PROJECT"** (biru, pojok kanan atas)
2. Isi nama project: `mataram-sstb`
3. Klik **"CREATE"**
4. Tunggu 30 detik
5. **PENTING:** Salin **PROJECT ID** yang muncul (biasanya: `mataram-sstb-XXXXXX`)

### Langkah 2: Setup Project di Aplikasi
```bash
# Jalankan file ini:
setup_project.bat
```

**Saat diminta:**
1. Paste PROJECT ID yang Anda salin tadi
2. Tekan Enter
3. Browser akan terbuka untuk autentikasi
4. Login dengan akun Google yang sama
5. Klik **"Allow"**

### Langkah 3: Jalankan Aplikasi
```bash
start.bat
```

## ✅ Hasil yang Diharapkan

Setelah koneksi berhasil, aplikasi akan:
- ✅ Menampilkan peta satelit Google resolusi tinggi
- ✅ Mendeteksi bangunan menggunakan **Google Open Buildings V3 AI**
- ✅ Menampilkan outline merah di setiap bangunan yang terdeteksi
- ✅ Menghitung luas bangunan secara otomatis
- ✅ Menghitung pajak per bangunan

## 🎮 Alternatif: Tetap di Demo Mode

Jika Anda ingin tetap menggunakan Demo Mode (tanpa koneksi GEE):
- Demo Mode sudah cukup untuk presentasi konsep
- Data bangunan adalah simulasi (tidak real-time)
- Tidak memerlukan setup Google Cloud

## 📞 Troubleshooting

**Q: Browser tidak terbuka saat menjalankan create_project.bat**
A: Buka manual: https://console.cloud.google.com/projectcreate

**Q: Tidak bisa menemukan PROJECT ID**
A: Setelah create project, lihat di dashboard. Format: `nama-project-angka-random`

**Q: Error "permission denied"**
A: Pastikan akun Google Anda sudah terdaftar di Earth Engine: https://signup.earthengine.google.com
