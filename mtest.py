from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        # 创建QLabel
        self.label = QLabel("This is a label")
        # 创建QPushButton
        self.button = QPushButton("Click me")

        # 创建一个垂直布局
        layout = QVBoxLayout()

        # 将QLabel和QPushButton添加到布局中
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        # 设置窗口的布局
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication([])
    widget = MyWidget()
    widget.show()
    app.exec_()
