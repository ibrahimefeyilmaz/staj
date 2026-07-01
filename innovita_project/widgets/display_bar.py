from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox
from PySide6.QtCore import QTimer, Qt
import functions

# Kendi yazdığın özel widget'lar (Sınıf ve dosya isimlerinin birebir eşleştiğinden emin ol)
from widgets.gauge import GaugeWidget
from widgets.speedometer import ProfessionalSpeedometer
from widgets.thermometer import VerticalThermometer
from widgets.altitude import VerticalAltitudeBar # Eğer böyle bir dosyan varsa yorumu kaldır

class DisplayBarWidget(QWidget):
    def __init__(self, node_id, msg_id, parent=None):
        super().__init__(parent)
        self.last_data_list = []
        
        self.play_timer = QTimer(self)
        self.queued_values = []
        self.play_timer.timeout.connect(self.play_next_value)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(5)
        
        self.top_row_widget = QWidget(self)
        self.top_row_layout = QHBoxLayout(self.top_row_widget)
        self.top_row_layout.setContentsMargins(5, 0, 5, 0)
        self.top_row_layout.setSpacing(15)
        
        self.setStyleSheet("DisplayBarWidget { background-color: #F5F5F5; border-radius: 6px; border: 1px solid #CCCCCC; }")

        text_parts = []
        if node_id: text_parts.append(f"Node: {node_id}")
        if msg_id: text_parts.append(f"MSG: {msg_id}")
        filter_text = " | ".join(text_parts)

        self.label_info = QLabel(filter_text, self)
        self.label_info.setStyleSheet("font-weight: bold; color: #0288D1;") 
        self.label_info.setFixedWidth(130)
        self.top_row_layout.addWidget(self.label_info)

        self.dropdown = QComboBox(self)
        self.dropdown.addItem("Show Raw Data") 
        
        for attr_name in dir(functions):
            attr = getattr(functions, attr_name)
            if callable(attr) and not attr_name.startswith("__"):
                self.dropdown.addItem(attr_name)
                
        self.dropdown.setFixedWidth(160)
        self.dropdown.setStyleSheet("background-color: #FFFFFF; color: #333333; border: 1px solid #BBB;")
        self.dropdown.currentIndexChanged.connect(self.refresh_display)
        self.top_row_layout.addWidget(self.dropdown)

        self.label_data = QLabel("Waiting for data...", self)
        self.label_data.setStyleSheet("color: #D32F2F; font-family: 'Consolas', monospace; font-size: 11pt; font-weight: bold;") 
        self.top_row_layout.addWidget(self.label_data, stretch=1)
        
        self.main_layout.addWidget(self.top_row_widget)
        
        # --- WIDGET TANIMLAMALARI ---
        self.gauge = GaugeWidget(self)
        self.gauge.hide() 
        self.main_layout.addWidget(self.gauge, alignment=Qt.AlignmentFlag.AlignCenter)

        self.speedometer = ProfessionalSpeedometer(self)
        self.speedometer.hide()
        self.main_layout.addWidget(self.speedometer, alignment=Qt.AlignmentFlag.AlignCenter)

        self.altimeter = VerticalAltitudeBar(self)
        self.altimeter.hide()
        self.main_layout.addWidget(self.altimeter, alignment=Qt.AlignmentFlag.AlignCenter)

        self.thermometer = VerticalThermometer(self)
        self.thermometer.hide()
        self.main_layout.addWidget(self.thermometer, alignment=Qt.AlignmentFlag.AlignCenter)
        
    def stop_playback(self):
        self.play_timer.stop() 
        self.queued_values.clear() 

    def update_live_data(self, data_list):
        self.last_data_list = data_list
        self.refresh_display()

    def play_next_value(self):
        if self.queued_values:
            val_str = self.queued_values.pop(0)
            try:
                val_float = float(val_str)
                selected_function = self.dropdown.currentText()
                
                # Seçili fonksiyona göre veriyi ilgili widget'a gönder
                if selected_function == "gaugemeter":
                    self.gauge.set_value(val_float / 1000.0) 
                elif selected_function == "speedometer":
                    self.speedometer.set_value(val_float * 0.005)
                elif selected_function == "altitudebar":
                    self.altimeter.set_altitude(val_float)
                elif selected_function == "thermometer":
                    self.thermometer.set_temperature(val_float * 0.005 - 10)

                self.label_data.setText(val_str)
            except (ValueError, TypeError):
                pass
        else:
            self.play_timer.stop()

    def refresh_display(self):
        if not self.last_data_list:
            return

        selected_function = self.dropdown.currentText()

        # HATA BURADAYDI: Timer'ı ve tüm widgetları körü körüne kapatmıyoruz.
        # Sadece aktif olması gereken widget'ı gösterip diğerlerini gizliyoruz.
        if selected_function == "gaugemeter":
            self.gauge.show()
            self.speedometer.hide()
            self.altimeter.hide()
            self.thermometer.hide()
        elif selected_function == "speedometer":
            self.gauge.hide()
            self.speedometer.show()
            self.altimeter.hide()
            self.thermometer.hide()
        elif selected_function == "altitudebar":
            self.gauge.hide()
            self.speedometer.hide()
            self.altimeter.show()
            self.thermometer.hide()
        elif selected_function == "thermometer":
            self.gauge.hide()
            self.speedometer.hide()
            self.altimeter.hide()
            self.thermometer.show()
        else:
            # Sadece geçerli bir fonksiyon seçilmediğinde göstergeleri kapatıp timer'ı durdur
            self.gauge.hide()
            self.speedometer.hide()
            self.altimeter.hide()
            self.thermometer.hide()
            self.play_timer.stop() 

        if selected_function == "Show Raw Data":
            self.label_data.setText(", ".join(self.last_data_list))
        else:
            func = getattr(functions, selected_function, None)
            if func:
                try:
                    meaningful_data = func(self.last_data_list)
                    
                    if selected_function in ["gaugemeter", "speedometer", "altitudebar", "thermometer"]:
                        sub_values = meaningful_data.split('|')
                        self.label_data.setText(", ".join(sub_values))
                        
                        self.queued_values.extend(sub_values)
                        if not self.play_timer.isActive():
                            self.play_timer.start(100) 
                    else:
                        self.label_data.setText(str(meaningful_data))
                            
                except Exception as e:
                    self.label_data.setText(f"Error: {str(e)}")
            else:
                self.label_data.setText(", ".join(self.last_data_list))

    def set_active_state(self, is_active):
        if is_active:
            self.label_info.setStyleSheet("font-weight: bold; color: #0288D1;")
            self.label_data.setStyleSheet("color: #D32F2F; font-family: 'Consolas', monospace; font-size: 11pt; font-weight: bold;")
            self.setStyleSheet("DisplayBarWidget { background-color: #F5F5F5; border-radius: 6px; border: 1px solid #CCCCCC; }")
            
            selected_function = self.dropdown.currentText()
            if selected_function == "gaugemeter": self.gauge.show()
            elif selected_function == "speedometer": self.speedometer.show()
            elif selected_function == "altitudebar": self.altimeter.show()
            elif selected_function == "thermometer": self.thermometer.show()
        else:
            self.label_info.setStyleSheet("color: #9E9E9E; text-decoration: line-through;")
            self.label_data.setStyleSheet("color: #9E9E9E; font-family: 'Consolas', monospace; font-size: 11pt; font-style: italic;")
            self.setStyleSheet("DisplayBarWidget { background-color: #EAEAEA; border-radius: 6px; border: 1px dashed #BBB; }")
            
            self.gauge.hide()
            self.speedometer.hide()
            self.altimeter.hide()
            self.thermometer.hide()
            self.stop_playback()
