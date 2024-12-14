import sys
from PyQt5.QtWidgets import QVBoxLayout, QFrame, QPushButton, QApplication
from PyQt5.QtCore import QTimer, QDateTime
from qfluentwidgets import PushButton


class ClockShow(PushButton):
    def __init__(self, frame: QFrame, layout: QVBoxLayout):
        super().__init__("Current Time", frame)
        layout.addWidget(self)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # 每秒更新一次

        self.update_time()

    def update_time(self):
        current_datetime = QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss')
        self.setText(current_datetime)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = QFrame()
    layout = QVBoxLayout()

    # 添加一个伸展部件，使按钮固定在最下方
    layout.addStretch()

    clock = ClockShow(frame, layout)

    frame.setLayout(layout)
    frame.show()

    sys.exit(app.exec_())
