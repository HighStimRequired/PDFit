import sys
import os
import subprocess
from PyQt5 import QtWidgets, QtGui, QtCore
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class PDFConverter(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quick PDF Converter")
        self.setGeometry(100, 100, 480, 130)
        self.setStyleSheet(self.dark_theme())
        self.initUI()

    def dark_theme(self):
        """
        Returns a compact dark-themed stylesheet with light blue accents.
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
            padding: 6px 10px;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #5dade2;
        }
        QLineEdit {
            background-color: #3c3c3c;
            border: 1px solid #555;
            padding: 4px;
            border-radius: 3px;
        }
        QLabel {
            padding: 2px;
        }
        """

    def initUI(self):
        """
        Initializes a compact UI using a QGridLayout.
        """
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        grid = QtWidgets.QGridLayout()
        grid.setContentsMargins(10, 10, 10, 10)  # Reduced margins
        grid.setSpacing(8)  # Reduced spacing between widgets

        # Row 0: File selection
        file_label = QtWidgets.QLabel("Select File:")
        grid.addWidget(file_label, 0, 0)
        self.file_path_edit = QtWidgets.QLineEdit()
        self.file_path_edit.setReadOnly(True)
        grid.addWidget(self.file_path_edit, 0, 1)
        self.browse_button = QtWidgets.QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_file)
        grid.addWidget(self.browse_button, 0, 2)

        # Row 1: Output directory selection
        out_label = QtWidgets.QLabel("Output Directory:")
        grid.addWidget(out_label, 1, 0)
        self.out_dir_edit = QtWidgets.QLineEdit()
        self.out_dir_edit.setReadOnly(True)
        grid.addWidget(self.out_dir_edit, 1, 1)
        self.out_browse_button = QtWidgets.QPushButton("Browse")
        self.out_browse_button.clicked.connect(self.browse_output_directory)
        grid.addWidget(self.out_browse_button, 1, 2)

        # Row 2: Convert button (centered)
        self.convert_button = QtWidgets.QPushButton("Convert to PDF")
        self.convert_button.clicked.connect(self.convert_file)
        grid.addWidget(self.convert_button, 2, 0, 1, 3, alignment=QtCore.Qt.AlignCenter)

        # Row 3: Status label
        self.status_label = QtWidgets.QLabel("")
        self.status_label.setWordWrap(True)
        grid.addWidget(self.status_label, 3, 0, 1, 3)

        central_widget.setLayout(grid)

    def browse_file(self):
        """
        Opens a file dialog for selecting the file to convert.
        """
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select File", "", "All Files (*.*)"
        )
        if file_path:
            self.file_path_edit.setText(file_path)
            self.status_label.setText("File selected.")

    def browse_output_directory(self):
        """
        Opens a directory dialog for selecting the output directory.
        """
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if directory:
            self.out_dir_edit.setText(directory)
            self.status_label.setText("Output directory selected.")

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
        Determines the file type and routes conversion accordingly.
        Uses the chosen output directory if provided, else defaults to the file's directory.
        """
        ext = os.path.splitext(file_path)[1].lower()
        output_dir = self.out_dir_edit.text() if self.out_dir_edit.text() else os.path.dirname(file_path)
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_pdf = os.path.join(output_dir, base_name + ".pdf")

        if ext in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']:
            self.image_to_pdf(file_path, output_pdf)
        elif ext in ['.txt', '.py', '.csv', '.log']:
            self.text_to_pdf(file_path, output_pdf)
        elif ext in ['.html', '.htm']:
            self.html_to_pdf(file_path, output_pdf)
        elif ext in ['.docx', '.doc', '.odt', '.xls', '.xlsx', '.ppt', '.pptx']:
            self.libreoffice_convert(file_path, output_dir)
            output_pdf = os.path.join(output_dir, base_name + ".pdf")
        else:
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
        """
        try:
            import pdfkit
        except ImportError:
            raise Exception("pdfkit is required for HTML conversion. Install it with 'pip install pdfkit'.")
        pdfkit.from_file(html_path, output_pdf)

    def libreoffice_convert(self, file_path, output_dir):
        """
        Converts a file to PDF using LibreOffice's headless mode.
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
