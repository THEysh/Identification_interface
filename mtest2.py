import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QPushButton
from qfluentwidgets import PushButton

from assembly.AdaptiveImageLabel import AdaptiveImageLabel


class LabelBtn(QFrame):
    def __init__(self, index: int, key='org', parent=None):
        super().__init__(parent)
        _layout = QVBoxLayout()
        self.Label = AdaptiveImageLabel(index, key)
        self.Label.setCustomImage("resource/painting_girl.png")
        self.button = PushButton("点击我", self)
        _layout.addWidget(self.Label)
        _layout.addWidget(self.button)
        self.setLayout(_layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LabelBtn 示例")
        self.setGeometry(100, 100, 400, 300)
        # 创建一个中心 widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        # 创建一个垂直布局来管理多个 LabelBtn 实例
        _vlayout = QVBoxLayout(central_widget)

        # 创建多个 LabelBtn 实例并添加到布局中
        for i in range(1):
            label_btn = LabelBtn(i, key='示例')
            _vlayout.addWidget(label_btn)
        # 设置布局
        central_widget.setLayout(_vlayout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
