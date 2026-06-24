import sys
import random
import string
from datetime import datetime
from PySide6.QtCore import QCoreApplication, QMetaObject, QRect, QTimer, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (QApplication, QComboBox, QLabel, QMainWindow, 
                             QMenuBar, QPlainTextEdit, QPushButton, QStatusBar, 
                             QWidget, QMessageBox, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy)
from PySide6.QtSerialPort import QSerialPortInfo

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(850, 600) 
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
    
        self.cb_port = QComboBox(self.centralwidget)
        self.cb_baud = QComboBox(self.centralwidget)
        self.date = QLabel(self.centralwidget)
        self.Refresh = QPushButton(self.centralwidget)
        self.plainTextEdit = QPlainTextEdit(self.centralwidget)
        self.start_stop = QPushButton(self.centralwidget)

        self.plainTextEdit.setStyleSheet(u"QPlainTextEdit { background-color: black; color: #00FF00; font-family: 'Consolas'; font-size: 12pt; }")
        self.plainTextEdit.setReadOnly(True)
        
        self.Refresh.setFont(QFont("Arial", 10, QFont.Bold))
        self.start_stop.setMinimumWidth(80)
        self.Refresh.setMinimumWidth(80)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Innovita Terminal", None))
        self.Refresh.setText("Refresh")

class TerminalApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.top_layout = QHBoxLayout()
        self.top_layout.setContentsMargins(10, 10, 10, 10) 
        self.top_layout.setSpacing(10) 

        self.top_layout.addWidget(self.ui.date)

        self.top_layout.addStretch() 
        
        self.top_layout.addWidget(self.ui.cb_port)
        self.top_layout.addWidget(self.ui.cb_baud)
        self.top_layout.addWidget(self.ui.start_stop)
        self.top_layout.addWidget(self.ui.Refresh)

        self.main_layout = QVBoxLayout(self.ui.centralwidget)
        self.main_layout.addLayout(self.top_layout) 
        self.main_layout.addWidget(self.ui.plainTextEdit) 

        self.data_buffer = ""
        self.ui.start_stop.setText("Start")

        self.ui.cb_baud.addItem("Select Baud")
        self.ui.cb_baud.addItems(["9600", "19200", "38400", "57600", "115200"])
        
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_datetime)
        self.clock_timer.start(1000)
        self.update_datetime()

        self.simulation_timer = QTimer(self)
        self.simulation_timer.timeout.connect(self.generate_fake_data)

        self.refresh_ports()
        self.ui.Refresh.clicked.connect(self.clear_terminal) 
        self.ui.start_stop.clicked.connect(self.toggle_simulation)

    def update_datetime(self):
        self.ui.date.setText(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))

    def refresh_ports(self):
        self.ui.cb_port.clear()
        self.ui.cb_port.addItem("Add Port")
        self.ui.cb_port.addItem("COM2")
        for port in QSerialPortInfo.availablePorts():
            self.ui.cb_port.addItem(port.portName())

    def clear_terminal(self):
        if QMessageBox.question(self, "Refresh", "Are you sure you want to clear the terminal?", 
                               QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            self.ui.plainTextEdit.clear()

    def toggle_simulation(self):
        if self.simulation_timer.isActive():
            self.simulation_timer.stop()
            self.ui.start_stop.setText("Start")
            self.ui.plainTextEdit.appendPlainText("=== Simulation is closed ===") 
        else:
            if self.ui.cb_port.currentIndex() == 0 or self.ui.cb_baud.currentIndex() == 0:
                QMessageBox.warning(self, "Warning", "Select a valid port and baud rate")
                return
            
            self.simulation_timer.start(1000)
            self.ui.start_stop.setText("Stop")
            self.ui.plainTextEdit.appendPlainText(f"=== {self.ui.cb_port.currentText()} Connection Started ===")
            self.data_buffer = ""

    def generate_fake_data(self):
        s_seq = ''.join(random.choices(string.ascii_lowercase, k=2))
        e_seq = ''.join(random.choices(string.ascii_lowercase, k=2))
        payload = f"{s_seq}, {random.randint(10,99)}, 100, {random.randint(1000,9999)}, {e_seq} \0\n"
        self.data_buffer += payload
        while '\n' in self.data_buffer:
            line, self.data_buffer = self.data_buffer.split('\n', 1)
            self.parse_and_display(line)

    def parse_and_display(self, line):
        clean = line.replace('\0', '').strip()
        parts = [p.strip() for p in clean.split(',')]
        if len(parts) >= 5:
            out = f"[{datetime.now().strftime('%H:%M:%S')}]: Start: {parts[0]} Node {parts[1]} Data: {parts[3]} End: {parts[-1]}"
            self.ui.plainTextEdit.appendPlainText(out)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TerminalApp()
    window.show() 
    sys.exit(app.exec())
