# Asisten-catatan
# 🕶️ Asisten Shadow

<div align="center">

```
  ╔═══════════════════════════════════════════╗
  ║    ███████╗██╗  ██╗ █████╗ ██████╗       ║
  ║    ██╔════╝██║  ██║██╔══██╗██╔══██╗      ║
  ║    ███████╗███████║███████║██║  ██║       ║
  ║    ╚════██║██╔══██║██╔══██║██║  ██║       ║
  ║    ███████║██║  ██║██║  ██║██████╔╝       ║
  ╚═══════════════════════════════════════════╝
        A S I S T E N   S H A D O W
          Catatan Terenkripsi v2.0
```

![Python](https://img.shields.io/badge/Python-3.6+-blue?style=flat-square&logo=python)
![Platform](https://img.shields.io/badge/Platform-Termux%20%7C%20Linux%20%7C%20macOS-green?style=flat-square)
![License](https://img.shields.io/badge/Lisensi-MIT-orange?style=flat-square)
![Version](https://img.shields.io/badge/Versi-2.0%20Enhanced-purple?style=flat-square)

**Aplikasi catatan terenkripsi berbasis terminal dengan tampilan berwarna yang berjalan mulus di Termux, Linux, dan macOS.**

</div>

---

## ✨ Fitur

| Fitur | Keterangan |
|-------|-----------|
| 🔐 Enkripsi Catatan | Isi catatan dienkripsi dengan Base64 |
| 🔑 Kunci Per Catatan | Proteksi ekstra dengan password per catatan |
| 🛡️ Hashing SHA-256 | Password & kunci di-hash sebelum disimpan |
| 📝 Input Multi-Baris | Tulis catatan panjang dengan mudah |
| 🔍 Pencarian | Cari catatan berdasarkan kata kunci |
| 📊 Statistik | Lihat ringkasan catatan terkunci/terbuka |
| 💾 Export Catatan | Simpan catatan ke file JSON |
| 📥 Import Catatan | Muat catatan dari file JSON |
| 🎨 Tampilan Berwarna | UI berwarna penuh, ramah Termux |

---

## 📋 Persyaratan

- **Python 3.6+** (tanpa dependensi eksternal)
- Terminal yang mendukung warna ANSI (Termux, bash, zsh, dll.)

---

## 🚀 Instalasi & Menjalankan

### Di Termux (Android)

```bash
# 1. Install Python jika belum ada
pkg update && pkg install python git

# 2. Clone repositori
git clone https://github.com/suryadi346-star/Asisten-catatan.git
cd Asisten-catatan

# 3. Jalankan installer
bash install.sh

# 4. Jalankan aplikasi
python main.py
```

### Di Linux / macOS

```bash
# 1. Clone repositori
git clone https://github.com/suryadi346-star/Asisten-catatan.git
cd Asisten-catatan

# 2. Jalankan installer
bash install.sh

# 3. Jalankan aplikasi
python3 main.py
```

### Tanpa Clone (Download Langsung)

```bash
# Download dan langsung jalankan
python3 main.py
```

---

## 📂 Struktur File

```
Asisten-catatan/
├── main.py           # Aplikasi utama
├── install.sh        # Script instalasi otomatis
├── run.sh            # Script jalankan cepat (dibuat saat install)
├── requirements.txt  # Daftar dependensi (semua built-in)
├── README.md         # Dokumentasi ini
├── users.json        # Data pengguna (dibuat otomatis)
└── notes.json        # Data catatan (dibuat otomatis)
```

> **Catatan:** `users.json` dan `notes.json` dibuat otomatis saat pertama kali digunakan.

---

## 🎮 Cara Penggunaan

### 1. Daftar Akun Baru
```
[1] Register Akun Baru
→ Username (min 3 karakter)
→ Password (min 6 karakter)
```

### 2. Login
```
[2] Login
→ Masukkan username dan password
```

### 3. Tambah Catatan
```
Dashboard → [1] Tambah Catatan
→ Tulis catatan (Enter dua kali untuk selesai)
→ Opsional: tambahkan kunci untuk proteksi
```

### 4. Export Catatan
```
Dashboard → [7] Export Catatan
→ Masukkan nama file (misal: backup.json)
→ File tersimpan di direktori yang sama
```

### 5. Import Catatan
```
Dashboard → [8] Import Catatan
→ Masukkan nama file yang akan diimport
→ Catatan terkunci tidak bisa diimport/diekspor
```

---

## 🔒 Keamanan

- **Password pengguna** di-hash menggunakan SHA-256 sebelum disimpan
- **Kunci catatan** juga di-hash dengan SHA-256
- **Isi catatan** dienkripsi dengan Base64
- Data disimpan **lokal** di perangkat kamu, tidak dikirim ke mana pun

> ⚠️ Base64 adalah encoding, bukan enkripsi kriptografis penuh. Jangan simpan data sangat sensitif tanpa lapisan keamanan tambahan.

---

## 🖥️ Tampilan

```
  ╔═══════════════════════════════════════════╗
  ║           D A S H B O A R D              ║
  ╚═══════════════════════════════════════════╝

  👤  Pengguna : admin
  📊  Catatan  : 3 total  │  1 terkunci  │  2 terbuka

  ──────────────────────────────────────────────────
  [1] Tambah Catatan
  [2] Lihat Semua Catatan
  [3] Buka & Baca Catatan
  ...
```

---

## 🐛 Laporan Bug

Temukan masalah? Buka [Issues](https://github.com/suryadi346-star/Asisten-catatan/issues) dan sertakan:
- Deskripsi masalah
- Langkah reproduksi
- Versi Python dan platform yang digunakan

---

## 📄 Lisensi

Proyek ini dilisensikan di bawah **MIT License**.

---

<div align="center">

Dibuat dengan ❤️ oleh **Suryadi** · [⬆ Kembali ke atas](#️-asisten-shadow)

</div>
