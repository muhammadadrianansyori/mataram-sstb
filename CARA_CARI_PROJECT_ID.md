# Cara Menemukan Google Cloud PROJECT ID

## 📍 Lokasi Project ID

### Metode 1: Di Google Cloud Console (Paling Mudah)

1. **Buka:** https://console.cloud.google.com
2. **Lihat bagian atas halaman** (navigation bar)
3. **Klik dropdown** di sebelah logo Google Cloud (biasanya ada nama project)
4. **Project ID akan terlihat** di bawah nama project

```
Contoh tampilan:
┌─────────────────────────────┐
│ mataram-sstb               │  ← Nama Project
│ ID: mataram-sstb-439205    │  ← INI YANG ANDA BUTUHKAN!
└─────────────────────────────┘
```

### Metode 2: Saat Membuat Project Baru

Ketika Anda klik "CREATE" saat membuat project:
- Halaman akan refresh
- Di bagian atas akan muncul notifikasi: "Project created"
- **Project ID** akan terlihat di dashboard atau di dropdown project selector

### Metode 3: Di Halaman Dashboard

1. Setelah login ke Google Cloud Console
2. Lihat **Dashboard** (halaman utama)
3. Ada card "Project Info" di sebelah kiri
4. **Project ID** tertulis di sana

## 🎯 Format Project ID

Project ID biasanya berbentuk:
- `nama-yang-anda-buat-123456` (angka random di belakang)
- Contoh: `mataram-sstb-439205`
- Atau: `my-project-847392`

## ⚠️ Catatan Penting

- **Project ID ≠ Project Name**
  - Project Name: Bisa diubah, bisa ada spasi (contoh: "Mataram SSTB")
  - Project ID: Tidak bisa diubah, tidak ada spasi (contoh: "mataram-sstb-439205")

- **Yang Anda butuhkan adalah PROJECT ID**, bukan Project Name!

## 🚀 Langkah Selanjutnya

Setelah menemukan Project ID:
1. Salin/copy Project ID tersebut
2. Jalankan: `setup_project.bat`
3. Paste Project ID saat diminta
4. Tekan Enter

## 📸 Screenshot Bantuan

Lihat gambar `gcp_project_id_guide.webp` di folder ini untuk panduan visual.

## 🆘 Jika Tidak Menemukan Project ID

**Kemungkinan 1:** Anda belum membuat project
- Solusi: Jalankan `create_project.bat` terlebih dahulu

**Kemungkinan 2:** Project belum selesai dibuat
- Solusi: Tunggu 30-60 detik, lalu refresh halaman

**Kemungkinan 3:** Login dengan akun yang berbeda
- Solusi: Pastikan login dengan akun Google yang sama dengan saat autentikasi Earth Engine
