import sys
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel

class MiddleClass(QObject):
    """定义一个包含自定义信号的中间类"""
    my_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def emit_signal(self, message):
        """一个用于手动触发信号的方法"""
        self.my_signal.emit(message)


class ReceiverClass(QObject):
    """定义一个接收信号并处理的类"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.signal_emitter = parent
        self.signal_emitter.my_signal.connect(self.on_my_signal)

    def on_my_signal(self, message):
        """当信号被触发时调用的槽函数"""
        print(f"Received message: {message}")


class MyMainWindow(QMainWindow):
    """定义一个主窗口类，它使用中间类和接收类"""

    def __init__(self):
        super().__init__()

        # 创建信号发射器实例，并将其作为父对象
        self.signal_emitter = MiddleClass()

        # 创建信号接收器实例，传递信号发射器作为父对象
        self.signal_receiver = ReceiverClass(parent=self.signal_emitter)

        # 创建用户界面部分
        self.button = QPushButton("Send Signal", self)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.button)
        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

        self.button.clicked.connect(lambda: self.signal_emitter.emit_signal("Hello, Signal!"))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = MyMainWindow()
    main_window.show()

    sys.exit(app.exec_())
