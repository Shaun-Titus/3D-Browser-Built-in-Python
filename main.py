import sys, os, json
from PyQt5.QtCore import QUrl, QTimer, pyqtSlot, QObject
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLineEdit, QToolBar, QAction, QLabel,
    QVBoxLayout, QWidget
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
from weather import get_weather

BASE = os.path.dirname(os.path.abspath(__file__))
HOME = os.path.join(BASE, "assets", "home.html")
TABS = os.path.join(BASE, "assets", "tabs.html")
QSS = os.path.join(BASE, "assets", "styles.qss")


class TabHandler(QObject):  # FIXED: Inherit from QObject
    def __init__(self, parent):
        super().__init__()  # FIXED: Call QObject constructor
        self.parent = parent

    @pyqtSlot(int)
    def switchToTab(self, idx):
        self.parent.switch_to_tab(idx)


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shaun’s 3D HyperBrowser")
        self.setGeometry(50, 50, 1280, 840)

        self.tabs = []
        self.current_tab = None

        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        for icon, command in [("🏠", self.open_home), ("➕", self.new_tab), ("🔄", self.reload_tab)]:
            btn = QAction(icon, self)
            self.toolbar.addAction(btn)
            btn.triggered.connect(command)

        self.url = QLineEdit()
        self.url.returnPressed.connect(self.load_url)
        self.toolbar.addWidget(self.url)

        self.weatherLbl = QLabel("⏳", self)
        self.toolbar.addWidget(self.weatherLbl)

        self.weatherTimer = QTimer(self)
        self.weatherTimer.timeout.connect(self.update_weather)
        self.weatherTimer.start(600_000)
        self.update_weather()

        central = QWidget()
        self.layout = QVBoxLayout(central)
        self.setCentralWidget(central)

        self.channel = QWebChannel()
        self.handler = TabHandler(self)
        self.channel.registerObject("handler", self.handler)

        self.new_tab(HOME)

    def new_tab(self, url=None):
        view = QWebEngineView()
        view.page().setWebChannel(self.channel)
        view.setUrl(QUrl.fromLocalFile(url or HOME))

        if self.current_tab:
            self.layout.removeWidget(self.current_tab)
            self.current_tab.hide()

        self.tabs.append(view)
        self.current_tab = view
        self.layout.addWidget(view)
        self.url.setText(view.url().toString())
        self.update_tab_tray()

    def switch_to_tab(self, idx):
        if 0 <= idx < len(self.tabs):
            self.layout.removeWidget(self.current_tab)
            self.current_tab.hide()
            self.current_tab = self.tabs[idx]
            self.layout.addWidget(self.current_tab)
            self.current_tab.show()
            self.url.setText(self.current_tab.url().toString())

    def reload_tab(self):
        if self.current_tab:
            self.current_tab.reload()

    def open_home(self):
        self.load_url(HOME, load_from_home=True)

    def load_url(self, url=None, load_from_home=False):
        text = self.url.text() if not load_from_home else url
        if not text.startswith("http"):
            text = "https://www.google.com/search?q=" + text
        self.current_tab.setUrl(QUrl(text))
        self.url.setText(text)

    def update_weather(self):
        w = get_weather("Kottayam")
        self.weatherLbl.setText(f"{w['cond']} {w['temp']}°C")

    def update_tab_tray(self):
        data = [{"url": t.url().toString(), "title": t.title() or ""} for t in self.tabs]
        tray_js = f"window.tabs = {json.dumps(data)};"
        self.current_tab.page().runJavaScript(tray_js)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open(QSS, "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())
    win = Browser()
    win.show()
    sys.exit(app.exec_())
