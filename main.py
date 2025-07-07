import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLineEdit,
    QTabWidget, QToolBar, QLabel
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon


os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = '--disable-logging --disable-infobars --no-sandbox --disable-gpu'
os.environ['QTWEBENGINE_DISABLE_SANDBOX'] = '1'
os.environ['QTWEBENGINE_DISABLE_GPU'] = '1'
os.environ['QTWEBENGINE_DISABLE_GPU_THREAD'] = '1'
os.environ['QTWEBENGINE_REMOTE_DEBUGGING'] = ''
os.environ['QT_LOGGING_RULES'] = '*.debug=false;qt.qpa.*=false'

class FalconWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🦅 Falcon Browser")
        self.setGeometry(100, 100, 1400, 900)

      
        self.setWindowIcon(QIcon("assets/icon.jpg"))


        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        homepage_path = os.path.join(base_path, "newtab.html")
        self.homepage_path = QUrl.fromLocalFile(homepage_path)

   
        self.setStyleSheet("""
            QMainWindow { background-color: #0d0d0d; }
            QToolBar { background-color: #111; spacing: 10px; padding: 6px; border-bottom: 1px solid #222; }
            QPushButton {
                background-color: #1c1c1c;
                color: #00ffff;
                border: 1px solid #333;
                padding: 6px 10px;
                margin: 0 4px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #262626;
                border: 1px solid #00ffff;
                color: white;
            }
            QLineEdit {
                background-color: #1e1e1e;
                color: white;
                border: 1px solid #444;
                padding: 8px;
                border-radius: 6px;
                min-width: 400px;
            }
            QTabWidget::pane { border-top: 2px solid #222; }
            QTabBar::tab {
                background: #1b1b1b;
                color: #ccc;
                padding: 10px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #222;
                color: #00ffff;
                font-weight: bold;
            }
            QStatusBar { background-color: #111; color: #aaa; }
        """)

        
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

     
        self.toolbar = QToolBar("Navigation")
        self.addToolBar(self.toolbar)
        self._create_toolbar_buttons()

       
        self.status_label = QLabel("🦅 Falcon Cyber Mode Active")
        self.status_label.setStyleSheet("color: #00ffff; padding-left: 12px;")
        self.statusBar().addWidget(self.status_label)

    
        self.add_new_tab(self.homepage_path)

    def _create_toolbar_buttons(self):
        self.back_btn = QPushButton("⮜")
        self.back_btn.clicked.connect(self.go_back)
        self.toolbar.addWidget(self.back_btn)

        self.forward_btn = QPushButton("⮞")
        self.forward_btn.clicked.connect(self.go_forward)
        self.toolbar.addWidget(self.forward_btn)

        self.reload_btn = QPushButton("⟳")
        self.reload_btn.clicked.connect(self.reload_page)
        self.toolbar.addWidget(self.reload_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.toolbar.addWidget(self.url_bar)

        self.new_tab_btn = QPushButton("＋")
        self.new_tab_btn.clicked.connect(lambda: self.add_new_tab())
        self.toolbar.addWidget(self.new_tab_btn)

    def add_new_tab(self, qurl=None):
        if isinstance(qurl, bool) or qurl is None:
            qurl = self.homepage_path

        browser = QWebEngineView()
        browser.setUrl(qurl)
        index = self.tabs.addTab(browser, "New Tab")
        self.tabs.setCurrentIndex(index)

        browser.urlChanged.connect(lambda url: self.update_url_bar(url, browser))
        browser.loadFinished.connect(lambda _, br=browser: self.update_tab_title(br))

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def navigate_to_url(self):
        url = self.url_bar.text().strip()
        if not url.startswith("http"):
            url = "http://" + url
        current_browser = self.tabs.currentWidget()
        if current_browser:
            current_browser.setUrl(QUrl(url))

    def update_url_bar(self, qurl, browser):
        if self.tabs.currentWidget() == browser:
            self.url_bar.setText(qurl.toString())

    def update_tab_title(self, browser):
        index = self.tabs.indexOf(browser)
        title = browser.page().title()
        if not title or title.isspace():
            title = "New Tab"
        self.tabs.setTabText(index, title)

    def go_back(self):
        current_browser = self.tabs.currentWidget()
        if current_browser:
            current_browser.back()

    def go_forward(self):
        current_browser = self.tabs.currentWidget()
        if current_browser:
            current_browser.forward()

    def reload_page(self):
        current_browser = self.tabs.currentWidget()
        if current_browser:
            current_browser.reload()

def launch_falcon_ui():
    app = QApplication(sys.argv)
    icon_path = os.path.abspath("assets/icon.jpg")
    app.setWindowIcon(QIcon(icon_path))
    window = FalconWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    launch_falcon_ui()
