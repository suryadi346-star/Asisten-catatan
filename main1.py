"""
ASISTEN SHADOW - Aplikasi Catatan Terenkripsi
Versi 2.0 - Enhanced Edition

Fitur:
- Registrasi dan Login pengguna
- Catatan terenkripsi dengan Base64
- Kunci/Password untuk catatan pribadi
- Pencarian catatan
- Statistik catatan
- Export/Import catatan
"""

import os
import json
import base64
import hashlib
import datetime
from typing import Dict, List, Optional, Tuple

# ==================== KONSTANTA ====================
USER_FILE = "users.json"
NOTES_FILE = "notes.json"
VERSION = "2.0"

# ==================== HELPER FUNCTIONS ====================

def load_data(filename: str) -> Dict:
    """Memuat data dari file JSON"""
    if not os.path.exists(filename):
        return {}

    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, IOError):
        return {}


def save_data(filename: str, data: Dict) -> bool:
    """Menyimpan data ke file JSON"""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except IOError:
        print("❌ Gagal menyimpan data!")
        return False


def hash_password(password: str) -> str:
    """Hash password menggunakan SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


def encode_text(text: str) -> str:
    """Encode teks dengan Base64"""
    return base64.b64encode(text.encode()).decode()


def decode_text(text_b64: str) -> str:
    """Decode teks dari Base64"""
    try:
        return base64.b64decode(text_b64.encode()).decode()
    except Exception:
        return "[ERROR: Data rusak]"


def get_timestamp() -> str:
    """Mendapatkan timestamp saat ini"""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def clear_screen():
    """Membersihkan layar konsol"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title: str):
    """Mencetak header dengan format yang rapi"""
    print("\n" + "="*50)
    print(f"{title:^50}")
    print("="*50)


def print_menu(options: List[str]):
    """Mencetak menu dengan format yang rapi"""
    print("-"*50)
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")
    print("-"*50)


def get_input(prompt: str, required: bool = True) -> str:
    """Mendapatkan input dengan validasi"""
    while True:
        value = input(prompt).strip()
        if not required or value:
            return value
        print("❌ Input tidak boleh kosong!")


def confirm_action(message: str) -> bool:
    """Konfirmasi aksi dari pengguna"""
    response = input(f"{message} (y/n): ").lower().strip()
    return response == 'y'


# ==================== USER MANAGEMENT ====================

class UserManager:
    """Mengelola registrasi dan autentikasi pengguna"""

    @staticmethod
    def register(username: str, password: str) -> bool:
        """Registrasi pengguna baru"""
        if not username or not password:
            print("❌ Username dan password tidak boleh kosong!")
            return False

        if len(username) < 3:
            print("❌ Username minimal 3 karakter!")
            return False

        if len(password) < 6:
            print("❌ Password minimal 6 karakter!")
            return False

        users = load_data(USER_FILE)

        if username in users:
            print("❌ Username sudah digunakan!")
            return False

        users[username] = {
            "password": hash_password(password),
            "created_at": get_timestamp(),
            "last_login": None
        }

        if save_data(USER_FILE, users):
            print("✔ Registrasi berhasil! Silakan login.")
            return True
        return False

    @staticmethod
    def login(username: str, password: str) -> bool:
        """Login pengguna"""
        users = load_data(USER_FILE)

        if username not in users:
            print("❌ Username tidak ditemukan!")
            return False

        if users[username]["password"] != hash_password(password):
            print("❌ Password salah!")
            return False

        # Update last login
        users[username]["last_login"] = get_timestamp()
        save_data(USER_FILE, users)

        return True

    @staticmethod
    def get_user_info(username: str) -> Optional[Dict]:
        """Mendapatkan informasi pengguna"""
        users = load_data(USER_FILE)
        return users.get(username)


# ==================== NOTES MANAGEMENT ====================

class NotesManager:
    """Mengelola catatan pengguna"""

    @staticmethod
    def add_note(username: str, content: str, lock_key: str = "") -> bool:
        """Menambahkan catatan baru"""
        if not content:
            print("❌ Catatan tidak boleh kosong!")
            return False

        notes = load_data(NOTES_FILE)

        if username not in notes:
            notes[username] = []

        note_data = {
            "id": len(notes[username]) + 1,
            "content": encode_text(content),
            "lock": hash_password(lock_key) if lock_key else "",
            "created_at": get_timestamp(),
            "updated_at": get_timestamp(),
            "is_locked": bool(lock_key)
        }

        notes[username].append(note_data)

        if save_data(NOTES_FILE, notes):
            print("✔ Catatan berhasil ditambahkan!")
            return True
        return False

    @staticmethod
    def get_notes(username: str) -> List[Dict]:
        """Mendapatkan semua catatan pengguna"""
        notes = load_data(NOTES_FILE)
        return notes.get(username, [])

    @staticmethod
    def display_notes_list(username: str) -> List[Dict]:
        """Menampilkan daftar catatan"""
        notes = NotesManager.get_notes(username)

        if not notes:
            print("\n⚠ Belum ada catatan.")
            return []

        print_header("DAFTAR CATATAN")
        print(f"{'No':<5} {'Status':<8} {'Preview':<30} {'Terakhir Diubah':<20}")
        print("-"*70)

        for i, note in enumerate(notes, 1):
            status = "🔒 Terkunci" if note["is_locked"] else "🔓 Terbuka"
            content = decode_text(note["content"])
            preview = content[:27] + "..." if len(content) > 27 else content

            if note["is_locked"]:
                preview = "[Catatan Terkunci]"

            print(f"{i:<5} {status:<8} {preview:<30} {note['updated_at']:<20}")

        print("-"*70)
        print(f"Total: {len(notes)} catatan\n")
        return notes

    @staticmethod
    def view_note(username: str, index: int) -> bool:
        """Melihat isi catatan"""
        notes = NotesManager.get_notes(username)

        if not 0 <= index < len(notes):
            print("❌ Nomor catatan tidak valid!")
            return False

        note = notes[index]

        if note["is_locked"]:
            key = get_input("🔑 Masukkan kunci catatan: ")
            if hash_password(key) != note["lock"]:
                print("❌ Kunci salah!")
                return False

        print_header("ISI CATATAN")
        print(f"Dibuat: {note['created_at']}")
        print(f"Diubah: {note['updated_at']}")
        print("-"*50)
        print(decode_text(note["content"]))
        print("-"*50)
        return True

    @staticmethod
    def edit_note(username: str, index: int, new_content: str, new_lock: Optional[str] = None) -> bool:
        """Mengedit catatan"""
        notes = load_data(NOTES_FILE)
        user_notes = notes.get(username, [])

        if not 0 <= index < len(user_notes):
            print("❌ Nomor catatan tidak valid!")
            return False

        note = user_notes[index]

        # Verifikasi kunci jika catatan terkunci
        if note["is_locked"]:
            key = get_input("🔑 Masukkan kunci saat ini: ")
            if hash_password(key) != note["lock"]:
                print("❌ Kunci salah!")
                return False

        # Update catatan
        note["content"] = encode_text(new_content)
        note["updated_at"] = get_timestamp()

        # Update kunci jika diminta
        if new_lock is not None:
            if new_lock == "":
                note["lock"] = ""
                note["is_locked"] = False
            else:
                note["lock"] = hash_password(new_lock)
                note["is_locked"] = True

        if save_data(NOTES_FILE, notes):
            print("✔ Catatan berhasil diedit!")
            return True
        return False

    @staticmethod
    def delete_note(username: str, index: int) -> bool:
        """Menghapus catatan"""
        notes = load_data(NOTES_FILE)
        user_notes = notes.get(username, [])

        if not 0 <= index < len(user_notes):
            print("❌ Nomor catatan tidak valid!")
            return False

        note = user_notes[index]

        # Verifikasi kunci jika terkunci
        if note["is_locked"]:
            key = get_input("🔑 Masukkan kunci catatan: ")
            if hash_password(key) != note["lock"]:
                print("❌ Kunci salah!")
                return False

        # Konfirmasi
        if not confirm_action("⚠ Yakin hapus catatan ini?"):
            print("❌ Penghapusan dibatalkan.")
            return False

        del user_notes[index]

        if save_data(NOTES_FILE, notes):
            print("✔ Catatan berhasil dihapus!")
            return True
        return False

    @staticmethod
    def search_notes(username: str, keyword: str) -> List[Tuple[int, Dict]]:
        """Mencari catatan berdasarkan keyword"""
        notes = NotesManager.get_notes(username)
        results = []

        for i, note in enumerate(notes):
            if note["is_locked"]:
                continue

            content = decode_text(note["content"]).lower()
            if keyword.lower() in content:
                results.append((i, note))

        return results

    @staticmethod
    def get_statistics(username: str) -> Dict:
        """Mendapatkan statistik catatan"""
        notes = NotesManager.get_notes(username)

        total = len(notes)
        locked = sum(1 for note in notes if note["is_locked"])
        unlocked = total - locked

        return {
            "total": total,
            "locked": locked,
            "unlocked": unlocked
        }

    @staticmethod
    def export_notes(username: str, filename: str) -> bool:
        """Export catatan ke file"""
        notes = NotesManager.get_notes(username)

        if not notes:
            print("❌ Tidak ada catatan untuk diekspor!")
            return False

        export_data = []
        for note in notes:
            if not note["is_locked"]:
                export_data.append({
                    "content": decode_text(note["content"]),
                    "created_at": note["created_at"],
                    "updated_at": note["updated_at"]
                })

        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(export_data, f, indent=4, ensure_ascii=False)
            print(f"✔ {len(export_data)} catatan berhasil diekspor ke {filename}")
            return True
        except IOError:
            print("❌ Gagal mengekspor catatan!")
            return False


# ==================== MENU FUNCTIONS ====================

def main_menu():
    """Menu utama aplikasi"""
    while True:
        print_header("ASISTEN SHADOW v" + VERSION)
        print_menu([
            "Register",
            "Login",
            "Tentang Aplikasi",
            "Keluar"
        ])

        choice = get_input("Pilih menu (1-4): ")

        if choice == "1":
            register_menu()
        elif choice == "2":
            login_menu()
        elif choice == "3":
            about_menu()
        elif choice == "4":
            print("\n✔ Terima kasih telah menggunakan Asisten Shadow!")
            break
        else:
            print("❌ Pilihan tidak valid!")


def register_menu():
    """Menu registrasi"""
    print_header("REGISTRASI PENGGUNA")
    username = get_input("Username (min 3 karakter): ")
    password = get_input("Password (min 6 karakter): ")
    confirm = get_input("Konfirmasi Password: ")

    if password != confirm:
        print("❌ Password tidak cocok!")
        return

    UserManager.register(username, password)


def login_menu():
    """Menu login"""
    print_header("LOGIN PENGGUNA")
    username = get_input("Username: ")
    password = get_input("Password: ")

    if UserManager.login(username, password):
        print(f"\n✔ Selamat datang, {username}!")
        input("\nTekan Enter untuk melanjutkan...")
        user_dashboard(username)


def user_dashboard(username: str):
    """Dashboard pengguna setelah login"""
    while True:
        print_header(f"DASHBOARD - {username.upper()}")

        # Tampilkan statistik
        stats = NotesManager.get_statistics(username)
        print(f"📊 Total Catatan: {stats['total']} | 🔒 Terkunci: {stats['locked']} | 🔓 Terbuka: {stats['unlocked']}")

        print_menu([
            "Tambah Catatan",
            "Lihat Semua Catatan",
            "Buka Catatan",
            "Edit Catatan",
            "Hapus Catatan",
            "Cari Catatan",
            "Export Catatan",
            "Info Akun",
            "Logout"
        ])

        choice = get_input("Pilih menu (1-9): ")

        if choice == "1":
            add_note_menu(username)
        elif choice == "2":
            NotesManager.display_notes_list(username)
            input("\nTekan Enter untuk kembali...")
        elif choice == "3":
            view_note_menu(username)
        elif choice == "4":
            edit_note_menu(username)
        elif choice == "5":
            delete_note_menu(username)
        elif choice == "6":
            search_note_menu(username)
        elif choice == "7":
            export_note_menu(username)
        elif choice == "8":
            account_info_menu(username)
        elif choice == "9":
            print("\n✔ Logout berhasil!")
            break
        else:
            print("❌ Pilihan tidak valid!")


def add_note_menu(username: str):
    """Menu tambah catatan"""
    print_header("TAMBAH CATATAN BARU")
    print("💡 Tips: Tekan Ctrl+D (Linux/Mac) atau Ctrl+Z (Windows) untuk selesai\n")

    content = get_input("Tulis catatan: ")
    lock = get_input("Kunci catatan (kosongkan jika tidak): ", required=False)

    NotesManager.add_note(username, content, lock)


def view_note_menu(username: str):
    """Menu lihat catatan"""
    notes = NotesManager.display_notes_list(username)
    if not notes:
        return

    index = get_input("\nPilih nomor catatan (0 untuk kembali): ")
    if index.isdigit() and int(index) > 0:
        NotesManager.view_note(username, int(index) - 1)
        input("\nTekan Enter untuk kembali...")


def edit_note_menu(username: str):
    """Menu edit catatan"""
    notes = NotesManager.display_notes_list(username)
    if not notes:
        return

    index = get_input("\nPilih nomor catatan (0 untuk kembali): ")
    if not index.isdigit() or int(index) == 0:
        return

    idx = int(index) - 1
    print_header("EDIT CATATAN")

    new_content = get_input("Isi baru catatan: ")
    print("\n💡 Kunci baru:")
    print("  - Kosongkan = tidak mengubah kunci")
    print("  - Ketik 'hapus' = menghapus kunci")
    print("  - Ketik kunci baru = mengubah kunci")

    new_lock_input = get_input("Kunci baru: ", required=False)

    if new_lock_input.lower() == "hapus":
        new_lock = ""
    elif new_lock_input == "":
        new_lock = None
    else:
        new_lock = new_lock_input

    NotesManager.edit_note(username, idx, new_content, new_lock)


def delete_note_menu(username: str):
    """Menu hapus catatan"""
    notes = NotesManager.display_notes_list(username)
    if not notes:
        return

    index = get_input("\nPilih nomor catatan (0 untuk kembali): ")
    if index.isdigit() and int(index) > 0:
        NotesManager.delete_note(username, int(index) - 1)


def search_note_menu(username: str):
    """Menu pencarian catatan"""
    print_header("CARI CATATAN")
    keyword = get_input("Masukkan kata kunci: ")

    results = NotesManager.search_notes(username, keyword)

    if not results:
        print("\n⚠ Tidak ada catatan yang cocok.")
        return

    print(f"\n📝 Ditemukan {len(results)} catatan:")
    print("-"*70)

    for idx, note in results:
        content = decode_text(note["content"])
        preview = content[:50] + "..." if len(content) > 50 else content
        print(f"{idx + 1}. {preview}")
        print(f"   Diubah: {note['updated_at']}")
        print()

    input("Tekan Enter untuk kembali...")


def export_note_menu(username: str):
    """Menu export catatan"""
    print_header("EXPORT CATATAN")
    filename = get_input("Nama file (contoh: backup.json): ")

    if not filename.endswith(".json"):
        filename += ".json"

    NotesManager.export_notes(username, filename)
    input("\nTekan Enter untuk kembali...")


def account_info_menu(username: str):
    """Menu informasi akun"""
    print_header("INFORMASI AKUN")

    user_info = UserManager.get_user_info(username)
    stats = NotesManager.get_statistics(username)

    if user_info:
        print(f"👤 Username: {username}")
        print(f"📅 Terdaftar: {user_info.get('created_at', 'N/A')}")
        print(f"🕐 Login Terakhir: {user_info.get('last_login', 'N/A')}")
        print(f"\n📊 Statistik Catatan:")
        print(f"   Total: {stats['total']}")
        print(f"   Terkunci: {stats['locked']}")
        print(f"   Terbuka: {stats['unlocked']}")

    input("\nTekan Enter untuk kembali...")


def about_menu():
    """Menu tentang aplikasi"""
    print_header("TENTANG ASISTEN SHADOW")
    print("""
Asisten Shadow adalah aplikasi catatan pribadi dengan enkripsi
yang membantu Anda menyimpan catatan dengan aman.

Fitur:
✔ Enkripsi catatan dengan Base64
✔ Password hashing dengan SHA-256
✔ Kunci pribadi untuk catatan sensitif
✔ Pencarian catatan
✔ Statistik dan analytics
✔ Export catatan

Version: 2.0
Developer: Asisten Shadow Team
    """)
    input("\nTekan Enter untuk kembali...")


# ==================== MAIN ENTRY POINT ====================

def main():
    """Fungsi utama aplikasi"""
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n✔ Program dihentikan oleh pengguna.")
    except Exception as e:
        print(f"\n❌ Terjadi kesalahan: {str(e)}")


if __name__ == "__main__":
    main()
