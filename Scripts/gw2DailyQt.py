import sys, urllib.request, json
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QGridLayout, QPushButton, QTabWidget, QFrame
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class loadThread(QThread):
    metaEventSignal = pyqtSignal(str)
    eventSignal = pyqtSignal(dict)
    def __init__(self, url, event = None):
        super().__init__()
        self.url = url
        self.event = event

    def run(self):
        if self.event == None:
            self.metaEventSignal.emit(urllib.request.urlopen(self.url).read().decode('UTF-8'))
        if self.event != None:
            items = json.loads(urllib.request.urlopen(self.url+str(self.event['id'])).read().decode('UTF-8'))
            for i in items[0].keys():
                self.event.setdefault(i,items[0][i])
            self.eventSignal.emit(self.event)

class frame(QFrame):
    def __init__(self):
        super().__init__()
        self.grid = QGridLayout()

        self.setLayout(self.grid)

    def addEvent(self, line):
        self.name = QLabel()
        self.name = line['name']
        self.grid.addWidget(self.name)
        self.resize(self.grid.sizeHint())

class window(QWidget):
    def __init__(self):
        super().__init__()
        self.tab = QTabWidget()

        self.grid = QGridLayout()
        self.grid.setSpacing(1)
        self.grid.addWidget(self.tab,1,1)
        self.setLayout(self.grid)

        self.threads = []

        self.metaEvent = loadThread(r'https://api.guildwars2.com/v2/achievements/daily')
        self.metaEvent.metaEventSignal.connect(self.getEvent, Qt.QueuedConnection)
        self.metaEvent.start()

    def getEvent(self, signal):
        items = json.loads(signal)
        for metaEvent in items.keys():
            for event in items[metaEvent]:
                self.threads.append(loadThread(r'https://api.guildwars2.com/v2/achievements?ids=',event=event))
                self.threads[-1].eventSignal.connect(self.addTab, Qt.QueuedConnection)
                self.threads[-1].start()

    def addTab(self, signal):
        items = signal
        print(items)
        for metaEvent in items.keys():
            setattr(self,'form{}'.format(str(metaEvent)),frame())
            self.tab.addTab(getattr(self,'form{}'.format(str(metaEvent))),str(metaEvent))
            for event in items[metaEvent]:
                getattr(self,'form{}'.format(str(metaEvent))).addEvent(event)

        self.resize(self.grid.sizeHint())

class application(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        self.window = window()
        self.window.show()
        self.exit(self.exec_())

if __name__ == '__main__':
    app = application()
