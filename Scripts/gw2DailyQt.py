import sys, urllib.request, json
from PyQt5.QtWidgets import QApplication, QWidget, QFrame, QVBoxLayout, QGridLayout, QScrollArea, QLabel
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap

class loadThread(QThread):
    signal = pyqtSignal(bytes,str)
    def __init__(self, url, arg):
        super().__init__()
        self.url = url
        self.arg = str(arg)

    def run(self):
        self.signal.emit(urllib.request.urlopen(self.url).read(),self.arg)

class frame(QFrame):
    def __init__(self, pix, name, reward, pix2, num):
        super().__init__()
        # self.resize(60,40)
        self.grid = QGridLayout()
        self.grid.setSpacing(3)

        self.logo = QLabel()
        self.logo.setPixmap(pix)

        self.name = QLabel()
        self.name.setText(name)

        self.reward = QLabel()
        self.reward.setText(reward)

        self.pic = QLabel()
        self.pic.setPixmap(pix2)

        self.num = num

        self.grid.addWidget(self.logo,1,1,3,1)
        self.grid.addWidget(self.name,1,2,2,1)
        self.grid.addWidget(self.reward,2,2,2,1, Qt.AlignRight)
        self.grid.addWidget(self.pic,2,3,2,1)
        self.setLayout(self.grid)

class mainFrame(QFrame):
    def __init__(self, data, pix):
        super().__init__()
        self.data = data
        self.pix = pix

        self.grid = QGridLayout()
        self.grid.setSpacing(3)

        self.initFrames()

    def initFrames(self):
        self.threads = []
        x, y = 1, 1
        for metaEvent in self.data.keys():
            for event in self.data[metaEvent]:
                setattr(self,'form{}'.format(str(event['id'])),frame(self.pix,'Event loading...','0',self.pix2))
                if x == 4:
                    x = 1
                    y += 1
                self.grid.addWidget(getattr(self,'form{}'.format(event['id'])),y,x,1,1)
                x += 1
                self.threads.append()
        self.setLayout(self.grid)

class window(QWidget):
    def __init__(self):
        super().__init__()
        self.area = QScrollArea()
        self.vbox = QVBoxLayout()

        self.done = 0

        self.threads = []
        self.threads.append(loadThread(r'https://api.guildwars2.com/v2/achievements/daily','events'))
        self.threads.append(loadThread(r'https://wiki.guildwars2.com/images/c/ca/Explorer.png','pve'))
        self.threads.append(loadThread(r'https://wiki.guildwars2.com/images/c/ca/PvP_Conqueror.png','pvp'))
        self.threads.append(loadThread(r'https://wiki.guildwars2.com/images/d/d2/World_vs_World.png','wvw'))
        self.threads.append(loadThread(r'https://wiki.guildwars2.com/images/e/e1/Hall_of_Monuments_%28achievement%29.png','special'))
        self.threads.append(loadThread(r'https://wiki.guildwars2.com/images/thumb/6/6b/Arenanet_Points.png/20px-Arenanet_Points.png','point'))
        for i in self.threads:
            i.signal.connect(self.getData, Qt.QueuedConnection)
            i.start()

        # self.thread = loadThread(r'https://api.guildwars2.com/v2/achievements/daily')
        # self.thread.signal.connect(self.getData, Qt.QueuedConnection)
        # self.thread.start()

        # self.thread2 = loadThread(r'https://wiki.guildwars2.com/images/1/14/Daily_Achievement.png')
        # self.thread2.signal.connect(self.getImage, Qt.QueuedConnection)
        # self.thread2.start()

        # self.thread3 = loadThread(r'https://wiki.guildwars2.com/images/thumb/6/6b/Arenanet_Points.png/20px-Arenanet_Points.png')
        # self.thread3.signal.connect(self.getImage2, Qt.QueuedConnection)
        # self.thread3.start()

    def ready(self):
        self.done += 1
        if self.done == 5:
            print('setting up main frame')
            self.mainFrame = mainFrame(self.data, self.pix)
            self.area.setWidget(self.mainFrame)
            self.vbox.addWidget(self.area)
            self.setLayout(self.vbox)

    def getData(self, data, flag):
        pass

class application(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        self.window = window()
        # self.window.resize(600,600)
        self.window.show()
        self.exit(self.exec_())

if __name__ == '__main__':
    app = application()
