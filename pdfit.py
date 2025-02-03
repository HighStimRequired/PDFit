import sys
import os
import subprocess
from PyQt5 import QtWidgets, QtGui, QtCore

# For image conversion to PDF
from PIL import Image
# For text conversion to PDF
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class PDFConverter(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quick PDF Converter")
        self.setGeometry(100, 100, 500, 300)
        self.setStyleSheet(self.dark_theme())
        self.initUI()

    def dark_theme(self):
        """
        Returns a stylesheet string for a dark-themed UI with light blue accents.
        """
        return """
        QWidget {
            background-color: #2c2c2c;
            color: #ffffff;
            font-family: sans-serif;
            font-size: 14px;
        }
        QPushButton {
            background-color: #3498db;
            border: none;
            padding: 10px;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #5dade2;
        }
        QLineEdit {
            background-color: #3c3c3c;
            border: 1px solid #555555;
            padding: 5px;
            border-radius: 3px;
        }
        QLabel {
            padding: 5px;
        }
        """

    def initUI(self):
        """
        Initializes the main UI components.
        """
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QVBoxLayout()

        # Instruction Label
        self.label = QtWidgets.QLabel("Select a file to convert to PDF:")
        layout.addWidget(self.label)

        # File path display (read-only)
        self.file_path_edit = QtWidgets.QLineEdit()
        self.file_path_edit.setReadOnly(True)
        layout.addWidget(self.file_path_edit)

        # Browse Button
        self.browse_button = QtWidgets.QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_file)
        layout.addWidget(self.browse_button)

        # Convert Button
        self.convert_button = QtWidgets.QPushButton("Convert to PDF")
        self.convert_button.clicked.connect(self.convert_file)
        layout.addWidget(self.convert_button)

        # Status Label for feedback
        self.status_label = QtWidgets.QLabel("")
        layout.addWidget(self.status_label)

        central_widget.setLayout(layout)

    def browse_file(self):
        """
        Opens a file dialog for the user to select a file.
        """
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select File", "", "All Files (*.*)"
        )
        if file_path:
            self.file_path_edit.setText(file_path)
            self.status_label.setText("File selected.")

    def convert_file(self):
        """
        Handles the conversion process when the user clicks the Convert button.
        """
        file_path = self.file_path_edit.text()
        if not file_path:
            self.status_label.setText("Please select a file first!")
            return

        self.status_label.setText("Converting...")
        QtWidgets.QApplication.processEvents()  # Refresh UI

        try:
            output_pdf = self.convert_to_pdf(file_path)
            self.status_label.setText(f"Conversion successful! PDF saved to:\n{output_pdf}")
        except Exception as e:
            self.status_label.setText(f"Conversion failed: {str(e)}")

    def convert_to_pdf(self, file_path):
        """
        Determines the file type and routes the conversion accordingly.
        """
        ext = os.path.splitext(file_path)[1].lower()
        output_dir = os.path.dirname(file_path)
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_pdf = os.path.join(output_dir, base_name + ".pdf")

        if ext in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']:
            self.image_to_pdf(file_path, output_pdf)
        elif ext in ['.txt', '.py', '.csv', '.log']:
            self.text_to_pdf(file_path, output_pdf)
        elif ext in ['.html', '.htm']:
            self.html_to_pdf(file_path, output_pdf)
        elif ext in ['.docx', '.doc', '.odt', '.xls', '.xlsx', '.ppt', '.pptx']:
            # Use LibreOffice for office documents
            self.libreoffice_convert(file_path, output_dir)
            output_pdf = os.path.join(output_dir, base_name + ".pdf")
        else:
            # Attempt a conversion via LibreOffice for other types
            self.libreoffice_convert(file_path, output_dir)
            output_pdf = os.path.join(output_dir, base_name + ".pdf")

        return output_pdf

    def image_to_pdf(self, image_path, output_pdf):
        """
        Converts an image file to a PDF using Pillow.
        """
        img = Image.open(image_path)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        img.save(output_pdf, "PDF", resolution=100.0)

    def text_to_pdf(self, text_path, output_pdf):
        """
        Converts a text file to a PDF using ReportLab.
        """
        c = canvas.Canvas(output_pdf, pagesize=letter)
        width, height = letter
        with open(text_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
        margin = 40
        y = height - margin
        line_height = 14
        for line in lines:
            if y < margin:
                c.showPage()
                y = height - margin
            c.drawString(margin, y, line.strip())
            y -= line_height
        c.save()

    def html_to_pdf(self, html_path, output_pdf):
        """
        Converts an HTML file to a PDF using pdfkit.
        Note: Ensure that pdfkit and wkhtmltopdf are installed and configured.
        """
        try:
            import pdfkit
        except ImportError:
            raise Exception("pdfkit is required for HTML conversion. Install it with 'pip install pdfkit'.")
        pdfkit.from_file(html_path, output_pdf)

    def libreoffice_convert(self, file_path, output_dir):
        """
        Converts a file to PDF using LibreOffice's headless conversion.
        Make sure LibreOffice is installed and added to your system PATH.
        """
        command = [
            'libreoffice', '--headless', '--convert-to', 'pdf', '--outdir',
            output_dir, file_path
        ]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            raise Exception("LibreOffice conversion failed. Ensure LibreOffice is installed and in your PATH.")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = PDFConverter()
    window.show()
    sys.exit(app.exec_())
