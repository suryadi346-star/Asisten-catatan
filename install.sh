#!/bin/bash
# ============================================
#  Asisten Shadow - Script Instalasi
#  Kompatibel: Termux, Linux, macOS
# ============================================

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
RESET='\033[0m'
BOLD='\033[1m'

echo ""
echo -e "${CYAN}${BOLD}  ╔══════════════════════════════════════╗${RESET}"
echo -e "${CYAN}${BOLD}  ║     ASISTEN SHADOW - INSTALLER       ║${RESET}"
echo -e "${CYAN}${BOLD}  ╚══════════════════════════════════════╝${RESET}"
echo ""

# Deteksi platform
if [ -d "/data/data/com.termux" ]; then
    PLATFORM="termux"
    echo -e "${YELLOW}  Platform terdeteksi: Termux${RESET}"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    PLATFORM="linux"
    echo -e "${YELLOW}  Platform terdeteksi: Linux${RESET}"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    PLATFORM="macos"
    echo -e "${YELLOW}  Platform terdeteksi: macOS${RESET}"
else
    PLATFORM="unknown"
    echo -e "${YELLOW}  Platform: Unknown${RESET}"
fi

echo ""
echo -e "${CYAN}  [1/3] Memeriksa Python...${RESET}"

# Cek Python
if command -v python3 &>/dev/null; then
    PYTHON="python3"
    PY_VER=$(python3 --version 2>&1)
    echo -e "${GREEN}  ✔ Python ditemukan: ${PY_VER}${RESET}"
elif command -v python &>/dev/null; then
    PYTHON="python"
    PY_VER=$(python --version 2>&1)
    echo -e "${GREEN}  ✔ Python ditemukan: ${PY_VER}${RESET}"
else
    echo -e "${RED}  ✗ Python tidak ditemukan!${RESET}"
    echo ""
    if [ "$PLATFORM" = "termux" ]; then
        echo -e "${YELLOW}  Jalankan: pkg install python${RESET}"
    elif [ "$PLATFORM" = "linux" ]; then
        echo -e "${YELLOW}  Jalankan: sudo apt install python3${RESET}"
    fi
    exit 1
fi

echo ""
echo -e "${CYAN}  [2/3] Menyiapkan direktori...${RESET}"

# Buat folder data jika belum ada
mkdir -p data
echo -e "${GREEN}  ✔ Direktori data siap${RESET}"

echo ""
echo -e "${CYAN}  [3/3] Membuat shortcut jalankan...${RESET}"

# Buat script jalankan
cat > run.sh << EOF
#!/bin/bash
cd "\$(dirname "\$0")"
${PYTHON} main.py
EOF

chmod +x run.sh
echo -e "${GREEN}  ✔ Script run.sh dibuat${RESET}"

echo ""
echo -e "${GREEN}${BOLD}  ╔══════════════════════════════════════╗${RESET}"
echo -e "${GREEN}${BOLD}  ║    Instalasi selesai! 🎉              ║${RESET}"
echo -e "${GREEN}${BOLD}  ╚══════════════════════════════════════╝${RESET}"
echo ""
echo -e "${CYAN}  Cara menjalankan:${RESET}"
echo -e "${YELLOW}    ${PYTHON} main.py${RESET}"
echo -e "${YELLOW}    atau: bash run.sh${RESET}"
echo ""
