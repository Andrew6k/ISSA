#!/usr/bin/env python
from PyQt5 import QtWidgets, QtGui, QtCore,  uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QThread
import socket
import os
import threading
import sys, time


HOST = 'localhost'
PORT = 5005


server_created_flag = False
global server
global conn

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        global server_created_flag
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(600,800)
        MainWindow.setWindowTitle('Server')
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
    
        self.centralwidget.setStyleSheet("background-color:white;")
        
        # Start server button
        self.server_start = QtWidgets.QPushButton(MainWindow)
        self.server_start.setText("Start server")
        self.server_start.setStyleSheet("font: bold; font-size: 15px;")
        self.server_start.setGeometry(QtCore.QRect(200, 170, 200, 40))
        self.server_start.clicked.connect(self.start_server)

        ### Set DTC

        # Set DTC1
        self.dtc1 = QtWidgets.QPushButton(MainWindow)
        self.dtc1 .setText("Set DTC1 active")
        self.dtc1 .setStyleSheet("font: bold; font-size: 15px;")
        self.dtc1 .setGeometry(QtCore.QRect(70, 300, 200, 40))
        self.dtc1.clicked.connect(lambda : self.set_dtc1(7,0.1))

        # Set DTC2
        self.dtc2 = QtWidgets.QPushButton(MainWindow)
        self.dtc2 .setText("Set DTC2 active")
        self.dtc2 .setStyleSheet("font: bold; font-size: 15px;")
        self.dtc2 .setGeometry(QtCore.QRect(70, 370, 200, 40))
        self.dtc2.clicked.connect(lambda : self.set_dtc2(6,0.1))

        # Set DTC3
        self.dtc3= QtWidgets.QPushButton(MainWindow)
        self.dtc3 .setText("Set DTC3 active")
        self.dtc3 .setStyleSheet("font: bold; font-size: 15px;")
        self.dtc3 .setGeometry(QtCore.QRect(70, 440, 200, 40))
        self.dtc3.clicked.connect(lambda : self.set_dtc3(5,0.1))

        # Set DTC4
        self.dtc4 = QtWidgets.QPushButton(MainWindow)
        self.dtc4 .setText("Set DTC4 active")
        self.dtc4 .setStyleSheet("font: bold; font-size: 15px;")
        self.dtc4 .setGeometry(QtCore.QRect(70, 510, 200, 40))
        self.dtc4.clicked.connect(lambda : self.set_dtc4(4,0.1))

        ### LEDS
        # Led 1
        self.led1_state = QtWidgets.QLabel(MainWindow)
        self.led1_state.setGeometry(QtCore.QRect(330, 300, 40,40))

        # Led 2
        self.led2_state = QtWidgets.QLabel(MainWindow)
        self.led2_state.setGeometry(QtCore.QRect(330, 370, 40,40))

        #Led 3
        self.led3_state = QtWidgets.QLabel(MainWindow)
        self.led3_state.setGeometry(QtCore.QRect(330, 441, 40,40))

        # Led 4
        self.led4_state = QtWidgets.QLabel(MainWindow)
        self.led4_state.setGeometry(QtCore.QRect(330, 510, 40,40))

        # Set all DTC's
        self.set_all_dtc = QtWidgets.QPushButton(MainWindow)
        self.set_all_dtc .setText("Set all DTC")
        self.set_all_dtc .setStyleSheet("font: bold; font-size: 15px;")
        self.set_all_dtc .setGeometry(QtCore.QRect(70, 580, 200, 40))
        self.set_all_dtc.clicked.connect(self.set_all)
 
        # Start server label
        self.server_label = QtWidgets.QLabel(self.centralwidget)
        self.server_label.setGeometry(QtCore.QRect(200, 210, 200, 40))
        self.server_label.setStyleSheet("font:bold;font-size: 15px;qproperty-alignment: AlignCenter;")
        
        # Continental image
        self.conti_label = QtWidgets.QLabel(self.centralwidget)
        self.conti_label.setGeometry(QtCore.QRect(110, 30, 400, 100))
        self.conti_label.setStyleSheet("qproperty-alignment: AlignCenter;")
        continental = QtGui.QImage(QtGui.QImageReader('./rsz_conti.png').read())
        self.conti_label.setPixmap(QtGui.QPixmap(continental))
        
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.show()

############################### EXERCISE 0 ###############################
    def start_server(self):
        self.set_all_dtc.setText('Set all DTC')
      
        self.dtc1 .setText("Set DTC1 active")
        self.dtc2 .setText("Set DTC2 active")
        self.dtc3 .setText("Set DTC3 active")
        self.dtc4 .setText("Set DTC4 active")

        self.led1_state.setStyleSheet('')
        self.led2_state.setStyleSheet('')
        self.led3_state.setStyleSheet('')
        self.led4_state.setStyleSheet('')

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((HOST, PORT))
        self.sock.listen()
        self.connection, _ = self.sock.accept()
        self.server_start.setEnabled(False)
        self.recv()
        ''' Complete with necessary code'''

############################### EXERCISE 1 ###############################
    def recv_handler(self,stop_event):
        while True:
            data = self.connection.recv(1024).decode()

            if len(data) > 0:
                print(data)
                if data.startswith('0x3'):
                    diag_mode =bool(data[-1:])
                elif data.startswith('0x2E'):
                    dtc = data[4:-1]
                    color = data[-1:]

                    if dtc == '01':
                        self.set_led0(color)
                    elif dtc == '02':
                        self.set_led1(color)
                    elif dtc == '03':
                        self.set_led2(color)
                    elif dtc == '04':
                        self.set_led3(color)
                else:
                    dtc = data[-2:]
                    if dtc == '01':
                        self.read_dtc1(dtc)
                    elif dtc == '02':
                        self.read_dtc2(dtc)
                    elif dtc == '03':
                        self.read_dtc3(dtc)
                    elif dtc == '04':
                        self.read_dtc4(dtc)

         
    def recv(self):
        self.stop_event = threading.Event()
        self.c_thread=threading.Thread(target=self.recv_handler, args=(self.stop_event,))
        self.c_thread.start()


############################### EXERCISE 2 ###############################
    # DTC1
    def set_dtc1(self,led,bright):
        if led == 0:
            self.led1_state.setStyleSheet('background-color:red;opacity:0.1')
            self.dtc1.setText("Set DTC1 active")
        elif led == 1:
            self.led1_state.setStyleSheet('background-color:green;opacity:0.1')
            self.dtc1.setText("Set DTC1 inactive")
        else:
            if self.led1_state.styleSheet() == 'background-color:red;opacity:0.1':
                self.led1_state.setStyleSheet('background-color:green;opacity:0.1')
                self.dtc1.setText("Set DTC1 inactive")
            else:
                self.led1_state.setStyleSheet('background-color:red;opacity:0.1')
                self.dtc1.setText("Set DTC1 active")
                
    # DTC2
    def set_dtc2(self,led,bright):
        if led == 0:
            self.led2_state.setStyleSheet('background-color:red;opacity:0.1')
            self.dtc2.setText("Set DTC2 active")
        elif led == 1:
            self.led2_state.setStyleSheet('background-color:green;opacity:0.1')
            self.dtc2.setText("Set DTC2 inactive")
        else:
            if self.led2_state.styleSheet() == 'background-color:red;opacity:0.1':
                self.led2_state.setStyleSheet('background-color:green;opacity:0.1')
                self.dtc2.setText("Set DTC2 inactive")
            else:
                self.led2_state.setStyleSheet('background-color:red;opacity:0.1')
                self.dtc2.setText("Set DTC2 active")
        

    # DTC3
    def set_dtc3(self,led,bright):
        if led == 0:
            self.led3_state.setStyleSheet('background-color:red;opacity:0.1')
            self.dtc3.setText("Set DTC3 active")
        elif led == 1:
            self.led3_state.setStyleSheet('background-color:green;opacity:0.1')
            self.dtc3.setText("Set DTC3 inactive")
        else:
            if self.led3_state.styleSheet() == 'background-color:red;opacity:0.1':
                self.led3_state.setStyleSheet('background-color:green;opacity:0.1')
                self.dtc3.setText("Set DTC3 inactive")
            else:
                self.led3_state.setStyleSheet('background-color:red;opacity:0.1')
                self.dtc3.setText("Set DTC3 active")
        
    # DTC4
    def set_dtc4(self,led,bright):
        if led == 0:
            self.led4_state.setStyleSheet('background-color:red;opacity:0.1')
            self.dtc4.setText("Set DTC4 active")
        elif led == 1:
            self.led4_state.setStyleSheet('background-color:green;opacity:0.1')
            self.dtc4.setText("Set DTC4 inactive")
        else:
            if self.led4_state.styleSheet() == 'background-color:red;opacity:0.1':
                self.led4_state.setStyleSheet('background-color:green;opacity:0.1')
                self.dtc4.setText("Set DTC4 inactive")
            else:
                self.led4_state.setStyleSheet('background-color:red;opacity:0.1')
                self.dtc4.setText("Set DTC4 active")
        

    def set_all(self):
        led1 = self.led1_state.styleSheet()
        led2 = self.led2_state.styleSheet()
        led3 = self.led3_state.styleSheet()
        led4 = self.led4_state.styleSheet()

        if led1 == 'background-color:red;opacity:0.1' and led2 == 'background-color:red;opacity:0.1' and led3 == 'background-color:red;opacity:0.1' and led4 == 'background-color:red;opacity:0.1':
            self.set_dtc1(1, 0.1)
            self.dtc1.setText("Set DTC1 inactive")
            self.set_dtc2(1, 0.1)
            self.dtc2.setText("Set DTC2 inactive")
            self.set_dtc3(1, 0.1)
            self.dtc3.setText("Set DTC3 inactive")
            self.set_dtc4(1, 0.1)
            self.dtc4.setText("Set DTC4 inactive")
        else: 
            self.set_dtc1(0, 0.1)
            self.dtc1.setText("Set DTC1 active")
            self.set_dtc2(0, 0.1)
            self.dtc2.setText("Set DTC2 active")
            self.set_dtc3(0, 0.1)
            self.dtc3.setText("Set DTC3 active")
            self.set_dtc4(0, 0.1)
            self.dtc4.setText("Set DTC4 active")
            
############################### EXERCISE 3 ###############################          
    def read_dtc1(self,data):
        message = '0x6201'

        if self.led1_state.styleSheet() == 'background-color:red;opacity:0.1':
            message += '25500'
        else:
            message += '02550'
        
        self.connection.send(message.encode())
    
    def read_dtc2(self,data):
        message = '0x6202'

        if self.led2_state.styleSheet() == 'background-color:red;opacity:0.1':
            message += '25500'
        else:
            message += '02550'
        
        self.connection.send(message.encode())
    

    def read_dtc3(self,data):
        message = '0x6203'

        if self.led3_state.styleSheet() == 'background-color:red;opacity:0.1':
            message += '25500'
        else:
            message += '02550'
        
        self.connection.send(message.encode())
    


    def read_dtc4(self,data):
        message = '0x6204'

        if self.led4_state.styleSheet() == 'background-color:red;opacity:0.1':
            message += '25500'
        else:
            message += '02550'
        
        self.connection.send(message.encode())
    

############################### EXERCISE 4 ###############################
    def set_led0(self,data):
        if data == "0":
           self.set_dtc1(0, 0.1)
           self.dtc1.setText("Set DTC1 active")
        else:
            self.set_dtc1(1, 0.1)
            self.dtc1.setText("Set DTC1 inactive")


    def set_led1(self,data):
        if data == "0":
            self.set_dtc2(0, 0.1)
            self.dtc2.setText("Set DTC2 active")
        else:
            self.set_dtc2(1, 0.1)
            self.dtc2.setText("Set DTC2 inactive")



    def set_led2(self,data):
        if data == "0":
            self.set_dtc3(0, 0.1)
            self.dtc3.setText("Set DTC3 active")
        else:
            self.set_dtc3(1, 0.1)
            self.dtc3.setText("Set DTC3 inactive")



    def set_led3(self,data):
        if data == "0":
            self.set_dtc4(0, 0.1)
            self.dtc4.setText("Set DTC4 active")
        else:
            self.set_dtc4(1, 0.1)
            self.dtc4.setText("Set DTC4 inactive")


##########################################################################
      
            
class MyWindow(QtWidgets.QMainWindow):
    def closeEvent(self,event):
        result = QtWidgets.QMessageBox.question(self,
                      "Confirm Exit",
                      "Are you sure you want to exit ?",
                      QtWidgets.QMessageBox.Yes| QtWidgets.QMessageBox.No)        

        
        if result == QtWidgets.QMessageBox.Yes:
            event.accept()
        elif result == QtWidgets.QMessageBox.No:
            event.ignore()

    def center(self):
        frameGm = self.frameGeometry()
        screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
        centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

def kill_proc_tree(pid, including_parent=True):    
    parent = psutil.Process(pid)
    if including_parent:
        parent.kill()

def main():
    global server_created_flag
    import sys
    global app
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MyWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.center()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

me = os.getpid()
kill_proc_tree(me)
    
