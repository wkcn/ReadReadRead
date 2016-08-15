#coding=utf-8
from PyQt4 import QtCore, QtGui
import sys
import MainWindow
import ReadBook
import Queue
import ICBDict
import os
import pickle
import copy
import threading

dicts = {}

def look_dict(word):
    if not dicts.has_key(word):
        icb = ICBDict.ICBDict(word)
        dicts[word] = icb
    return dicts[word]

def get_text(icb):
    text = ""
    for p,a in icb["trans"]:
        text += p + ' ' + a + '\n'
    text += '==========\n'
    for p,a in icb["ex"]:
        text += p + ' ' + a + '\n'
    return text

old_word = []
know_word = []

class QueueA:
    def __init__(self):
        self.queue = []
        self.i = 0
        self.j = 0
    def put(self, e):
        self.queue.append(e)
        self.j += 1
    def get(self):
        e = self.queue[self.i]
        self.i += 1
        return e
    def empty(self):
        return self.i >= self.j

T_BUFFER = {}
class ICB_Buffer(threading.Thread):
    def __init__(self, word):
        threading.Thread.__init__(self)
        self.word = word
    def run(self):
        global dicts
        if not dicts.has_key(self.word):
            icb = ICBDict.ICBDict(self.word)
            dicts[self.word] = icb


class MainWindow_(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow_, self).__init__(parent)
        self.main = MainWindow.Ui_MainWindow()
        self.main.setupUi(self)
        QtCore.QObject.connect(self.main.pushButton, QtCore.SIGNAL("clicked()"), self.know)
        QtCore.QObject.connect(self.main.pushButton_2, QtCore.SIGNAL("clicked()"), self.ouch)
        QtCore.QObject.connect(self.main.pushButton_3, QtCore.SIGNAL("clicked()"), self.easy)
        QtCore.QObject.connect(self.main.pushButton_eng, QtCore.SIGNAL("clicked()"), lambda : self.ps_click(0))
        QtCore.QObject.connect(self.main.pushButton_usa, QtCore.SIGNAL("clicked()"), lambda : self.ps_click(1))
        self.smallQueue = Queue.Queue()
        self.largeQueue = QueueA()
        words = ReadBook.read_book("galaxy.txt")
        self.words = words
        global know_word, old_word
        know_word = ReadBook.get_know_word()
        old_word = copy.copy(know_word)
        print 'you know %d words' % len(know_word)
        for word in words:
            if word not in know_word:
                self.largeQueue.put(word)
        self.isLargeQueue = True
        self.show_info = False
        self.get_next_word()
    def show_word(self, word):
        self.main.label.setText(word)
        icb = look_dict(word)
        self.icb = icb
        if len(icb["trans"]):
            self.word = word
            self.main.pushButton_eng.setText(icb["ps"][0])
            self.main.pushButton_usa.setText(icb["ps"][1])
            ratio = len(know_word) * 100.0 / len(self.words)
            self.main.progressBar.setValue(ratio)
            #self.main.textBrowser.setText(get_text(icb))
            self.main.textBrowser.setText("")
            self.show_info = False
        else:
            if word not in know_word:
                 know_word.append(word)
            self.get_next_word()
    def get_next_word(self):
        #buffer
        for i in range(self.largeQueue.i, min(self.largeQueue.i + 10, self.largeQueue.j)):
            word = self.largeQueue.queue[i]
            if not T_BUFFER.has_key(word) and not dicts.has_key(word):
                T_BUFFER[word] = ICB_Buffer(word)
                T_BUFFER[word].setDaemon(True)
                T_BUFFER[word].start()
            
        if self.largeQueue.empty():
            return
        if self.isLargeQueue:
            word = self.largeQueue.get()
            if self.smallQueue.qsize() >= 10:
                self.isLargeQueue = False
        else:
            word = self.smallQueue.get()
            if self.smallQueue.empty():
                self.isLargeQueue = True

        self.show_info = False
        self.show_word(word)

    def easy(self):
        if self.word not in know_word:
             know_word.append(self.word)
        self.get_next_word()

    def know(self):
        if self.show_info:
            self.get_next_word()
        else:
            self.show_info = True
            self.main.textBrowser.setText(get_text(self.icb))

    def ouch(self):
        if self.show_info: 
            self.smallQueue.put(self.word)
            self.largeQueue.put(self.word)
            self.get_next_word()
        else:
            self.show_info = True
            self.main.textBrowser.setText(get_text(self.icb))

    def ps_click(self, i):
        url = self.icb["voice"][i]
        os.system('mplayer %s' % url)
        
        

app = QtGui.QApplication(sys.argv)
main = MainWindow_()
main.show()
app.exec_()

KnowFile = open("know.txt", "a")
for word in know_word:
    if word not in old_word:
        KnowFile.write("%s\n" % word)

print "exit! :-)"
