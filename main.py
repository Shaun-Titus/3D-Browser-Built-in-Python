import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QAction,
    QLineEdit, QStatusBar
)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage

import sys
from PyQt5.QtWidgets import QApplication
# ... other imports ...

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load and apply QSS stylesheet
    with open("assets/styles.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = Browser()
    window.show()
    sys.exit(app.exec_())


# 1) Subclass QWebEnginePage to override console logging
class SilentWebEnginePage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        # Simply ignore all console messages
        pass

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Shaun's 3D Browser – Phase 1 Revamped")
        self.setGeometry(100, 100, 1200, 800)

        # 2) Use our silent page rather than the default
        self.browser = QWebEngineView()
        self.browser.setPage(SilentWebEnginePage(self.browser))
        self.browser.setUrl(QUrl("https://www.google.com"))
        self.setCentralWidget(self.browser)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        navtb = QToolBar("Navigation")
        self.addToolBar(navtb)

        back_btn = QAction("⏪ Back", self)
        back_btn.setStatusTip("Go back")
        back_btn.triggered.connect(self.browser.back)
        navtb.addAction(back_btn)

        forward_btn = QAction("⏩ Forward", self)
        forward_btn.setStatusTip("Go forward")
        forward_btn.triggered.connect(self.browser.forward)
        navtb.addAction(forward_btn)

        reload_btn = QAction("🔄 Reload", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(self.browser.reload)
        navtb.addAction(reload_btn)

        home_btn = QAction("🏠 Home", self)
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.load_url_from_bar)
        navtb.addWidget(self.url_bar)

        self.browser.urlChanged.connect(self.update_url_bar)
        self.browser.loadFinished.connect(self.update_title)
        self.browser.loadProgress.connect(self.update_progress)

    def navigate_home(self):
        self.browser.setUrl(QUrl("https://www.google.com"))

    def load_url_from_bar(self):
        text = self.url_bar.text().strip()
        if "." in text and not text.startswith(("http://", "https://")):
            url = QUrl("https://" + text)
        else:
            if not text.startswith(("http://", "https://")):
                text = "https://www.google.com/search?q=" + text
            url = QUrl(text)
        self.browser.setUrl(url)

    def update_url_bar(self, qurl):
        self.url_bar.setText(qurl.toString())
        self.url_bar.setCursorPosition(0)

    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle(f"{title} — Shaun's 3D Browser")

    def update_progress(self, progress):
        self.status.showMessage(f"Loading... {progress}%")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())
