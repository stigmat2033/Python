import sys, json, urllib.request
from PyQt5.QtWidgets import (
    QApplication, QWidget, QScrollArea, QVBoxLayout,QFrame, QGridLayout
)
from PyQt5.QtCore import QThread, pyqtSignal, Qt

class loadThread(QThread):
    signal = pyqtSignal(bytes)
    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        print('thread working')
        self.signal.emit(urllib.request.urlopen(self.url).read())

class mainFrame(QFrame):
    def __init__(self, args):
        super().__init__()
        self.grid = QGridLayout()


class window(QWidget):
    def __init__(self):
        super().__init__()
        self.vbox = QVBoxLayout()
        self.scrollArea = QScrollArea()
        print('starting thread')
        self.thread = loadThread(r'https://api.guildwars2.com/v2/achievements/daily')
        self.thread.signal.connect(self.initMainFrame, Qt.QueuedConnection)
        self.thread.start()
        self.setLayout(self.vbox)
        print('thread started')

    def initMainFrame(self, signal):
        print('setting main frame')
        self.mainFrame = mainFrame(json.loads(signal.decode('UTF-8')))
        self.scrollArea.setWidget(self.mainFrame)
        self.vbox.addWidget(self.scrollArea)
        self.setLayout(self.vbox)
        print('done setting main frame')

class application(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        self.window = window()
        self.window.resize(300,300)
        self.window.show()
        self.exit(self.exec_())

if __name__ == '__main__':
    app = application()
