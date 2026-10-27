
import sys
import re
# pyrefly: ignore[missing-import]
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty, QPointF
# pyrefly: ignore[missing-import]
from PyQt6.QtGui import QFont, QColor, QPainter, QPainterPath, QPen, QBrush
# pyrefly: ignore[missing-import]
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTextEdit, QPushButton, QFrame, QProgressBar, QGraphicsDropShadowEffect
)
# pyrefly: ignore[missing-import]
import nltk
# pyrefly: ignore[missing-import]
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download VADER lexicon quietly
nltk.download('vader_lexicon', quiet=True)

# Curated Professional Theme System
FACE_CONFIGS = {
    "Joy": {
        "face_color": "#FFC107",
        "mouth_curve": 38.0,
        "eye_type": "open",
        "brow_angle": 0.0,
        "teardrop": False,
        "bg_gradient": "qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #FFFDE7, stop:1 #FFF59D);",
        "card_bg": "#FFFFFF",
        "text_color": "#3E2723",
        "accent_color": "#FFA000",
        "subtext_color": "#795548",
        "message": "Your radiant energy is contagious today. Keep sharing that warmth.",
        "action": "Spread Good Energy"
    },
    "Calm": {
        "face_color": "#4DB6AC",
        "mouth_curve": 8.0,
        "eye_type": "closed",
        "brow_angle": 0.0,
        "teardrop": False,
        "bg_gradient": "qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #E0F2F1, stop:1 #B2DFDB);",
        "card_bg": "#FFFFFF",
        "text_color": "#004D40",
        "accent_color": "#00897B",
        "subtext_color": "#00695C",
        "message": "A peaceful mind cultivates clarity. Take a steady, deep breath.",
        "action": "Begin Mindful Breathing"
    },
    "Sadness": {
        "face_color": "#64B5F6",
        "mouth_curve": -32.0,
        "eye_type": "open",
        "brow_angle": -12.0,
        "teardrop": True,
        "bg_gradient": "qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #E3F2FD, stop:1 #BBDEFB);",
        "card_bg": "#FFFFFF",
        "text_color": "#0D47A1",
        "accent_color": "#1E88E5",
        "subtext_color": "#1565C0",
        "message": "It is okay to pause and process your feelings. Honor your pace.",
        "action": "Enter Calm Space"
    },
    "Anger": {
        "face_color": "#E57373",
        "mouth_curve": -18.0,
        "eye_type": "open",
        "brow_angle": 22.0,
        "teardrop": False,
        "bg_gradient": "qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #FFEBEE, stop:1 #FFCDD2);",
        "card_bg": "#FFFFFF",
        "text_color": "#B71C1C",
        "accent_color": "#E53935",
        "subtext_color": "#C62828",
        "message": "Acknowledge the frustration, then let off steam in a safe way.",
        "action": "Decompress Now"
    },
    "Focus": {
        "face_color": "#7986CB",
        "mouth_curve": 4.0,
        "eye_type": "focused",
        "brow_angle": 4.0,
        "teardrop": False,
        "bg_gradient": "qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #E8EAF6, stop:1 #C5CAE9);",
        "card_bg": "#FFFFFF",
        "text_color": "#1A237E",
        "accent_color": "#3F51B5",
        "subtext_color": "#283593",
        "message": "Sharp vision and clear purpose. Dive in and eliminate distractions.",
        "action": "Start Focus Session"
    }
}


class EmotionFaceWidget(QWidget):
    """Custom Vector Canvas Avatar with Smooth Interpolation."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(150, 150)

        self._mouth_curve = FACE_CONFIGS["Calm"]["mouth_curve"]
        self._brow_angle = FACE_CONFIGS["Calm"]["brow_angle"]
        self.face_color = QColor(FACE_CONFIGS["Calm"]["face_color"])
        self.eye_type = FACE_CONFIGS["Calm"]["eye_type"]
        self.show_teardrop = FACE_CONFIGS["Calm"]["teardrop"]

    def get_mouth_curve(self): return self._mouth_curve
    def set_mouth_curve(self, val):
        self._mouth_curve = val
        self.update()
    mouth_curve = pyqtProperty(float, get_mouth_curve, set_mouth_curve)

    def get_brow_angle(self): return self._brow_angle
    def set_brow_angle(self, val):
        self._brow_angle = val
        self.update()
    brow_angle = pyqtProperty(float, get_brow_angle, set_brow_angle)

    def transition_to_emotion(self, emotion_key):
        config = FACE_CONFIGS[emotion_key]

        self.anim_mouth = QPropertyAnimation(self, b"mouth_curve")
        self.anim_mouth.setDuration(450)
        self.anim_mouth.setStartValue(self._mouth_curve)
        self.anim_mouth.setEndValue(config["mouth_curve"])
        self.anim_mouth.setEasingCurve(QEasingCurve.Type.OutCubic)

        self.anim_brow = QPropertyAnimation(self, b"brow_angle")
        self.anim_brow.setDuration(450)
        self.anim_brow.setStartValue(self._brow_angle)
        self.anim_brow.setEndValue(config["brow_angle"])
        self.anim_brow.setEasingCurve(QEasingCurve.Type.OutCubic)

        self.face_color = QColor(config["face_color"])
        self.eye_type = config["eye_type"]
        self.show_teardrop = config["teardrop"]

        self.anim_mouth.start()
        self.anim_brow.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        center_x, center_y = self.width() / 2, self.height() / 2
        radius = 65.0

        # Base Face Circle
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(self.face_color))
        painter.drawEllipse(QPointF(center_x, center_y), radius, radius)

        feature_pen = QPen(QColor("#1A1A1A"), 4, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        painter.setPen(feature_pen)

        left_eye_center = QPointF(center_x - 22, center_y - 14)
        right_eye_center = QPointF(center_x + 22, center_y - 14)

        if self.eye_type == "open":
            painter.setBrush(QBrush(QColor("#1A1A1A")))
            painter.drawEllipse(left_eye_center, 6, 9)
            painter.drawEllipse(right_eye_center, 6, 9)
        elif self.eye_type == "closed":
            path_left = QPainterPath(left_eye_center + QPointF(-7, 0))
            path_left.quadTo(left_eye_center + QPointF(0, 7), left_eye_center + QPointF(7, 0))
            path_right = QPainterPath(right_eye_center + QPointF(-7, 0))
            path_right.quadTo(right_eye_center + QPointF(0, 7), right_eye_center + QPointF(7, 0))
            painter.drawPath(path_left)
            painter.drawPath(path_right)
        elif self.eye_type == "focused":
            painter.setBrush(QBrush(QColor("#1A1A1A")))
            painter.drawEllipse(left_eye_center, 4, 4)
            painter.drawEllipse(right_eye_center, 4, 4)

        brow_pen = QPen(QColor("#1A1A1A"), 3, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        painter.setPen(brow_pen)

        p1_l = QPointF(center_x - 30, center_y - 28 - self._brow_angle)
        p2_l = QPointF(center_x - 12, center_y - 28 + self._brow_angle)
        painter.drawLine(p1_l, p2_l)

        p1_r = QPointF(center_x + 12, center_y - 28 + self._brow_angle)
        p2_r = QPointF(center_x + 30, center_y - 28 - self._brow_angle)
        painter.drawLine(p1_r, p2_r)

        mouth_pen = QPen(QColor("#1A1A1A"), 4, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        painter.setPen(mouth_pen)
        mouth_path = QPainterPath(QPointF(center_x - 26, center_y + 22))
        control_point = QPointF(center_x, center_y + 22 + self._mouth_curve)
        mouth_path.quadTo(control_point, QPointF(center_x + 26, center_y + 22))
        painter.drawPath(mouth_path)

        if self.show_teardrop:
            tear_pen = QPen(Qt.PenStyle.NoPen)
            painter.setPen(tear_pen)
            painter.setBrush(QBrush(QColor("#29B6F6")))
            tear_path = QPainterPath(QPointF(center_x - 20, center_y - 2))
            tear_path.quadTo(QPointF(center_x - 24, center_y + 10), QPointF(center_x - 20, center_y + 14))
            tear_path.quadTo(QPointF(center_x - 16, center_y + 10), QPointF(center_x - 20, center_y - 2))
            painter.drawPath(tear_path)


class EmotionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Atmosphere Mood Studio")
        self.resize(820, 680)

        self.sia = SentimentIntensityAnalyzer()
        self.current_theme = "Calm"

        self.init_ui()
        self.apply_theme("Calm")

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(32, 32, 32, 32)
        self.main_layout.setSpacing(20)

        # Header Frame
        self.header_card = QFrame()
        header_layout = QVBoxLayout(self.header_card)
        header_layout.setContentsMargins(24, 24, 24, 24)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.face_avatar = EmotionFaceWidget()

        self.title_label = QLabel("Feeling Calm")
        self.title_label.setFont(QFont("Segoe UI", 20, QFont.Weight.DemiBold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.adaptive_msg = QLabel(FACE_CONFIGS["Calm"]["message"])
        self.adaptive_msg.setFont(QFont("Segoe UI", 11))
        self.adaptive_msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.adaptive_msg.setWordWrap(True)

        header_layout.addWidget(self.face_avatar, alignment=Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(self.title_label)
        header_layout.addWidget(self.adaptive_msg)

        shadow_header = QGraphicsDropShadowEffect()
        shadow_header.setBlurRadius(25)
        shadow_header.setColor(QColor(0, 0, 0, 15))
        shadow_header.setYOffset(6)
        self.header_card.setGraphicsEffect(shadow_header)

        # Clean Pill Selector Bar
        emoji_bar_layout = QHBoxLayout()
        emoji_bar_layout.setSpacing(12)
        
        mood_pill_data = [
            ("Happy", "Joy"),
            ("Calm", "Calm"),
            ("Sad", "Sadness"),
            ("Angry", "Anger"),
            ("Focus", "Focus")
        ]

        self.pill_buttons = {}
        for label, emotion in mood_pill_data:
            btn = QPushButton(label)
            btn.setFont(QFont("Segoe UI", 10, QFont.Weight.Medium))
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _, e=emotion: self.apply_theme(e))
            emoji_bar_layout.addWidget(btn)
            self.pill_buttons[emotion] = btn

        # Modern Text Input Area
        self.input_card = QFrame()
        input_layout = QVBoxLayout(self.input_card)
        input_layout.setContentsMargins(20, 20, 20, 20)

        input_title = QLabel("How is your day going?")
        input_title.setFont(QFont("Segoe UI", 11, QFont.Weight.DemiBold))

        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Type a thought, paste emojis, or reflect on your mood...")
        self.text_input.setFont(QFont("Segoe UI", 11))
        self.text_input.setFixedHeight(95)
        self.text_input.textChanged.connect(self.analyze_text_sentiment)

        input_layout.addWidget(input_title)
        input_layout.addWidget(self.text_input)

        shadow_input = QGraphicsDropShadowEffect()
        shadow_input.setBlurRadius(25)
        shadow_input.setColor(QColor(0, 0, 0, 12))
        shadow_input.setYOffset(6)
        self.input_card.setGraphicsEffect(shadow_input)

        # Footer Actions & Metrics
        self.footer_layout = QHBoxLayout()
        self.footer_layout.setSpacing(16)

        self.meter_card = QFrame()
        meter_layout = QVBoxLayout(self.meter_card)
        meter_layout.setContentsMargins(18, 16, 18, 16)

        meter_title = QLabel("Mood Intensity Metric")
        meter_title.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))

        self.polarity_bar = QProgressBar()
        self.polarity_bar.setRange(-100, 100)
        self.polarity_bar.setValue(0)
        self.polarity_bar.setTextVisible(False)
        self.polarity_bar.setFixedHeight(8)

        self.polarity_label = QLabel("Balanced State (0.00)")
        self.polarity_label.setFont(QFont("Segoe UI", 9))

        meter_layout.addWidget(meter_title)
        meter_layout.addWidget(self.polarity_bar)
        meter_layout.addWidget(self.polarity_label)

        shadow_meter = QGraphicsDropShadowEffect()
        shadow_meter.setBlurRadius(20)
        shadow_meter.setColor(QColor(0, 0, 0, 10))
        shadow_meter.setYOffset(4)
        self.meter_card.setGraphicsEffect(shadow_meter)

        self.action_btn = QPushButton(FACE_CONFIGS["Calm"]["action"])
        self.action_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.action_btn.setFixedHeight(62)
        self.action_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        shadow_action = QGraphicsDropShadowEffect()
        shadow_action.setBlurRadius(20)
        shadow_action.setColor(QColor(0, 0, 0, 15))
        shadow_action.setYOffset(5)
        self.action_btn.setGraphicsEffect(shadow_action)

        self.footer_layout.addWidget(self.meter_card, stretch=2)
        self.footer_layout.addWidget(self.action_btn, stretch=1)

        self.main_layout.addWidget(self.header_card)
        self.main_layout.addLayout(emoji_bar_layout)
        self.main_layout.addWidget(self.input_card)
        self.main_layout.addLayout(self.footer_layout)

    # def analyze_text_sentiment(self):
    #     text = self.text_input.toPlainText().strip()
    #     if not text:
    #         self.polarity_bar.setValue(0)
    #         self.polarity_label.setText("Balanced State (0.00)")
    #         return

    #     # Direct Emoji Detection Overrides
    #     if any(e in text for e in ["😊", "🎉", "🥳", "✨", "😃", "😁"]):
    #         self.apply_theme("Joy")
    #         return
    #     elif any(e in text for e in ["😭", "💔", "🌧️", "😢", "😔", "☹️"]):
    #         self.apply_theme("Sadness")
    #         return
    #     elif any(e in text for e in ["🤬", "😡", "🔥", "👿", "💢"]):
    #         self.apply_theme("Anger")
    #         return
    #     elif any(e in text for e in ["🚀", "🧠", "💻", "⚡"]):
    #         self.apply_theme("Focus")
    #         return

    #     scores = self.sia.polarity_scores(text)
    #     compound = scores['compound']

    #     self.polarity_bar.setValue(int(compound * 100))
    #     self.polarity_label.setText(f"Sentiment Index: {compound:.2f}")

    #     text_lower = text.lower()
        
    #     sad_indicators = ["lonely", "disappointed", "sad", "unhappy", "cry", "crying", "depressed", "hurt", "miss", "sorry", "hopeless", "grief", "gloomy", "fail", "lost"]
    #     angry_indicators = ["angry", "hate", "furious", "mad", "annoyed", "terrible", "worst", "rage", "frustrated", "idiot", "stupid", "disrespect"]
    #     focus_indicators = ["study", "analyze", "data", "code", "report", "project", "work", "focus", "exam", "deadline", "prepare"]

    #     sad_score = sum(1 for w in sad_indicators if re.search(r'\b' + w + r'\b', text_lower))
    #     angry_score = sum(1 for w in angry_indicators if re.search(r'\b' + w + r'\b', text_lower))
    #     focus_score = sum(1 for w in focus_indicators if re.search(r'\b' + w + r'\b', text_lower))

    #     if compound >= 0.35:
    #         detected = "Joy"
    #     elif compound <= -0.1:
    #         if sad_score > angry_score:
    #             detected = "Sadness"
    #         elif angry_score > sad_score:
    #             detected = "Anger"
    #         elif compound <= -0.5:
    #             detected = "Anger"
    #         else:
    #             detected = "Sadness"
    #     elif focus_score > 0 or (0.05 <= compound < 0.35):
    #         detected = "Focus"
    #     else:
    #         detected = "Calm"

    #     if detected != self.current_theme:
    #         self.apply_theme(detected)

    def analyze_text_sentiment(self):
        text = self.text_input.toPlainText().strip()
        if not text:
            self.polarity_bar.setValue(0)
            self.polarity_label.setText("Balanced State (0.00)")
            return

        # Direct Emoji Detection Overrides
        if any(e in text for e in ["😊", "🎉", "🥳", "✨", "😃", "😁"]):
            self.apply_theme("Joy")
            return
        elif any(e in text for e in ["🌿", "🧘‍♂️", "☕", "🍃", "🌊", "🌾"]):
            self.apply_theme("Calm")
            return
        elif any(e in text for e in ["😭", "💔", "🌧️", "😢", "😔", "☹️"]):
            self.apply_theme("Sadness")
            return
        elif any(e in text for e in ["🤬", "😡", "🔥", "👿", "💢"]):
            self.apply_theme("Anger")
            return
        elif any(e in text for e in ["🚀", "🧠", "💻", "⚡"]):
            self.apply_theme("Focus")
            return

        scores = self.sia.polarity_scores(text)
        compound = scores['compound']

        self.polarity_bar.setValue(int(compound * 100))
        self.polarity_label.setText(f"Sentiment Index: {compound:.2f}")

        text_lower = text.lower()
        
        calm_indicators = ["calm", "peaceful", "relax", "relaxing", "rest", "resting", "quiet", "tranquil", "serene", "chill"]
        sad_indicators = ["lonely", "disappointed", "sad", "unhappy", "cry", "crying", "depressed", "hurt", "miss", "sorry", "hopeless", "grief", "gloomy", "fail", "lost"]
        angry_indicators = ["angry", "hate", "furious", "mad", "annoyed", "terrible", "worst", "rage", "frustrated", "idiot", "stupid", "disrespect"]
        focus_indicators = ["study", "analyze", "data", "code", "report", "project", "work", "focus", "exam", "deadline", "prepare"]

        calm_score = sum(1 for w in calm_indicators if re.search(r'\b' + w + r'\b', text_lower))
        sad_score = sum(1 for w in sad_indicators if re.search(r'\b' + w + r'\b', text_lower))
        angry_score = sum(1 for w in angry_indicators if re.search(r'\b' + w + r'\b', text_lower))
        focus_score = sum(1 for w in focus_indicators if re.search(r'\b' + w + r'\b', text_lower))

        # Decision Tree Priority Logic
        if calm_score > 0 and sad_score == 0 and angry_score == 0:
            detected = "Calm"
        elif compound >= 0.35:
            detected = "Joy"
        elif compound <= -0.1:
            if sad_score > angry_score:
                detected = "Sadness"
            elif angry_score > sad_score:
                detected = "Anger"
            elif compound <= -0.5:
                detected = "Anger"
            else:
                detected = "Sadness"
        elif focus_score > 0:
            detected = "Focus"
        else:
            detected = "Calm"

        if detected != self.current_theme:
            self.apply_theme(detected)

    def apply_theme(self, emotion_name):
        self.current_theme = emotion_name
        config = FACE_CONFIGS[emotion_name]

        self.face_avatar.transition_to_emotion(emotion_name)

        self.title_label.setText(f"Feeling {emotion_name}")
        self.adaptive_msg.setText(config["message"])
        self.action_btn.setText(config["action"])

        style_sheet = f"""
            QMainWindow {{
                background: {config["bg_gradient"]};
            }}
            QFrame {{
                background-color: {config["card_bg"]};
                border-radius: 20px;
                border: none;
            }}
            QLabel {{
                color: {config["text_color"]};
                background: transparent;
            }}
            QTextEdit {{
                background-color: #F8F9FA;
                border: 1.5px solid #E9ECEF;
                border-radius: 12px;
                padding: 12px;
                color: #212529;
            }}
            QTextEdit:focus {{
                border: 1.5px solid {config["accent_color"]};
                background-color: #FFFFFF;
            }}
            QPushButton {{
                background-color: {config["card_bg"]};
                color: {config["text_color"]};
                border-radius: 12px;
                padding: 10px 18px;
                border: 1px solid rgba(0, 0, 0, 0.08);
            }}
            QPushButton:hover {{
                background-color: {config["accent_color"]};
                color: white;
            }}
            QProgressBar {{
                border: none;
                border-radius: 4px;
                background-color: #E9ECEF;
            }}
            QProgressBar::chunk {{
                background-color: {config["accent_color"]};
                border-radius: 4px;
            }}
        """
        self.setStyleSheet(style_sheet)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EmotionApp()
    window.show()
    sys.exit(app.exec())