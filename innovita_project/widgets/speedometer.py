import os
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QBrush, QFontDatabase
from PySide6.QtCore import Qt, QRectF, QPointF

def load_digital_font():
    font_paths = ["digital-7.tff", "digital-7.ttf"]
    for path in font_paths:
        if os.path.exists(path):
            font_id = QFontDatabase.addApplicationFont(path)
            if font_id != -1:
                families = QFontDatabase.applicationFontFamilies(font_id)
                if families:
                    return families[0]
    return "Consolas"

class ProfessionalSpeedometer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(180, 180)  
        self.setMaximumSize(240, 240)
        self.current_value = 0.0  
        self.min_value = 0
        self.max_value = 50 
        self.digital_font_family = load_digital_font()

    def set_value(self, value):
        self.current_value = max(float(self.min_value), min(float(value), float(self.max_value)))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        width = self.width()
        height = self.height()
        size = min(width, height) - 40
        cx = width / 2
        cy = height / 2
        radius = size / 2

        rect_x = cx - radius
        rect_y = cy - radius
        arc_rect = QRectF(rect_x, rect_y, size, size)
        arc_start = 225 

        # 1. DIŞ METALİK ÇERÇEVE
        painter.save()
        frame_pen = QPen(QColor(80, 85, 90), 2)
        painter.setPen(frame_pen)
        painter.drawEllipse(arc_rect)
        painter.restore()

        # 2. ARKA PLAN SABİT KADRAN YAYI
        base_pen = QPen(QColor(45, 48, 50), 6, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        painter.setPen(base_pen)
        painter.drawArc(int(rect_x), int(rect_y), int(size), int(size), arc_start * 16, -270 * 16)

        # 3. DİNAMİK HIZ RENKLENDİRMESİ
        current_span = -((self.current_value / self.max_value) * 270)
        
        if self.current_value > 0:
            if self.current_value <= 30:
                active_pen = QPen(QColor(220, 225, 230), 6, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
                painter.setPen(active_pen)
                painter.drawArc(arc_rect, arc_start * 16, int(current_span * 16))
            else:
                active_pen = QPen(QColor(220, 225, 230), 6, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
                painter.setPen(active_pen)
                silver_span = -((30 / self.max_value) * 270)
                painter.drawArc(arc_rect, arc_start * 16, int(silver_span * 16))
                
                factor = (self.current_value - 30) / (50 - 30)
                r = int(211 + (192 - 211) * factor)
                g = int(84 + (41 - 84) * factor)
                b = int(0 + (43 - 0) * factor)
                
                high_pen = QPen(QColor(r, g, b), 6, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
                painter.setPen(high_pen)
                start_angle_30 = arc_start + silver_span 
                span_remaining = current_span - silver_span
                painter.drawArc(arc_rect, int(start_angle_30 * 16), int(span_remaining * 16))

        # 4. ÇENTİKLER VE RAKAMLAR
        painter.save() 
        font = QFont("Segoe UI", 11, QFont.Weight.Bold)
        painter.setFont(font)
        start_rot = 135 
        
        # Ara Çentikler
        sub_ticks = 50 
        for s in range(sub_ticks + 1):
            rot_angle = start_rot + (s / sub_ticks) * 270
            painter.save()
            painter.translate(cx, cy)
            painter.rotate(rot_angle)
            painter.setPen(QPen(QColor(140, 145, 150), 1))
            painter.drawLine(int(radius - 15), 0, int(radius - 8), 0)
            painter.restore()

        # Ana Çentikler
        num_main_ticks = 5
        for i in range(num_main_ticks + 1):
            speed_val = i * 10
            rot_angle = start_rot + (speed_val / self.max_value) * 270
            
            painter.save()
            painter.translate(cx, cy)
            painter.rotate(rot_angle)
            painter.setPen(QPen(QColor(240, 240, 240), 2))
            painter.drawLine(int(radius - 20), 0, int(radius - 8), 0)
            
            painter.translate(radius - 35, 0)
            painter.rotate(-rot_angle)
            painter.setPen(QColor(240, 240, 240))
            painter.drawText(QRectF(-20, -15, 40, 30), Qt.AlignmentFlag.AlignCenter, f"{speed_val}")
            painter.restore()
            
        painter.restore()

        # 5. MAVİ İBRE
        val_ratio = self.current_value / self.max_value
        needle_angle = 135 + (val_ratio * 270)

        painter.save()
        painter.translate(cx, cy)
        painter.rotate(needle_angle) 
        
        blue_color = QColor(0, 130, 255)
        needle_pen = QPen(blue_color, 3, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        painter.setPen(needle_pen)
        painter.drawLine(0, 0, int(radius - 22), 0)

        painter.setBrush(QBrush(blue_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPointF(0, 0), 6, 6)
        painter.restore()

        # 6. DİJİTAL MERKEZ DEĞERLERİ
        if self.current_value <= 30:
            digi_color = QColor(235, 235, 235)
        else:
            factor = (self.current_value - 30) / (50 - 30)
            r = int(211 + (192 - 211) * factor)
            g = int(84 + (41 - 84) * factor)
            b = int(0 + (43 - 0) * factor)
            digi_color = QColor(r, g, b)

        painter.setPen(digi_color)
        painter.setFont(QFont(self.digital_font_family, 20, QFont.Weight.Bold))
        painter.drawText(int(cx - 50), int(cy + 10), 100, 40, Qt.AlignmentFlag.AlignCenter, f"{int(self.current_value)}")
        
        painter.setPen(QColor(150, 155, 160))
        sub_font = QFont(self.digital_font_family, 16, QFont.Weight.Normal)
        painter.setFont(sub_font)