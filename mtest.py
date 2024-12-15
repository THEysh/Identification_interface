from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QLabel
from PyQt5.QtCore import Qt, QEvent
import sys

class RangeSlider(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slider = QSlider(Qt.Horizontal)
        self.label = QLabel()
        self.slider.valueChanged.connect(self.update_label)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self.slider)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def update_label(self, value):
        self.label.setText(str(value))

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = RangeSlider()
    window.show()

    sys.exit(app.exec_())
