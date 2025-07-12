import os
import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QAction,
    QLineEdit, QStatusBar
)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage

# 1) Subclass to suppress JS console spam
class SilentWebEnginePage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, msg, line, src):
        # Ignore all JavaScript console messages
        pass

# 2) Define project base directory and custom homepage path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HOMEPAGE = QUrl.fromLocalFile(os.path.join(BASE_DIR, "assets", "home.html"))

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shaun's 3D Browser")
        self.setGeometry(100, 100, 1200, 800)

        # — Central web view with silent console
        self.browser = QWebEngineView()
        self.browser.setPage(SilentWebEnginePage(self.browser))
        self.browser.setUrl(HOMEPAGE)  # Load your custom homepage
        self.setCentralWidget(self.browser)

        # — Status bar for load progress and messages
        self.status = QStatusBar()
        self.setStatusBar(self.status)

        # — Navigation toolbar
        navtb = QToolBar("Navigation")
        self.addToolBar(navtb)

        # Back button
        back_btn = QAction("⏪ Back", self)
        back_btn.setStatusTip("Go back")
        back_btn.triggered.connect(self.browser.back)
        navtb.addAction(back_btn)

        # Forward button
        forward_btn = QAction("⏩ Forward", self)
        forward_btn.setStatusTip("Go forward")
        forward_btn.triggered.connect(self.browser.forward)
        navtb.addAction(forward_btn)

        # Reload button
        reload_btn = QAction("🔄 Reload", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(self.browser.reload)
        navtb.addAction(reload_btn)

        # Home button
        home_btn = QAction("🏠 Home", self)
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        # — URL bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.load_url_from_bar)
        navtb.addWidget(self.url_bar)

        # — Connect signals
        self.browser.urlChanged.connect(self.update_url_bar)
        self.browser.loadFinished.connect(self.update_title)
        self.browser.loadProgress.connect(self.update_progress)

    def navigate_home(self):
        """Go to the local custom homepage."""
        self.browser.setUrl(HOMEPAGE)

    def load_url_from_bar(self):
        """Decide if input is a URL or search query and navigate."""
        text = self.url_bar.text().strip()
        if "." in text and not text.startswith(("http://", "https://")):
            # Looks like a domain → load directly
            url = QUrl("https://" + text)
        else:
            # Treat as search if no dot or full URL not given
            if not text.startswith(("http://", "https://")):
                text = "https://www.google.com/search?q=" + text
            url = QUrl(text)
        self.browser.setUrl(url)

    def update_url_bar(self, qurl):
        """Update the URL bar to reflect the current page."""
        self.url_bar.setText(qurl.toString())
        self.url_bar.setCursorPosition(0)

    def update_title(self):
        """Set window title to the current page's title."""
        title = self.browser.page().title()
        self.setWindowTitle(f"{title} — Shaun's 3D Browser")

    def update_progress(self, pct):
        """Show loading progress in the status bar."""
        self.status.showMessage(f"Loading… {pct}%")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load and apply QSS stylesheet
    qss_path = os.path.join(BASE_DIR, "assets", "styles.qss")
    if not os.path.isfile(qss_path):
        raise FileNotFoundError(f"Couldn’t find stylesheet at {qss_path}")
    with open(qss_path, "r") as f:
        app.setStyleSheet(f.read())

    # Create and show browser window
    window = Browser()
    window.show()
    sys.exit(app.exec_())
