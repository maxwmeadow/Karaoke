from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtGui import QIcon, QFontDatabase, QFont

def create_overlay(current):
    app = QApplication([])
    window = QMainWindow()

    window.setMinimumSize(500, 200)

    window.setWindowFlags(Qt.WindowType.FramelessWindowHint)
    window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    label = QLabel(f"{current[1]}", alignment=Qt.AlignmentFlag.AlignCenter)
    window.setCentralWidget(label)

    font = window.setFont(QFont("Century Gothic", 18, QFont.Weight.Bold))

    window.show()
    app.exec()