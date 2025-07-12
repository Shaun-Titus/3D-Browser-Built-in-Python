import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Shaun's 3D Browser")

        self.setGeometry(100, 100, 1200, 800)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))
        self.setCentralWidget(self.browser)

# Create an instance of the app
app = QApplication(sys.argv)

# Create an instance of our custom Browser class
window = Browser()

# Show the browser window
window.show()

# Run the app and keep it open until the user closes it
sys.exit(app.exec_())
# This code creates a simple 3D browser using PyQt5 and QWebEngineView.
# It sets up a main window with a web view that loads Google's homepage.