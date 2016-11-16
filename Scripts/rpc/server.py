import sys
from xmlrpc.server import SimpleXMLRPCServer
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLabel
from PyQt5.QtCore import QThread, Qt, pyqtSignal

class ServerThread(QThread):
    signal = pyqtSignal(str)
    def __init__(self):
        super().__init__()

    def run(self):
        self.messages = []
        self.baseId = 0
        server = SimpleXMLRPCServer(('10.60.46.59',9999),allow_none=True)
        server.register_function(self.sendMessage)
        server.register_function(self.getId)
        server.register_function(self.getMessages)
        server.serve_forever()

    def sendMessage(self, text):
        self.messages.append(text)
        self.baseId += 1
        self.signal.emit(text)

    def getId(self):
        return self.baseId

    def getMessages(self, lastId):
        return self.messages[lastId:]


class window(QWidget):
    def __init__(self):
        super().__init__()
        self.vbox = QVBoxLayout()
        self.text = QTextEdit()
        self.label = QLabel()

        self.vbox.addWidget(self.text)
        self.vbox.addWidget(self.label)

        self.setLayout(self.vbox)

        self.server = ServerThread()
        self.server.signal.connect(self.sendMessage, Qt.QueuedConnection)
        self.server.start()

    def sendMessage(self, text):
        self.text.append(text)

class application(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        self.window = window()
        self.window.show()
        self.exit(self.exec_())

if __name__ == '__main__':
    app = application()