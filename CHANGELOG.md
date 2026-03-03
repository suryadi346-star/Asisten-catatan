# 📋 Changelog — Asisten Shadow

Semua perubahan penting dicatat di file ini.

---

## [2.0] - Enhanced Edition

### ✨ Ditambahkan
- Tampilan berwarna penuh dengan ANSI escape codes (mendukung Termux)
- Banner ASCII art di layar utama
- Input multi-baris untuk catatan panjang (Enter dua kali untuk selesai)
- Fitur **Import Catatan** dari file JSON
- Fungsi `getpass` untuk input password yang tersembunyi (tidak tampil di layar)
- Script instalasi otomatis `install.sh` (mendukung Termux, Linux, macOS)
- File `.gitignore` untuk keamanan data
- Dashboard menampilkan statistik real-time

### 🔧 Diperbaiki
- Struktur menu lebih rapi dan mudah dibaca
- Validasi input lebih ketat
- Pesan error/sukses lebih informatif dengan ikon

### 🎨 Perubahan Tampilan
- Header menggunakan box drawing characters (╔, ║, ╚, dst.)
- Daftar catatan menampilkan preview isi
- Warna konsisten: Cyan = judul, Hijau = sukses, Merah = error, Kuning = peringatan

---

## [1.0] - Initial Release

### ✨ Fitur Awal
- Registrasi dan login pengguna
- Tambah, lihat, edit, hapus catatan
- Enkripsi catatan dengan Base64
- Kunci per catatan dengan SHA-256
- Pencarian catatan
- Statistik catatan
- Export catatan ke JSON
