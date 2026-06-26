import sys
from datetime import datetime
from PySide6.QtCore import QCoreApplication, QMetaObject, QRect, QTimer, Qt, QStringListModel, QEvent
from PySide6.QtGui import QFont, QIcon
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel, 
                               QLineEdit, QMainWindow, QMenuBar, QPlainTextEdit, 
                               QPushButton, QSizePolicy, QStatusBar, QWidget, QMessageBox, QVBoxLayout, QSpacerItem, QCompleter, QListWidget, QListWidgetItem)
from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1150, 610) # Listeyi sığdırmak için genişlik biraz artırıldı
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.cb_port = QComboBox(self.centralwidget)
        self.cb_port.setObjectName(u"cb_port")
        self.cb_port.setGeometry(QRect(610, 70, 111, 26))
        font = QFont()
        font.setBold(False)
        self.cb_port.setFont(font)
        self.cb_baud = QComboBox(self.centralwidget)
        self.cb_baud.setObjectName(u"cb_baud")
        self.cb_baud.setGeometry(QRect(730, 70, 121, 26))
        self.date = QLabel(self.centralwidget)
        self.date.setObjectName(u"date")
        self.date.setGeometry(QRect(30, 30, 111, 20))
        self.Refresh = QPushButton(self.centralwidget)
        self.Refresh.setObjectName(u"Refresh")
        self.Refresh.setGeometry(QRect(950, 70, 81, 26))
        font1 = QFont()
        font1.setBold(True)
        self.Refresh.setFont(font1)
        self.plainTextEdit = QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setGeometry(QRect(30, 110, 1001, 421))
        self.plainTextEdit.setStyleSheet(u"QPlainTextEdit {\n"
"    background-color: black;\n"
"    color: #00FF00; \n"
"    font-family: \"Consolas\", \"Courier New\", monospace;\n"
"    font-size: 12pt;\n"
"}")
        self.plainTextEdit.setReadOnly(True)
        self.start_stop = QPushButton(self.centralwidget)
        self.start_stop.setObjectName(u"start_stop")
        self.start_stop.setGeometry(QRect(860, 70, 81, 26))
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(30, 70, 492, 28))
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_node_id = QLabel(self.widget)
        self.label_node_id.setObjectName(u"label_node_id")

        self.horizontalLayout.addWidget(self.label_node_id)

        self.le_node_id = QLineEdit(self.widget)
        self.le_node_id.setObjectName(u"le_node_id")

        self.horizontalLayout.addWidget(self.le_node_id)

        self.label_msg_id = QLabel(self.widget)
        self.label_msg_id.setObjectName(u"label_msg_id")

        self.horizontalLayout.addWidget(self.label_msg_id)

        self.le_msg_id = QLineEdit(self.widget)
        self.le_msg_id.setObjectName(u"le_msg_id")

        self.horizontalLayout.addWidget(self.le_msg_id)

        self.btn_apply_filter = QPushButton(self.widget)
        self.btn_apply_filter.setObjectName(u"btn_apply_filter")

        self.horizontalLayout.addWidget(self.btn_apply_filter)

        self.btn_clear_filter = QPushButton(self.widget)
        self.btn_clear_filter.setObjectName(u"btn_clear_filter")

        self.horizontalLayout.addWidget(self.btn_clear_filter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1057, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Innovita Terminal", None))
        self.date.setText(QCoreApplication.translate("MainWindow", u"Date", None))
        self.Refresh.setText(QCoreApplication.translate("MainWindow", u"Refresh", None))
        self.start_stop.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.label_node_id.setText(QCoreApplication.translate("MainWindow", u"Node ID", None))
        self.label_msg_id.setText(QCoreApplication.translate("MainWindow", u"MSG ID", None))
        self.btn_apply_filter.setText(QCoreApplication.translate("MainWindow", u"Add Filter", None)) # 'Apply Filters' -> 'Add Filter' olarak değiştirildi
        self.btn_clear_filter.setText(QCoreApplication.translate("MainWindow", u"Clear Filters", None))


class FilterWidget(QWidget):
    """Filtre listesindeki her bir satır için özel widget (Görünürlük ve Silme butonları ile birlikte)"""
    def __init__(self, node_id, msg_id, on_toggle, on_delete, parent=None):
        super().__init__(parent)
        self.node_id = node_id
        self.msg_id = msg_id
        self.is_active = True
        self.on_toggle = on_toggle
        self.on_delete = on_delete

        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 2, 5, 2)
        layout.setSpacing(5)

        # Filtre metnini oluşturma
        text_parts = []
        if node_id: text_parts.append(f"Node: {node_id}")
        if msg_id: text_parts.append(f"MSG: {msg_id}")
        filter_text = " | ".join(text_parts)

        self.label = QLabel(filter_text, self)
        layout.addWidget(self.label)
        layout.addStretch()

        # Görünürlük / Aktiflik Butonu (göz simgesi yerine 'O' / 'X' mantığı veya metin kullanıldı)
        self.btn_visible = QPushButton("Active", self)
        self.btn_visible.setFixedWidth(55)
        self.btn_visible.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-size: 10px; font-weight: bold; }")
        self.btn_visible.clicked.connect(self.toggle_active)
        layout.addWidget(self.btn_visible)

        # Silme Butonu
        self.btn_delete = QPushButton("X", self)
        self.btn_delete.setFixedWidth(25)
        self.btn_delete.setStyleSheet("QPushButton { background-color: #f44336; color: white; font-weight: bold; }")
        self.btn_delete.clicked.connect(self.delete_filter)
        layout.addWidget(self.btn_delete)

    def toggle_active(self):
        self.is_active = not self.is_active
        if self.is_active:
            self.btn_visible.setText("Active")
            self.btn_visible.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-size: 10px; font-weight: bold; }")
            self.label.setStyleSheet("")
        else:
            self.btn_visible.setText("Passive")
            self.btn_visible.setStyleSheet("QPushButton { background-color: #757575; color: white; font-size: 10px; font-weight: bold; }")
            self.label.setStyleSheet("color: #757575; text-decoration: line-through;")
        
        self.on_toggle()

    def delete_filter(self):
        self.on_delete(self)


class TerminalApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.serial_port = QSerialPort(self)
        self.serial_port.readyRead.connect(self.read_serial_data)

        # Filtreleri saklayacağımız liste dinamik nesneleri tutacak
        self.active_filters = []

        self.top_layout = QHBoxLayout()
        self.top_layout.setContentsMargins(10, 10, 10, 10)
        self.top_layout.setSpacing(10)

        self.top_layout.addWidget(self.ui.date)
        self.top_layout.addStretch()
        self.top_layout.addWidget(self.ui.cb_port)
        self.top_layout.addWidget(self.ui.cb_baud)
        self.top_layout.addWidget(self.ui.start_stop)
        self.top_layout.addWidget(self.ui.Refresh)

        # SAĞ PANEL: Filtre listesi başlığı ve QListWidget bileşeni
        self.right_panel_layout = QVBoxLayout()
        self.filter_list_label = QLabel("Active Filters List", self)
        font_title = QFont()
        font_title.setBold(True)
        self.filter_list_label.setFont(font_title)
        
        self.filter_list_widget = QListWidget(self)
        self.filter_list_widget.setFixedWidth(250) # Sağ tarafta sabit genişlik
        
        self.right_panel_layout.addWidget(self.filter_list_label)
        self.right_panel_layout.addWidget(self.filter_list_widget)

        # ORTA PANEL: Terminal ve Üst filtre barı
        self.center_layout = QVBoxLayout()
        self.center_layout.addWidget(self.ui.widget)  
        self.center_layout.addWidget(self.ui.plainTextEdit)

        # ANA ALT LAYOUT: Terminal (Sol) ve Filtre Listesi (Sağ) yan yana
        self.content_layout = QHBoxLayout()
        self.content_layout.addLayout(self.center_layout, stretch=4)
        self.content_layout.addLayout(self.right_panel_layout, stretch=1)

        self.main_layout = QVBoxLayout(self.ui.centralwidget)
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addLayout(self.content_layout)

        self.data_buffer = ""

        # --- AUTOCOMPLETE & HISTORY SETUP ---
        self.node_history = []
        self.msg_history = []

        # Node ID Completer
        self.node_model = QStringListModel(self.node_history, self)
        self.node_completer = QCompleter(self.node_model, self)
        self.node_completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.ui.le_node_id.setCompleter(self.node_completer)
        self.ui.le_node_id.installEventFilter(self)

        # MSG ID Completer
        self.msg_model = QStringListModel(self.msg_history, self)
        self.msg_completer = QCompleter(self.msg_model, self)
        self.msg_completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.ui.le_msg_id.setCompleter(self.msg_completer)
        self.ui.le_msg_id.installEventFilter(self)
        # ------------------------------------

        self.ui.start_stop.setText("Start")

        self.ui.cb_baud.addItem("Select Baud")
        self.ui.cb_baud.addItems(["9600", "19200", "38400", "57600", "115200", "230400", "460800", "921600"])
        
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_datetime)
        self.clock_timer.start(1000)
        self.update_datetime()

        self.refresh_ports()
        
        self.ui.Refresh.clicked.connect(self.clear_terminal)
        self.ui.start_stop.clicked.connect(self.toggle_connection)
        self.ui.btn_apply_filter.clicked.connect(self.add_filter) # apply_filters fonksiyonu add_filter yapıldı
        self.ui.btn_clear_filter.clicked.connect(self.clear_filters)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if obj == self.ui.le_node_id:
                self.node_completer.setCompletionPrefix("")
                self.node_completer.complete()
            elif obj == self.ui.le_msg_id:
                self.msg_completer.setCompletionPrefix("")
                self.msg_completer.complete()
        return super().eventFilter(obj, event)

    def update_history(self, new_value, history_list, model):
        if not new_value:
            return
        if new_value in history_list:
            history_list.remove(new_value)
        history_list.insert(0, new_value)
        if len(history_list) > 5:
            history_list.pop()
        model.setStringList(list(history_list))

    def update_datetime(self):
        self.ui.date.setText(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))

    def refresh_ports(self):
        self.ui.cb_port.clear()
        self.ui.cb_port.addItem("Select Port")
        for port in QSerialPortInfo.availablePorts():
            self.ui.cb_port.addItem(port.portName())

    def clear_terminal(self):
        if QMessageBox.question(self, "Refresh", "Are you sure you want to clear the terminal?",
                                QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            self.ui.plainTextEdit.clear()

    def add_filter(self):
        """Kutulardaki verilere göre listeye yeni bir filtre varyasyonu ekler"""
        node_id_str = self.ui.le_node_id.text().strip()
        msg_id_str = self.ui.le_msg_id.text().strip()

        if not node_id_str and not msg_id_str:
            QMessageBox.warning(self, "Empty Input", "Please enter at least a Node ID or a MSG ID to add a filter.")
            return

        if node_id_str: 
            try:
                node_id_val = int(node_id_str)
                if not (0 <= node_id_val <= 15):
                    QMessageBox.warning(self, "Invalid Node ID", "Node ID must be between 0 and 15.")
                    return 
            except ValueError:
                QMessageBox.warning(self, "Invalid Input", "Node ID must be a numeric value.")
                return

        if msg_id_str: 
            try:
                msg_id_val = int(msg_id_str)
                if not (0 <= msg_id_val <= 255):
                    QMessageBox.warning(self, "Invalid MSG ID", "MSG ID must be between 0 and 255.")
                    return 
            except ValueError:
                QMessageBox.warning(self, "Invalid Input", "MSG ID must be a numeric value.")
                return

        # Aynı filtrenin listede zaten var olup olmadığını kontrol etme
        for existing_widget in self.active_filters:
            if existing_widget.node_id == node_id_str and existing_widget.msg_id == msg_id_str:
                QMessageBox.information(self, "Duplicate Filter", "This filter has already been added to the list.")
                return

        # Geçmiş listelerini (Autocomplete) güncelle
        if node_id_str: self.update_history(node_id_str, self.node_history, self.node_model)
        if msg_id_str: self.update_history(msg_id_str, self.msg_history, self.msg_model)

        # Listeye (QListWidget) özel widget olarak filtre satırını ekleme
        item = QListWidgetItem(self.filter_list_widget)
        filter_widget = FilterWidget(node_id_str, msg_id_str, self.on_filter_changed, self.remove_single_filter, self)
        item.setSizeHint(filter_widget.sizeHint())
        
        self.filter_list_widget.addItem(item)
        self.filter_list_widget.setItemWidget(item, filter_widget)
        
        # Filtreyi listemize kaydetme
        self.active_filters.append(filter_widget)

        # Terminale bilgi yazdırma
        info = f"Added Filter -> Node: '{node_id_str or 'Any'}', MSG: '{msg_id_str or 'Any'}'"
        self.ui.plainTextEdit.appendPlainText(f"--- {info} ---")

        # Giriş kutularını temizleme
        self.ui.le_node_id.clear()
        self.ui.le_msg_id.clear()

    def on_filter_changed(self):
        """Herhangi bir filtrenin aktif/pasif durumu değiştiğinde tetiklenir."""
        self.ui.plainTextEdit.appendPlainText("--- Filter States Updated ---")

    def remove_single_filter(self, filter_widget):
        """Satırdaki 'X' butonuna basıldığında o filtreyi listeden siler"""
        for i in range(self.filter_list_widget.count()):
            item = self.filter_list_widget.item(i)
            widget = self.filter_list_widget.itemWidget(item)
            if widget == filter_widget:
                self.filter_list_widget.takeItem(i)
                self.active_filters.remove(filter_widget)
                self.ui.plainTextEdit.appendPlainText(f"--- Removed Filter: Node: {widget.node_id or 'Any'} | MSG: {widget.msg_id or 'Any'} ---")
                break

    def clear_filters(self):
        """Clear Filters butonuna basıldığında sağdaki listenin tamamını temizler"""
        self.filter_list_widget.clear()
        self.active_filters.clear()
        self.ui.le_node_id.clear()
        self.ui.le_msg_id.clear()
        self.ui.plainTextEdit.appendPlainText("--- All Filters Cleared ---")

    def toggle_connection(self):
        if self.serial_port.isOpen():
            self.serial_port.close()
            self.ui.start_stop.setText("Start")
            self.ui.plainTextEdit.appendPlainText("=== Connection Closed ===")
        else:
            if self.ui.cb_port.currentIndex() == 0 or self.ui.cb_baud.currentIndex() == 0:
                QMessageBox.warning(self, "Warning", "Select a valid port and baud rate")
                return

            port_name = self.ui.cb_port.currentText()
            baud_rate = int(self.ui.cb_baud.currentText())
            
            self.serial_port.setPortName(port_name)
            self.serial_port.setBaudRate(baud_rate)
            
            if self.serial_port.open(QSerialPort.ReadWrite):
                self.ui.start_stop.setText("Stop")
                self.ui.plainTextEdit.appendPlainText(f"=== {port_name} Connection Started ===")
                self.data_buffer = ""
            else:
                QMessageBox.critical(self, "Error", f"Could not open {port_name}. It might be in use.")

    def read_serial_data(self):
        raw_data = self.serial_port.readAll().data().decode('utf-8', errors='ignore')
        self.data_buffer += raw_data

        while '\n' in self.data_buffer:
            line, self.data_buffer = self.data_buffer.split('\n', 1)
            self.parse_and_display(line)

    def parse_and_display(self, line):
        clean = line.replace('\0', '').strip()
        
        if not clean:
            return
        
        parts = [p.strip() for p in clean.split(',')]
        length = len(parts)

        if length < 3:
            return
        
        if(parts[0] != "iy" or parts[-1] != "ky"):
            return
            
        current_node_id = parts[1].strip()
        current_msg_id = parts[2].strip()

        # --- ÇOKLU VARYASYONLU FİLTRE MANTIĞI ---
        # Eğer aktif filtreler listesinde eleman varsa eşleşme kontrolü yapılır.
        # Eleman yoksa (filtre uygulanmadıysa) tüm veriler terminale akar.
        if self.active_filters:
            match_found = False
            has_enabled_filter = False

            for f in self.active_filters:
                if not f.is_active:
                    continue  # Pasif (görünürlüğü kapatılmış) filtreleri es geç
                
                has_enabled_filter = True
                
                # Filtre koşullarının değerlendirilmesi (OR mantığı)
                node_match = (f.node_id == current_node_id) if f.node_id else True
                msg_match = (f.msg_id == current_msg_id) if f.msg_id else True
                
                if node_match and msg_match:
                    match_found = True
                    break # Bir eşleşme bulmamız bu mesajı yazdırmak için yeterli
            
            # Eğer en az bir aktif filtre varsa ve gelen veri hiçbirine uymuyorsa fonksiyonu bitir (Ekrana yazma)
            if has_enabled_filter and not match_found:
                return
        # ----------------------------------------

        doesDataExist = length >= 5

        if doesDataExist:
            data_str = ", ".join(parts[3:-1])
            data_status = f"DATA: {data_str}"
        else:
            data_status = "NO DATA"

        out = f"[{datetime.now().strftime('%H:%M:%S:%f')[:-3]}] NODE ID: {current_node_id:<2} MSG ID: {current_msg_id:<3} {data_status}"
        self.ui.plainTextEdit.appendPlainText(out)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TerminalApp()
    window.show()
    sys.exit(app.exec())
