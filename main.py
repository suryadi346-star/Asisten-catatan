
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
import sys
import json
import base64
import hashlib
import datetime
import tty
import termios
from typing import Dict, List, Optional, Tuple

# ==================== KONSTANTA ====================
USER_FILE = "users.json"
NOTES_FILE = "notes.json"
VERSION = "2.0"

# ==================== WARNA TERMINAL ====================

class Color:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"

    BLACK   = "\033[30m"
    RED     = "\033[31m"
    GREEN   = "\033[32m"
    YELLOW  = "\033[33m"
    BLUE    = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN    = "\033[36m"
    WHITE   = "\033[37m"

    BG_BLACK   = "\033[40m"
    BG_RED     = "\033[41m"
    BG_GREEN   = "\033[42m"
    BG_YELLOW  = "\033[43m"
    BG_BLUE    = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN    = "\033[46m"
    BG_WHITE   = "\033[47m"

def c(text, *styles):
    """Wrap text dengan kode warna ANSI"""
    return "".join(styles) + str(text) + Color.RESET


# ==================== HELPER FUNCTIONS ====================

def load_data(filename: str) -> Dict:
    if not os.path.exists(filename):
        return {}
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, IOError):
        return {}


def save_data(filename: str, data: Dict) -> bool:
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except IOError:
        print(c("  ✗ Gagal menyimpan data!", Color.RED))
        return False


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def encode_text(text: str) -> str:
    return base64.b64encode(text.encode()).decode()


def decode_text(text_b64: str) -> str:
    try:
        return base64.b64decode(text_b64.encode()).decode()
    except Exception:
        return "[ERROR: Data rusak]"


def get_timestamp() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_banner():
    """Mencetak banner ASCII art aplikasi"""
    clear_screen()
    print(c("""
  ╔═══════════════════════════════════════════╗
  ║                                           ║
  ║    ███████╗██╗  ██╗ █████╗ ██████╗        ║
  ║    ██╔════╝██║  ██║██╔══██╗██╔══██╗       ║
  ║    ███████╗███████║███████║██║  ██║       ║
  ║    ╚════██║██╔══██║██╔══██║██║  ██║       ║
  ║    ███████║██║  ██║██║  ██║██████╔╝       ║
  ║    ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝        ║
  ║                                           ║
  ║       A S I S T E N   S H A D O W         ║
  ║         Catatan Terenkripsi v2.0          ║
  ╚═══════════════════════════════════════════╝""", Color.CYAN, Color.BOLD))
    print()


def print_header(title: str):
    w = 46
    print()
    print(c("  ┌" + "─" * w + "┐", Color.CYAN))
    print(c("  │" + title.center(w) + "│", Color.CYAN))
    print(c("  └" + "─" * w + "┘", Color.CYAN))


def print_divider(char="─", width=48):
    print(c("  " + char * width, Color.DIM))


def print_menu(options: List[str], color=Color.YELLOW):
    print_divider()
    for i, option in enumerate(options, 1):
        num = c(f"  [{i}]", Color.CYAN, Color.BOLD)
        print(f"{num} {c(option, color)}")
    print_divider()


def success(msg): print(c(f"\n  ✔ {msg}", Color.GREEN, Color.BOLD))
def error(msg):   print(c(f"\n  ✗ {msg}", Color.RED))
def warn(msg):    print(c(f"\n  ⚠ {msg}", Color.YELLOW))
def info(msg):    print(c(f"\n  ℹ {msg}", Color.CYAN))


def _input_password(prompt: str) -> str:
    """Input password dengan tampilan * per karakter. Fallback ke getpass jika tidak di terminal."""
    sys.stdout.write(prompt)
    sys.stdout.flush()

    # Fallback jika bukan terminal interaktif (misal pipe/redirect)
    if not sys.stdin.isatty():
        import getpass
        return getpass.getpass("")

    password_chars = []
    try:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setraw(fd)
        try:
            while True:
                ch = sys.stdin.read(1)
                # Enter
                if ch in ('\r', '\n'):
                    sys.stdout.write('\n')
                    sys.stdout.flush()
                    break
                # Backspace / Delete
                elif ch in ('\x7f', '\x08'):
                    if password_chars:
                        password_chars.pop()
                        # Hapus satu * di layar
                        sys.stdout.write('\b \b')
                        sys.stdout.flush()
                # Ctrl+C
                elif ch == '\x03':
                    sys.stdout.write('\n')
                    raise KeyboardInterrupt
                # Ctrl+D / EOF
                elif ch == '\x04':
                    sys.stdout.write('\n')
                    break
                # Karakter normal
                elif ch >= ' ':
                    password_chars.append(ch)
                    sys.stdout.write('*')
                    sys.stdout.flush()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    except (termios.error, AttributeError):
        # Fallback untuk Windows atau terminal yang tidak support tty
        import getpass
        return getpass.getpass("")

    return ''.join(password_chars)


def get_input(prompt: str, required: bool = True, password: bool = False) -> str:
    while True:
        try:
            if password:
                value = _input_password(c(f"  → {prompt}", Color.WHITE)).strip()
            else:
                value = input(c(f"  → {prompt}", Color.WHITE)).strip()
        except EOFError:
            value = ""
        if not required or value:
            return value
        error("Input tidak boleh kosong!")


def confirm_action(message: str) -> bool:
    resp = input(c(f"\n  ⚠ {message} ", Color.YELLOW) + c("[y/N]: ", Color.CYAN)).lower().strip()
    return resp == 'y'


def pause():
    input(c("\n  Tekan Enter untuk melanjutkan...", Color.DIM))


# ==================== USER MANAGEMENT ====================

class UserManager:

    @staticmethod
    def register(username: str, password: str) -> bool:
        if not username or not password:
            error("Username dan password tidak boleh kosong!")
            return False
        if len(username) < 3:
            error("Username minimal 3 karakter!")
            return False
        if len(password) < 6:
            error("Password minimal 6 karakter!")
            return False

        users = load_data(USER_FILE)
        if username in users:
            error("Username sudah digunakan!")
            return False

        users[username] = {
            "password": hash_password(password),
            "created_at": get_timestamp(),
            "last_login": None
        }

        if save_data(USER_FILE, users):
            success("Registrasi berhasil! Silakan login.")
            return True
        return False

    @staticmethod
    def login(username: str, password: str) -> bool:
        users = load_data(USER_FILE)
        if username not in users:
            error("Username tidak ditemukan!")
            return False
        if users[username]["password"] != hash_password(password):
            error("Password salah!")
            return False

        users[username]["last_login"] = get_timestamp()
        save_data(USER_FILE, users)
        return True

    @staticmethod
    def get_user_info(username: str) -> Optional[Dict]:
        users = load_data(USER_FILE)
        return users.get(username)


# ==================== NOTES MANAGEMENT ====================

class NotesManager:

    @staticmethod
    def add_note(username: str, content: str, lock_key: str = "") -> bool:
        if not content:
            error("Catatan tidak boleh kosong!")
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
            success("Catatan berhasil ditambahkan!")
            return True
        return False

    @staticmethod
    def get_notes(username: str) -> List[Dict]:
        notes = load_data(NOTES_FILE)
        return notes.get(username, [])

    @staticmethod
    def display_notes_list(username: str) -> List[Dict]:
        notes = NotesManager.get_notes(username)

        if not notes:
            warn("Belum ada catatan.")
            return []

        print_header("DAFTAR CATATAN")
        print()

        for i, note in enumerate(notes, 1):
            if note["is_locked"]:
                icon    = c("🔒", Color.RED)
                preview = c("[Catatan Terkunci]", Color.DIM)
            else:
                icon    = c("🔓", Color.GREEN)
                content = decode_text(note["content"])
                short   = content[:40] + ("..." if len(content) > 40 else "")
                preview = c(short, Color.WHITE)

            num  = c(f"  [{i}]", Color.CYAN, Color.BOLD)
            date = c(note["updated_at"], Color.DIM)
            print(f"{num} {icon}  {preview}")
            print(f"       {date}")
            print()

        print_divider()
        print(c(f"  Total: {len(notes)} catatan", Color.YELLOW))
        return notes

    @staticmethod
    def view_note(username: str, index: int) -> bool:
        notes = NotesManager.get_notes(username)
        if not 0 <= index < len(notes):
            error("Nomor catatan tidak valid!")
            return False

        note = notes[index]
        if note["is_locked"]:
            key = get_input("Masukkan kunci catatan: ", password=True)
            if hash_password(key) != note["lock"]:
                error("Kunci salah!")
                return False

        print_header("ISI CATATAN")
        print(c(f"\n  📅 Dibuat  : {note['created_at']}", Color.DIM))
        print(c(f"  ✏  Diubah  : {note['updated_at']}", Color.DIM))
        print_divider()
        print()
        for line in decode_text(note["content"]).split("\n"):
            print(f"  {line}")
        print()
        print_divider()
        return True

    @staticmethod
    def edit_note(username: str, index: int, new_content: str, new_lock: Optional[str] = None) -> bool:
        notes = load_data(NOTES_FILE)
        user_notes = notes.get(username, [])

        if not 0 <= index < len(user_notes):
            error("Nomor catatan tidak valid!")
            return False

        note = user_notes[index]
        if note["is_locked"]:
            key = get_input("Masukkan kunci saat ini: ", password=True)
            if hash_password(key) != note["lock"]:
                error("Kunci salah!")
                return False

        note["content"]    = encode_text(new_content)
        note["updated_at"] = get_timestamp()

        if new_lock is not None:
            if new_lock == "":
                note["lock"]      = ""
                note["is_locked"] = False
            else:
                note["lock"]      = hash_password(new_lock)
                note["is_locked"] = True

        if save_data(NOTES_FILE, notes):
            success("Catatan berhasil diedit!")
            return True
        return False

    @staticmethod
    def delete_note(username: str, index: int) -> bool:
        notes = load_data(NOTES_FILE)
        user_notes = notes.get(username, [])

        if not 0 <= index < len(user_notes):
            error("Nomor catatan tidak valid!")
            return False

        note = user_notes[index]
        if note["is_locked"]:
            key = get_input("Masukkan kunci catatan: ", password=True)
            if hash_password(key) != note["lock"]:
                error("Kunci salah!")
                return False

        if not confirm_action("Yakin ingin menghapus catatan ini?"):
            warn("Penghapusan dibatalkan.")
            return False

        del user_notes[index]
        if save_data(NOTES_FILE, notes):
            success("Catatan berhasil dihapus!")
            return True
        return False

    @staticmethod
    def search_notes(username: str, keyword: str) -> List[Tuple[int, Dict]]:
        notes   = NotesManager.get_notes(username)
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
        notes    = NotesManager.get_notes(username)
        total    = len(notes)
        locked   = sum(1 for n in notes if n["is_locked"])
        unlocked = total - locked
        return {"total": total, "locked": locked, "unlocked": unlocked}

    @staticmethod
    def export_notes(username: str, filename: str) -> bool:
        notes = NotesManager.get_notes(username)
        if not notes:
            error("Tidak ada catatan untuk diekspor!")
            return False

        export_data = []
        for note in notes:
            if not note["is_locked"]:
                export_data.append({
                    "content":    decode_text(note["content"]),
                    "created_at": note["created_at"],
                    "updated_at": note["updated_at"]
                })

        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(export_data, f, indent=4, ensure_ascii=False)
            success(f"{len(export_data)} catatan diekspor ke '{filename}'")
            return True
        except IOError:
            error("Gagal mengekspor catatan!")
            return False

    @staticmethod
    def import_notes(username: str, filename: str) -> bool:
        if not os.path.exists(filename):
            error(f"File '{filename}' tidak ditemukan!")
            return False

        try:
            with open(filename, "r", encoding="utf-8") as f:
                import_data = json.load(f)

            if not isinstance(import_data, list):
                error("Format file tidak valid!")
                return False

            notes = load_data(NOTES_FILE)
            if username not in notes:
                notes[username] = []

            count = 0
            for item in import_data:
                if "content" in item:
                    note_data = {
                        "id":         len(notes[username]) + 1,
                        "content":    encode_text(item["content"]),
                        "lock":       "",
                        "created_at": item.get("created_at", get_timestamp()),
                        "updated_at": get_timestamp(),
                        "is_locked":  False
                    }
                    notes[username].append(note_data)
                    count += 1

            if save_data(NOTES_FILE, notes):
                success(f"{count} catatan berhasil diimpor!")
                return True
        except (json.JSONDecodeError, IOError):
            error("Gagal membaca file import!")
        return False


# ==================== MENU FUNCTIONS ====================

def main_menu():
    while True:
        print_banner()
        print_menu([
            "Register Akun Baru",
            "Login",
            "Tentang Aplikasi",
            "Keluar"
        ])

        choice = get_input("Pilih menu [1-4]: ")

        if choice == "1":
            register_menu()
        elif choice == "2":
            login_menu()
        elif choice == "3":
            about_menu()
        elif choice == "4":
            clear_screen()
            print(c("\n  Terima kasih telah menggunakan Asisten Shadow!\n", Color.CYAN))
            break
        else:
            error("Pilihan tidak valid!")
            pause()


def register_menu():
    print_banner()
    print_header("REGISTRASI AKUN BARU")
    print()
    username = get_input("Username (min 3 karakter)  : ")
    password = get_input("Password (min 6 karakter)  : ", password=True)
    confirm  = get_input("Konfirmasi Password        : ", password=True)

    if password != confirm:
        error("Password tidak cocok!")
        pause()
        return

    UserManager.register(username, password)
    pause()


def login_menu():
    print_banner()
    print_header("LOGIN PENGGUNA")
    print()
    username = get_input("Username : ")
    password = get_input("Password : ", password=True)

    if UserManager.login(username, password):
        success(f"Selamat datang, {username}!")
        pause()
        user_dashboard(username)


def user_dashboard(username: str):
    while True:
        clear_screen()
        stats = NotesManager.get_statistics(username)

        print(c("""
  ╔═══════════════════════════════════════════╗
  ║           D A S H B O A R D               ║
  ╚═══════════════════════════════════════════╝""", Color.MAGENTA, Color.BOLD))

        print(c(f"\n  👤  Pengguna : {username}", Color.WHITE, Color.BOLD))
        print(c(f"  📊  Catatan  : "
                f"{c(str(stats['total']), Color.CYAN)} total  │  "
                f"{c(str(stats['locked']), Color.RED)} terkunci  │  "
                f"{c(str(stats['unlocked']), Color.GREEN)} terbuka", Color.WHITE))

        print_menu([
            "Tambah Catatan",
            "Lihat Semua Catatan",
            "Buka & Baca Catatan",
            "Edit Catatan",
            "Hapus Catatan",
            "Cari Catatan",
            "Export Catatan",
            "Import Catatan",
            "Info Akun",
            "Logout"
        ])

        choice = get_input("Pilih menu [1-10]: ")

        if   choice == "1":  add_note_menu(username)
        elif choice == "2":
            clear_screen()
            NotesManager.display_notes_list(username)
            pause()
        elif choice == "3":  view_note_menu(username)
        elif choice == "4":  edit_note_menu(username)
        elif choice == "5":  delete_note_menu(username)
        elif choice == "6":  search_note_menu(username)
        elif choice == "7":  export_note_menu(username)
        elif choice == "8":  import_note_menu(username)
        elif choice == "9":  account_info_menu(username)
        elif choice == "10":
            success("Logout berhasil!")
            pause()
            break
        else:
            error("Pilihan tidak valid!")
            pause()


def add_note_menu(username: str):
    clear_screen()
    print_header("TAMBAH CATATAN BARU")
    info("Tulis catatan kamu. Tekan Enter dua kali untuk selesai.\n")

    lines = []
    while True:
        try:
            line = input(c("  │ ", Color.CYAN))
            if line == "" and lines and lines[-1] == "":
                break
            lines.append(line)
        except (EOFError, KeyboardInterrupt):
            break

    content = "\n".join(lines).strip()
    if not content:
        error("Catatan kosong, dibatalkan.")
        pause()
        return

    print()
    lock = get_input("Kunci catatan (kosongkan jika tidak perlu): ", required=False, password=True)
    NotesManager.add_note(username, content, lock)
    pause()


def view_note_menu(username: str):
    clear_screen()
    notes = NotesManager.display_notes_list(username)
    if not notes:
        pause()
        return

    print()
    index = get_input("Pilih nomor catatan (0 untuk batal): ")
    if index.isdigit() and int(index) > 0:
        clear_screen()
        NotesManager.view_note(username, int(index) - 1)
        pause()


def edit_note_menu(username: str):
    clear_screen()
    notes = NotesManager.display_notes_list(username)
    if not notes:
        pause()
        return

    print()
    index = get_input("Pilih nomor catatan (0 untuk batal): ")
    if not index.isdigit() or int(index) == 0:
        return

    idx = int(index) - 1
    clear_screen()
    print_header("EDIT CATATAN")
    info("Tulis isi baru. Enter dua kali untuk selesai.\n")

    lines = []
    while True:
        try:
            line = input(c("  │ ", Color.CYAN))
            if line == "" and lines and lines[-1] == "":
                break
            lines.append(line)
        except (EOFError, KeyboardInterrupt):
            break

    new_content = "\n".join(lines).strip()
    if not new_content:
        error("Isi baru kosong, dibatalkan.")
        pause()
        return

    print()
    info("Pilihan kunci:\n"
         "  - Kosongkan = tidak mengubah kunci\n"
         "  - Ketik 'hapus' = menghapus kunci\n"
         "  - Ketik kunci baru = mengubah kunci")

    new_lock_input = get_input("Kunci baru: ", required=False, password=True)

    if new_lock_input.lower() == "hapus":
        new_lock = ""
    elif new_lock_input == "":
        new_lock = None
    else:
        new_lock = new_lock_input

    NotesManager.edit_note(username, idx, new_content, new_lock)
    pause()


def delete_note_menu(username: str):
    clear_screen()
    notes = NotesManager.display_notes_list(username)
    if not notes:
        pause()
        return

    print()
    index = get_input("Pilih nomor catatan yang akan dihapus (0 untuk batal): ")
    if index.isdigit() and int(index) > 0:
        NotesManager.delete_note(username, int(index) - 1)
        pause()


def search_note_menu(username: str):
    clear_screen()
    print_header("CARI CATATAN")
    print()
    keyword = get_input("Kata kunci pencarian: ")
    results = NotesManager.search_notes(username, keyword)

    if not results:
        warn(f"Tidak ada catatan yang mengandung kata '{keyword}'.")
        pause()
        return

    print()
    print(c(f"  Ditemukan {len(results)} hasil untuk '{keyword}':", Color.CYAN, Color.BOLD))
    print_divider()

    for idx, note in results:
        content = decode_text(note["content"])
        preview = content[:60] + ("..." if len(content) > 60 else "")
        print(c(f"\n  [{idx+1}] ", Color.CYAN, Color.BOLD) + c(preview, Color.WHITE))
        print(c(f"       {note['updated_at']}", Color.DIM))

    pause()


def export_note_menu(username: str):
    clear_screen()
    print_header("EXPORT CATATAN")
    print()
    filename = get_input("Nama file (contoh: backup.json): ")
    if not filename.endswith(".json"):
        filename += ".json"
    NotesManager.export_notes(username, filename)
    pause()


def import_note_menu(username: str):
    clear_screen()
    print_header("IMPORT CATATAN")
    print()
    filename = get_input("Nama file yang akan diimport: ")
    NotesManager.import_notes(username, filename)
    pause()


def account_info_menu(username: str):
    clear_screen()
    print_header("INFORMASI AKUN")

    user_info = UserManager.get_user_info(username)
    stats     = NotesManager.get_statistics(username)

    if user_info:
        print()
        print(c(f"  👤  Username      : {username}", Color.WHITE, Color.BOLD))
        print(c(f"  📅  Terdaftar     : {user_info.get('created_at', 'N/A')}", Color.WHITE))
        print(c(f"  🕐  Login Terakhir: {user_info.get('last_login', 'N/A')}", Color.WHITE))
        print_divider()
        print(c(f"\n  📊 Statistik Catatan:", Color.YELLOW, Color.BOLD))
        print(c(f"     ▸ Total    : {stats['total']}", Color.WHITE))
        print(c(f"     ▸ Terkunci : {stats['locked']}", Color.RED))
        print(c(f"     ▸ Terbuka  : {stats['unlocked']}", Color.GREEN))

    pause()


def about_menu():
    clear_screen()
    print_banner()
    print_header("TENTANG APLIKASI")
    print(c("""
  Asisten Shadow adalah aplikasi catatan pribadi
  dengan enkripsi yang membantu Anda menyimpan
  informasi sensitif dengan aman.

  Fitur Unggulan:
  ✔  Enkripsi catatan dengan Base64
  ✔  Password hashing dengan SHA-256
  ✔  Kunci pribadi per catatan
  ✔  Pencarian cepat
  ✔  Export & Import catatan
  ✔  Tampilan berwarna (Termux-friendly)
  ✔  Input multi-baris

  Version   : 2.0 Enhanced
  Platform  : Python 3.6+
  Kompatibel: Termux, Linux, macOS, Windows
    """, Color.WHITE))
    pause()


# ==================== MAIN ====================

def main():
    try:
        main_menu()
    except KeyboardInterrupt:
        clear_screen()
        print(c("\n  Program dihentikan.\n", Color.YELLOW))
    except Exception as e:
        print(c(f"\n  Terjadi kesalahan: {str(e)}", Color.RED))


if __name__ == "__main__":
    main()
