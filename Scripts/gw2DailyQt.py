import sys, urllib.request, json
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QGridLayout, QTabWidget, QFrame, QVBoxLayout
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class loadThread(QThread):
    metaEventSignal = pyqtSignal(str)
    eventSignal = pyqtSignal(dict,str)
    def __init__(self, url, events = None, metaEvent=None):
        super().__init__()
        self.url = url
        self.event = events
        self.metaEvent = metaEvent

    def run(self):
        if self.event == None:
            self.metaEventSignal.emit(urllib.request.urlopen(self.url).read().decode('UTF-8'))
        if self.event != None:
            items = json.loads(urllib.request.urlopen(self.url+str(self.event['id'])).read().decode('UTF-8'))
            for i in items[0].keys():
                self.event.setdefault(i,items[0][i])
            self.eventSignal.emit(self.event,self.metaEvent)

class itemWindow(QWidget):
    def __init__(self,item):
        super().__init__()
        self.vbox = QVBoxLayout()

        self.itemId = QLabel()
        self.itemId.setText(str(item['id']))
        self.itemName = QLabel()
        self.itemName.setText(item['name'])

        self.vbox.addWidget(self.itemId)
        self.vbox.addWidget(self.itemName)

        self.resize(self.vbox.sizeHint())
        self.setLayout(self.vbox)

class eventWindow(QWidget):
    def __init__(self,event):
        super().__init__()
        print(event)
        self.vbox = QVBoxLayout()

        self.eventData = QLabel()
        self.eventData.setText('Id: {} Required access: {}'.format(
            str(event['id']),event['required_access']
        ))
        self.eventName = QLabel()
        self.eventName.setText(event['name'])
        self.eventDescription = QLabel()
        self.eventDescription.setText(event['description'])
        self.eventRequirement = QLabel()
        self.eventRequirement.setText(event['requirement'])
        self.eventRewards = QLabel()
        self.eventRewards.setText('Rewards:')
        self.vbox.addWidget(self.eventData)
        self.vbox.addWidget(self.eventName)
        self.vbox.addWidget(self.eventDescription)
        self.vbox.addWidget(self.eventRequirement)
        self.vbox.addWidget(self.eventRewards)
        self.resize(self.vbox.sizeHint())
        self.setLayout(self.vbox)

        self.threads = []
        for i in event['rewards']:
            self.threads.append(loadThread(r'https://api.guildwars2.com/v2/items/' + str(i['id'])))
            self.threads[-1].metaEventSignal.connect(self.addReward, Qt.QueuedConnection)
            self.threads[-1].start()

    def addReward(self, signal):
        signal = json.loads(signal)
        setattr(self,str(signal['id']),label(signal))
        getattr(self, str(signal['id'])).setText(signal['name'])
        getattr(self, str(signal['id'])).signal.connect(self.setItemWindow)
        self.vbox.addWidget(getattr(self,str(signal['id'])))
        self.resize(self.vbox.sizeHint())

    def setItemWindow(self, signal):
        self.itemWindow = itemWindow(signal)
        self.itemWindow.show()

class label(QLabel):
    signal = pyqtSignal(dict)
    def __init__(self,event):
        super().__init__()
        self.event = event

    def mouseReleaseEvent(self, QMouseEvent):
        self.signal.emit(self.event)

class frame(QFrame):
    def __init__(self):
        super().__init__()
        self.grid = QGridLayout()

        self.setLayout(self.grid)

    def addEvent(self, event):
        setattr(self,str(event['id']),label(event))
        getattr(self,str(event['id'])).setText(event['name'])
        getattr(self, str(event['id'])).signal.connect(self.setEventWindow)
        self.grid.addWidget(getattr(self,str(event['id'])))
        self.resize(self.grid.sizeHint())

    def setEventWindow(self, event):
        self.eventWindow = eventWindow(event)
        self.eventWindow.show()

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
            setattr(self,'{}Tab'.format(metaEvent),frame())
            self.tab.addTab(getattr(self,'{}Tab'.format(metaEvent)),metaEvent)
            for event in items[metaEvent]:
                self.threads.append(loadThread(r'https://api.guildwars2.com/v2/achievements?ids=',events=event, metaEvent= metaEvent))
                self.threads[-1].eventSignal.connect(self.addTab, Qt.QueuedConnection)
                self.threads[-1].start()

    def addTab(self, event, metaEvent):
        getattr(self,'{}Tab'.format(metaEvent)).addEvent(event)

        self.resize(self.grid.sizeHint())

class application(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        self.window = window()
        self.window.show()
        self.exit(self.exec_())

if __name__ == '__main__':
    app = application()
