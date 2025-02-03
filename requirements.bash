#!/bin/bash
# install.sh: Install Python dependencies and check for external tools.

# --- Step 1: Check for Python 3 ---
if ! command -v python3 &>/dev/null; then
    echo "Error: python3 not found. Please install Python 3.6+."
    exit 1
fi

echo "Python3 found: $(python3 --version)"

# --- Step 2: Create & Activate a Virtual Environment ---
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

# --- Step 3: Upgrade pip ---
echo "Upgrading pip..."
pip install --upgrade pip

# --- Step 4: Install Python Dependencies ---
echo "Installing Python dependencies from requirements.txt..."
pip install -r requirements.txt

echo "Python dependencies installed."

# --- Step 5: Check for External Tools ---
echo "Checking for external tools required for additional file conversions..."

declare -A deps
deps=(
    ["LibreOffice"]="libreoffice"
    ["wkhtmltopdf"]="wkhtmltopdf"
    ["pdflatex"]="pdflatex"
    ["ebook-convert (Calibre)"]="ebook-convert"
)

for dep in "${!deps[@]}"; do
    if ! command -v "${deps[$dep]}" &>/dev/null; then
        echo "Warning: $dep is not installed or not in PATH. Some conversions may not work."
    else
        echo "$dep is installed."
    fi
done

echo "Installation complete."
echo "Activate the virtual environment using: source venv/bin/activate"
