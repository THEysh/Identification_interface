import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Button Click Example")

        # 初始化按钮
        self.loadModBtn = QPushButton("Load Module", self)

        # 设置布局
        layout = QVBoxLayout(self)
        layout.addWidget(self.loadModBtn)

        # 连接按钮点击事件
        # 使用 lambda 传递额外参数
        self.loadModBtn.clicked.connect(lambda: self.on_button_click("Hello, world!"))

    def on_button_click(self, message):
        # 在按钮点击时调用
        print(f"Button clicked! Message: {message}")


# 启动应用
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
