import math
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont
from PySide6.QtCore import Qt

class GaugeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(140, 140) 
        self.setMaximumSize(180, 180)
        self.value = 0.0  

    def set_value(self, value):
        self.value = max(0.0, value)
        self.update()  

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        width, height = self.width(), self.height()
        center_x, center_y = width // 2, height // 2
        radius = min(center_x, center_y) - 15

        current_lap = int(self.value)
        lap_progress = self.value - current_lap

        painter.setPen(QPen(QColor(50, 50, 50), 4))
        painter.setBrush(QColor(15, 15, 15))
        painter.drawEllipse(center_x - radius, center_y - radius, radius * 2, radius * 2)

        painter.setPen(QPen(QColor(120, 120, 120), 1.5))
        for i in range(10):
            angle_deg = (i * 36) - 90
            angle_rad = math.radians(angle_deg)
            p1_x = int(center_x + (radius - 10) * math.cos(angle_rad))
            p1_y = int(center_y + (radius - 10) * math.sin(angle_rad))
            p2_x = int(center_x + radius * math.cos(angle_rad))
            p2_y = int(center_y + radius * math.sin(angle_rad))
            painter.drawLine(p1_x, p1_y, p2_x, p2_y)

        needle_angle_deg = (lap_progress * 360) - 90
        needle_angle_rad = math.radians(needle_angle_deg)
        needle_len = radius - 20
        needle_x = int(center_x + needle_len * math.cos(needle_angle_rad))
        needle_y = int(center_y + needle_len * math.sin(needle_angle_rad))

        painter.setPen(QPen(QColor(255, 60, 60), 3))
        painter.drawLine(center_x, center_y, needle_x, needle_y)
        painter.setBrush(QColor(255, 60, 60))
        painter.drawEllipse(center_x - 6, center_y - 6, 12, 12)

        painter.setPen(QPen(QColor(255, 255, 255)))
        painter.setFont(QFont("Consolas", 18, QFont.Weight.Bold))
        painter.drawText(center_x - 50, center_y - 15, 100, 30, Qt.AlignmentFlag.AlignCenter, f"{current_lap}")
        
        painter.setFont(QFont("Consolas", 11))
        painter.setPen(QPen(QColor(0, 255, 255))) 
        painter.drawText(center_x - 50, center_y + 15, 100, 20, Qt.AlignmentFlag.AlignCenter, f"{self.value:.3f}")