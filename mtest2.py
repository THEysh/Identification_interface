import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QScrollArea, QGridLayout, QLabel
from PyQt5.QtCore import Qt
from qfluentwidgets import FlowLayout


# 引入你的 FlowLayout 类


class MyScrollArea(QScrollArea):
    def __init__(self):
        super().__init__()
        self.initUI()
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.on_resize()
    def on_resize(self):
        current_size = self.size()
        print(f"ScrollArea resized to: {current_size.width()} x {current_size.height()}")

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建一个外层布局来管理 QScrollArea
        main_layout = QVBoxLayout(self)

        self.scroll_area = MyScrollArea()
        main_layout.addWidget(self.scroll_area)

        self.setLayout(main_layout)
        self.setGeometry(100, 100, 400, 300)  # 设置窗口大小

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()

    sys.exit(app.exec_())
