import sys, urllib.request, json
from PyQt5.QtWidgets import QApplication, QWidget, QFrame, QVBoxLayout, QGridLayout, QScrollArea, QLabel, QProgressBar, QSizePolicy
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QObject
from PyQt5.QtGui import QPixmap

class eventObject(QObject):
    signal = pyqtSignal(int)
    def __init__(self, type, id):
        super().__init__()
        self.type = type
        self.id = id
        self.thread = loadThread(r'https://api.guildwars2.com/v2/achievements?ids='+str(self.id))
        self.thread.signal.connect(self.addData, Qt.QueuedConnection)
        if self.type == 'pve':
            self.thread2 = loadThread(r'https://wiki.guildwars2.com/images/c/ca/Explorer.png')
        elif self.type == 'wvw':
            self.thread2 = loadThread(r'https://wiki.guildwars2.com/images/d/d2/World_vs_World.png')
        elif self.type == 'pvp':
            self.thread2 = loadThread(r'https://wiki.guildwars2.com/images/c/ca/PvP_Conqueror.png')
        else:
            self.thread2 = loadThread(r'https://wiki.guildwars2.com/images/e/e1/Hall_of_Monuments_%28achievement%29.png')
        self.thread2.signal.connect(self.addImage, Qt.QueuedConnection)
        self.thread3 = loadThread(r'https://wiki.guildwars2.com/images/thumb/6/6b/Arenanet_Points.png/20px-Arenanet_Points.png')
        self.thread3.signal.connect(self.addPic, Qt.QueuedConnection)

    def start(self):
        self.thread.start()
        self.thread2.start()
        self.thread3.start()

    def addData(self, signal):
        self.text = json.loads(signal.decode('UTF-8'))
        self.signal.emit(1)

    def addImage(self, signal):
        self.pix = signal
        self.signal.emit(1)

    def addPic(self, signal):
        self.pic = signal
        self.signal.emit(1)

class loadThread(QThread):
    signal = pyqtSignal(bytes)
    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        self.signal.emit(urllib.request.urlopen(self.url).read())

class frame(QFrame):
    def __init__(self,name, pix, pix2, reward):
        super().__init__()
        self.grid = QGridLayout()
        self.grid.setSpacing(3)

        self.logo = QLabel()
        self.pix = QPixmap()
        self.pix.loadFromData(pix)
        self.logo.setPixmap(self.pix)

        self.name = QLabel()
        if len(name) > 25:
            name = (name[:25]+'...')
        self.name.setText(name)

        self.reward = QLabel()
        self.reward.setText(reward)

        self.pic = QLabel()
        self.pix2 = QPixmap()
        self.pix2.loadFromData(pix2)
        self.pic.setPixmap(self.pix2)

        self.grid.addWidget(self.logo,2,1,3,1)
        self.grid.addWidget(self.name,1,1,1,3)
        self.grid.addWidget(self.reward,2,2,2,1, Qt.AlignRight)
        self.grid.addWidget(self.pic,2,3,2,1)
        self.setLayout(self.grid)

class mainFrame(QFrame):
    def __init__(self,data):
        super().__init__()
        self.data = data

        self.grid = QGridLayout()
        self.grid.setSpacing(3)

        self.X = 1
        self.Y = 1

        for i in self.data.keys():
            setattr(self,'form{}'.format(str(i)),frame(
                self.data[i].text[0]['name'],self.data[i].pix,self.data[i].pic,'0'
            ))
            if self.X == 4:
                self.X = 1
                self.Y += 1
            self.grid.addWidget(
                getattr(self,'form{}'.format(str(i))),self.Y,self.X,1,1
            )
            self.X += 1
        self.setLayout(self.grid)

class window(QWidget):
    def __init__(self,data):
        super().__init__()
        self.data = data

        self.area = QScrollArea()
        self.vbox = QVBoxLayout()

        self.mainFrame = mainFrame(self.data)

        self.area.setWidget(self.mainFrame)
        self.area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.pref = QSizePolicy()
        self.pref.setHorizontalPolicy(QSizePolicy.Maximum)
        self.area.setSizePolicy(self.pref)
        self.vbox.addWidget(self.area)
        self.setLayout(self.vbox)
        self.show()

class launcher(QWidget):
    signal = pyqtSignal(dict)
    def __init__(self):
        super().__init__()
        self.vbox = QVBoxLayout()

        self.bar = QProgressBar()
        self.bar.setMaximum(5)

        self.setWindowTitle('Loading data')
        self.vbox.addWidget(self.bar)
        self.setLayout(self.vbox)

        self.data = {}
        self.total = 0
        self.value = 0
        self.thread = loadThread(r'https://api.guildwars2.com/v2/achievements/daily')
        self.thread.signal.connect(self.getData, Qt.QueuedConnection)
        self.thread.start()

    def sendData(self):
        self.signal.emit(self.data)
        self.close()

    def progress(self):
        self.value += 1
        self.bar.setValue(self.value)
        if self.bar.value() == self.total:
            self.sendData()

    def getData(self, signal):
        items = json.loads(signal.decode('UTF-8'))
        for metaEvent in items.keys():
            for event in items[metaEvent]:
                self.total += 3
                self.data.setdefault(event['id'], eventObject(metaEvent, event['id']))
                self.data[event['id']].signal.connect(self.progress)

        self.bar.setMaximum(self.total)
        for i in self.data.keys():
            self.data[i].start()

class application(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        self.launcher = launcher()
        self.launcher.signal.connect(self.setData, Qt.QueuedConnection)
        self.launcher.show()
        self.exit(self.exec_())
        self.window = window(self.data)
        self.window.show()
        self.exit(self.exec_())

    def setData(self, signal):
        self.data = signal

if __name__ == '__main__':
    app = application()
    print(app)
