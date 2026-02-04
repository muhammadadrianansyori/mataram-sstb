# 🎯 REGISTRASI PROJECT KE EARTH ENGINE

## ⚠️ Masalah Saat Ini

Error: **"Project mataram-sstb is not registered to use Earth Engine"**

Artinya:
- ✅ Project Google Cloud sudah dibuat
- ✅ Autentikasi berhasil
- ❌ Project belum didaftarkan ke Earth Engine

## 🚀 Solusi: Registrasi Project

### Cara Otomatis (Mudah):
```bash
# Jalankan file ini:
register_project.bat
```

### Cara Manual:

1. **Buka halaman registrasi:**
   https://code.earthengine.google.com/register

2. **Pilih "Register a Cloud Project"**
   (Bukan "Register a Noncommercial or Commercial project")

3. **Isi form:**
   - **Project ID:** `mataram-sstb`
   - **Purpose:** Pilih **"Education"** atau **"Research"**
   - **Description:** (opsional) "Building monitoring for tax assessment"

4. **Klik "Submit"**

5. **Tunggu approval:**
   - Untuk Education/Research: Biasanya **instant** (langsung approved)
   - Anda akan melihat pesan "Registration successful"

6. **Tunggu propagasi:** 2-3 menit

7. **Jalankan aplikasi:**
   ```bash
   start.bat
   ```

## 📸 Screenshot Panduan

Saat di halaman registrasi:
```
┌─────────────────────────────────────────┐
│  Register a Cloud Project               │  ← PILIH INI
│  ○ Noncommercial                        │
│  ○ Commercial                           │
│                                         │
│  Project ID: [mataram-sstb]            │  ← ISI INI
│  Purpose: [Education ▼]                │  ← PILIH EDU/RESEARCH
│                                         │
│  [Submit]                              │  ← KLIK INI
└─────────────────────────────────────────┘
```

## ⏱️ Berapa Lama?

- **Registrasi:** 1 menit
- **Approval:** Instant (untuk Education/Research)
- **Propagasi:** 2-3 menit
- **Total:** Maksimal 5 menit

## ✅ Tanda Berhasil

Setelah registrasi berhasil:
1. Anda akan melihat pesan "Your project has been registered"
2. Saat menjalankan `start.bat`, tidak ada lagi error merah
3. Peta satelit langsung muncul dengan deteksi bangunan

## 🆘 Jika Ditolak (Jarang Terjadi)

Jika registrasi ditolak:
1. Coba pilih purpose yang berbeda
2. Atau gunakan **Demo Mode** untuk presentasi
3. Demo Mode sudah cukup untuk menunjukkan konsep aplikasi

## 💡 Catatan

- Earth Engine **GRATIS** untuk Education & Research
- Tidak ada biaya apapun
- Approval biasanya instant untuk non-commercial use
- Setelah registered, project bisa digunakan selamanya
