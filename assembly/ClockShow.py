import sys
from PyQt5.QtWidgets import QVBoxLayout, QFrame, QLayout
from PyQt5.QtCore import QTimer, QDateTime
from qfluentwidgets import PushButton
from qfluentwidgets import FluentIcon as FIF

class ClockShow(PushButton):
    def __init__(self, frame:QFrame, layout:QLayout):
        super().__init__(frame)
        self.setIcon(FIF.TILES)
        layout.addWidget(self)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # 每秒更新一次
        self.update_time()

    def update_time(self):
        current_datetime = QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss')
        self.setText(current_datetime)

