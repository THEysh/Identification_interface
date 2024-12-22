from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import QTimer, QDateTime
from qfluentwidgets import PushButton
from qfluentwidgets import FluentIcon as FIF

class ClockShow(PushButton):
    def __init__(self, parent:QFrame):
        super().__init__(parent)
        self.setIcon(FIF.TILES)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # 每秒更新一次
        self.update_time()

    def update_time(self):
        current_datetime = QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss')
        self.setText(current_datetime)


