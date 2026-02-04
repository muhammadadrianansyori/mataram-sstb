# 🎯 Cara Menggunakan Aplikasi Mataram SSTB

## 🚀 Menjalankan Aplikasi

### Cara Termudah:
```bash
# Klik 2x file ini:
start.bat
```

Aplikasi akan terbuka di browser Anda secara otomatis.

---

## 🎛️ Menggunakan Kontrol

### **Panel Kiri (Tax Configuration)**

1. **Tax Rate (Rp / m²)**
   - Atur tarif pajak per meter persegi
   - Default: Rp 5,000/m²
   - Gunakan tombol +/- atau ketik langsung

2. **Inspector Radius (meters)**
   - Atur radius zona inspeksi
   - Range: 100-500 meter
   - Geser slider untuk mengubah

---

## 🗺️ Navigasi Peta

- **Zoom In/Out**: Scroll mouse atau tombol +/-
- **Pan (Geser)**: Klik dan drag peta
- **Layer Control**: Klik ikon layer di pojok kanan atas
  - Toggle "AI Building Footprints"
  - Toggle "Satellite" basemap

---

## 🔍 Memahami Visualisasi

### **Warna dan Simbol:**
- 🔴 **Polygon Merah** = Bangunan terdeteksi AI
- 🟢 **Lingkaran Hijau** = Zona inspector (area fokus)
- 🗺️ **Background** = Citra satelit Google resolusi tinggi

### **Status Indikator:**
- ✅ **Hijau**: "Connected to Google Earth Engine" = Koneksi aktif
- ✅ **Hijau**: "Real-time satellite data loaded successfully" = Data berhasil dimuat
- ⚠️ **Kuning**: Warning (biasanya minor)
- ❌ **Merah**: Error (perlu troubleshooting)

---

## 📊 Fitur yang Tersedia

### **Saat Ini:**
- ✅ Deteksi bangunan real-time
- ✅ Visualisasi footprint bangunan
- ✅ Peta satelit resolusi tinggi
- ✅ Konfigurasi tarif pajak
- ✅ Zona inspector yang dapat disesuaikan

### **Akan Datang (Future):**
- 📊 Klik bangunan untuk lihat detail area & pajak
- 📈 Dashboard statistik total
- 📅 Analisis perubahan dari waktu ke waktu
- 🗂️ Export data ke Excel/CSV

---

## 🎮 Mode Demo

Jika koneksi GEE gagal, aplikasi akan menawarkan **Demo Mode**.

**Cara Mengaktifkan:**
1. Klik tombol "🎮 Launch Demo Mode"
2. Peta akan menampilkan data simulasi
3. Cocok untuk presentasi offline

**Cara Kembali ke Real Mode:**
1. Klik tombol "🔄 Try Real Mode Again"
2. Pastikan koneksi internet aktif

---

## 🔧 Troubleshooting

### **Aplikasi Tidak Terbuka**
```bash
# Cek apakah Streamlit terinstall:
streamlit --version

# Jika error, reinstall:
pip install streamlit
```

### **Peta Tidak Muncul**
- Refresh browser (F5)
- Cek koneksi internet
- Coba mode demo

### **Error "GEE Not Connected"**
```bash
# Re-authenticate:
auth_gee.bat
```

---

## 💡 Tips Penggunaan

1. **Untuk Presentasi:**
   - Gunakan Demo Mode jika internet tidak stabil
   - Zoom ke area yang menarik sebelum presentasi
   - Screenshot peta untuk dokumentasi

2. **Untuk Analisis:**
   - Atur tax rate sesuai NJOP daerah
   - Bandingkan berbagai radius inspector
   - Catat area dengan bangunan padat

3. **Untuk Pengembangan:**
   - Lihat file `app.py` untuk modifikasi
   - Tambahkan fitur di sidebar
   - Integrasikan dengan database pajak

---

## 📞 Bantuan Lebih Lanjut

**File Dokumentasi:**
- `SETUP_GUIDE.md` - Panduan setup lengkap
- `CARA_REGISTRASI.md` - Cara registrasi GEE
- `walkthrough.md` - Dokumentasi teknis lengkap

**Jika Masih Bermasalah:**
- Cek semua file `.md` di folder `d:/bps`
- Jalankan `auth_gee.bat` untuk re-authenticate
- Gunakan Demo Mode untuk sementara

---

## 🎉 Selamat Menggunakan!

Aplikasi **Mataram SSTB Smart Tax Inspector** siap membantu Anda memonitor bangunan dan menghitung potensi pajak dengan teknologi satelit dan AI! 🛰️
