import sys
import xmlrpc.client
import time
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QLineEdit, QPushButton, QGridLayout
from PyQt5.QtCore import QThread, Qt, pyqtSignal

client = xmlrpc.client.ServerProxy('http://localhost:9999')

class updateThread(QThread):
    signal = pyqtSignal(str)
    def __init__(self):
        super().__init__()

    def run(self):
        self.baseId = 0
        while True:
            buf = client.getId()
            if buf != self.baseId:
                buf = client.getMessages(self.baseId)
                for i in buf:
                    self.signal.emit(i)
                    self.baseId += 1
            time.sleep(1)

class window(QWidget):
    def __init__(self):
        super().__init__()
        self.grid = QGridLayout()
        self.text = QTextEdit()
        self.btn = QPushButton()
        self.btn.setText('Send')
        self.btn.clicked.connect(self.sendMessage)
        self.message = QLineEdit()

        self.grid.addWidget(self.text,1,1,2,2)
        self.grid.addWidget(self.message,3,1,1,1)
        self.grid.addWidget(self.btn,3,2,1,1)

        self.setLayout(self.grid)

        self.updateThread = updateThread()
        self.updateThread.signal.connect(self.updateMessages, Qt.QueuedConnection)
        self.updateThread.start()

    def sendMessage(self, signal):
        client.sendMessage(self.message.text())

    def updateMessages(self, signal):
        self.text.append(signal)

class application(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        self.window = window()
        self.window.show()
        self.exit(self.exec_())

if __name__ == '__main__':
    app = application()
