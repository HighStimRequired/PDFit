# PDFit

**Convert (*almost*) ANYTHING into a PDF!**

PDFit is a Python-based application with a sleek dark-themed GUI designed to convert a wide range of file types to PDF with minimal user effort.

---

## 🚀 Features

- **User-Friendly Interface:** Dark mode with light blue accents for optimal usability.
- **Multi-Format Conversion:** Supports converting:
  - **Images:** JPG, JPEG, PNG, BMP, GIF
  - **Text Files:** TXT, PY, CSV, LOG
  - **HTML Files:** HTML, HTM
  - **Office Documents:** DOCX, DOC, ODT, XLS, XLSX, PPT, PPTX
  - **Others:** Additional formats via LibreOffice's headless mode

---

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.6+**
- **Required Python Packages:** Install using pip:
  ```bash
  pip install PyQt5 Pillow reportlab pdfkit
  ```
- **Additional Dependencies:**
  - `pdfkit` requires [wkhtmltopdf](https://wkhtmltopdf.org/) to be installed.
  - **LibreOffice:** Ensure it’s installed and added to your system PATH.

---

## 🔧 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pdfit.git
   ```
2. Navigate to the project directory:
   ```bash
   cd pdfit
   ```
3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🛠 Usage

1. Run the application:
   ```bash
   python pdfit.py
   ```
2. Use the GUI to browse and select a file.
3. Click **Convert to PDF**. The output PDF will be saved in the same directory as the original file.

---

## 🤝 Contributing

Contributions are welcome! Please fork the repository and create a pull request with your improvements.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

