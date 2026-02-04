# Panduan Deployment ke Streamlit Cloud 🚀

Panduan ini akan membantu Anda mempublikasikan aplikasi "Mataram SSTB" agar bisa diakses orang lain melalui link web gratis (Streamlit Community Cloud).

## Persiapan Awal
1.  Pastikan kode Anda sudah stabil.
2.  Anda wajib memiliki akun:
    *   **GitHub** (untuk menyimpan kode).
    *   **Streamlit Cloud** (untuk hosting).
    *   **Google Cloud** (untuk akses GEE).

---

## Langkah 1: Upload Kode ke GitHub

1.  Buat Repository baru di GitHub (misal: `mataram-sstb-app`).
2.  Upload file-file berikut ke repository tersebut:
    *   `app.py`
    *   `utils.py`
    *   `requirements.txt`
    *   `simple_building_check.ipynb` (opsional, jika ingin disimpan)
    *   Jangan upload folder `.venv` atau file credentials rahasia!

## Langkah 2: Buat Service Account Key (Dibutuhkan untuk Streamlit Cloud)
Karena Streamlit Cloud berjalan di server luar, kita butuh "kunci rahasia" agar dia bisa akses Google Earth Engine.

1.  Buka [Google Cloud Console > IAM & Admin > Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts).
2.  Pilih Project Anda (`mataram-sstb`).
3.  Klik **+ CREATE SERVICE ACCOUNT**.
    *   Name: `streamlit-bot`
    *   Access: Pilih Role **Editor** atau **Earth Engine Resource Writer**.
4.  Setelah dibuat, klik email service account tersebut di daftar.
5.  Masuk ke tab **KEYS** > **ADD KEY** > **Create new key** > **JSON**.
6.  File `.json` akan terdownload otomatis. **JAGA FILE INI! JANGAN DI-UPLOAD KE GITHUB**.
7.  Buka file `.json` tersebut dengan Notepad, copy semua isinya.

## Langkah 3: Deploy di Streamlit Cloud

1.  Buka [share.streamlit.io](https://share.streamlit.io).
2.  Login dengan GitHub.
3.  Klik **New app**.
4.  Pilih Repository GitHub yang tadi Anda buat (`mataram-sstb-app`).
5.  Branch: `main` (atau `master`).
6.  Main file path: `app.py`.
7.  **PENTING**: Sebelum klik Deploy, klik **Advanced settings...**
8.  Di bagian **Secrets**, paste isi file JSON tadi dengan format berikut:

```toml
[gee_service_account]
type = "service_account"
project_id = "mataram-sstb"
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----..."
client_email = "..."
client_id = "..."
auth_uri = "..."
token_uri = "..."
auth_provider_x509_cert_url = "..."
client_x509_cert_url = "..."
```

> **Tips:** Cukup copy-paste seluruh isi JSON Anda, lalu tambahkan `[gee_service_account]` di baris paling atas. Pastikan formatnya mirip di atas.

9.  Klik **Save**.
10. Klik **Deploy**.

## Langkah 4: Selesai! 🎉
Tunggu beberapa menit hingga proses "Oven" selesai. Jika berhasil, Anda akan mendapatkan link (contoh: `https://mataram-sstb-app.streamlit.app`) yang bisa dibagikan ke siapa saja!

---

### Troubleshooting
*   **Error "No project found"**: Cek kembali Secrets Anda, pastikan `project_id` benar.
*   **Error "Private Key invalid"**: Pastikan saat copy paste `private_key`, seluruh karakter termasuk garisn baru (`\n`) tercopy dengan benar.
