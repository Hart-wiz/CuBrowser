import sys
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QAction  # ✅ moved here in PyQt6
from PyQt6.QtWidgets import QApplication, QMainWindow, QToolBar, QLineEdit
from PyQt6.QtWebEngineWidgets import QWebEngineView

class Browser(QMainWindow):
    def __init__(self, start_url="https://duckduckgo.com"):
        super().__init__()
        self.setWindowTitle("Mini Browser")
        self.resize(1000, 700)

        # Web view
        self.view = QWebEngineView()
        self.setCentralWidget(self.view)
        self.view.setUrl(QUrl(start_url))

        # Toolbar
        nav = QToolBar("Navigation")
        self.addToolBar(nav)

        back = QAction("◀", self); back.triggered.connect(self.view.back)
        fwd = QAction("▶", self);  fwd.triggered.connect(self.view.forward)
        reload = QAction("⟳", self); reload.triggered.connect(self.view.reload)
        stop = QAction("✕", self);  stop.triggered.connect(self.view.stop)
        home = QAction("Home", self); home.triggered.connect(lambda: self.view.setUrl(QUrl("https://duckduckgo.com")))
        for a in (back, fwd, reload, stop, home): nav.addAction(a)

        # URL bar
        self.urlbar = QLineEdit()
        self.urlbar.setPlaceholderText("Type a URL and press Enter…")
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        nav.addWidget(self.urlbar)

        # Keep URL bar in sync
        self.view.urlChanged.connect(self.update_urlbar)

    def navigate_to_url(self):
        url = QUrl.fromUserInput(self.urlbar.text().strip())
        if url.isValid():
            self.view.setUrl(url)

    def update_urlbar(self, qurl: QUrl):
        self.urlbar.setText(qurl.toString())
        self.urlbar.setCursorPosition(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    start = sys.argv[1] if len(sys.argv) > 1 else "https://duckduckgo.com"
    win = Browser(start)
    win.show()
    sys.exit(app.exec())
