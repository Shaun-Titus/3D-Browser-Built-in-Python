import sys
import os
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLineEdit,
    QToolBar,
    QAction,
    QVBoxLayout,
    QWidget,
)
from PyQt5.QtWebEngineWidgets import QWebEngineView

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HOME_PAGE = os.path.join(BASE_DIR, "assets", "home.html")

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shaun’s 3D Browser")
        self.setGeometry(100, 100, 1200, 800)

        self.browser = QWebEngineView()
        self.browser.load(QUrl.fromLocalFile(HOME_PAGE))

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        self.browser.urlChanged.connect(self.update_url_bar)

        # Toolbar
        nav_bar = QToolBar()
        self.addToolBar(nav_bar)

        back_btn = QAction("⏪", self)
        back_btn.triggered.connect(self.browser.back)
        nav_bar.addAction(back_btn)

        forward_btn = QAction("⏩", self)
        forward_btn.triggered.connect(self.browser.forward)
        nav_bar.addAction(forward_btn)

        reload_btn = QAction("🔄", self)
        reload_btn.triggered.connect(self.browser.reload)
        nav_bar.addAction(reload_btn)

        home_btn = QAction("🏠", self)
        home_btn.triggered.connect(self.navigate_home)
        nav_bar.addAction(home_btn)

        nav_bar.addWidget(self.url_bar)

        # Layout
        container = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        container.setLayout(layout)
        self.setCentralWidget(container)

    def navigate_home(self):
        self.browser.load(QUrl.fromLocalFile(HOME_PAGE))

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "https://www.google.com/search?q=" + url
        self.browser.load(QUrl(url))

    def update_url_bar(self, q):
        self.url_bar.setText(q.toString())

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load and apply stylesheet
    qss_file = os.path.join(BASE_DIR, "assets", "styles.qss")
    if not os.path.isfile(qss_file):
        raise FileNotFoundError(f"Couldn’t find stylesheet at {qss_file}")
    with open(qss_file, "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())

    window = Browser()
    window.show()
    sys.exit(app.exec_())
