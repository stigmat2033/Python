import sys, urllib.request, json
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QGridLayout, QTabWidget, QFrame, QVBoxLayout
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class loadDataThread(QThread):
    # Тред для загрузки текстовой информации (json)
    signal = pyqtSignal(str)
    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        self.signal.emit(urllib.request.urlopen(self.url).read().decode('UTF-8'))

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

class frame(QWidget):
    def __init__(self):
        super().__init__()
        self.vbox = QVBoxLayout()

        self.setLayout(self.vbox)

        self.threads = []

    def getEvent(self, event):
        self.threads.append(loadDataThread(r'https://api.guildwars2.com/v2/achievements?id='+str(event['id'])))
        self.threads[-1].signal.connect(self.addEvent, Qt.QueuedConnection)
        self.threads[-1].start()

    def addEvent(self, signal):
        signal = json.loads(signal)
        print(type(signal))
        setattr(self,str(signal['id']),label(signal))
        getattr(self,str(signal['id'])).setText(signal['name'])
        getattr(self, str(signal['id'])).signal.connect(self.setEventWindow)
        self.vbox.addWidget(getattr(self,str(signal['id'])))
        # self.resize(self.grid.sizeHint())

    def setEventWindow(self, event):
        self.eventWindow = eventWindow(event)
        self.eventWindow.show()

class dailyTab(QWidget):
    def __init__(self):
        super().__init__()
        # Виджет для дейлков
        # Содержит содержит главный таб виджет для дейликов
        self.tab = QTabWidget()

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.tab)
        self.setLayout(self.vbox)

        self.threads = []
        # При ините создаём тред для получения дейликов
        self.loadDataThread = loadDataThread(r'https://api.guildwars2.com/v2/achievements/daily')
        self.loadDataThread.signal.connect(self.getEvent, Qt.QueuedConnection)
        self.loadDataThread.start()

    def getEvent(self, signal):
        signal = json.loads(signal)
        for metaEvent in signal.keys():
            setattr(self,metaEvent,frame())
            self.tab.addTab(getattr(self,metaEvent),metaEvent)
            for event in signal[metaEvent]:
                if (event['level']['max'] == 80 and metaEvent == 'pve') or metaEvent != 'pve':
                    getattr(self,metaEvent).getEvent(event)

    def addTab(self, event, metaEvent):
        getattr(self,'{}Tab'.format(metaEvent)).addEvent(event)

        self.resize(self.grid.sizeHint())

class mainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Виджет для главного таб виджета
        # Содержит вкладки для дейликов и т.д.
        self.vbox = QVBoxLayout()

        self.dailyTab = dailyTab()

        self.tab = QTabWidget()
        self.tab.addTab(self.dailyTab,'Daily events')

        self.vbox.addWidget(self.tab)
        self.setLayout(self.vbox)

class application(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        self.mainWindow = mainWindow()
        self.mainWindow.resize(400,400)
        self.mainWindow.show()
        self.exit(self.exec_())

if __name__ == '__main__':
    app = application()
