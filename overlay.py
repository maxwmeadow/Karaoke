from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel
from PyQt6.QtGui import QFont, QColor

app = None
label = None

#Create the lyric overlay based on the current lyric being given
def create_overlay(current_lyric):
    global app, label

    if app is None:
        app = QApplication([])

    if label is None:
        label = QLabel("Starting...")
        label.setWindowTitle("Karaoke")

        label.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
        label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        label.setGeometry(100, 100, 1920, 200)

        font = QFont("Arial", 24, QFont.Weight.Bold)
        label.setFont(font)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("""background-color: rgba(0, 0, 0, 180);
            color: white;
            border: 2px solid white;
            border-radius: 15px;
            padding: 20px;
            """)

        label.show()

    if current_lyric and len(current_lyric) >= 3:
        current_word = current_lyric[1]
        full_line = current_lyric[2]

        highlighted = []
        for word in full_line.split():
            if word == current_word:
                highlighted.append(f"<span style='color: yellow;'>{word}</span>")
            else:
                highlighted.append(word)

        lyric_text = " ".join(highlighted)
        label.setText(lyric_text)

    else:
        label.setText("No lyrics available")

    app.processEvents()