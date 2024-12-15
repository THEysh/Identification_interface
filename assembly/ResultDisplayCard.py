from PyQt5.QtWidgets import QFrame, QWidget, QLayout
from qfluentwidgets import TextBrowser, PushButton

from assembly.autoResizePushButton import AutoResizePushButton


class ResultDisplayCard():
    def __init__(self, frame:QFrame):
        self.panel = frame
        self.rList = []
        self.rList.append(PushButton("识别结果 🦄", self.panel))
        self.rList.append(PushButton("置信度 🐴", self.panel))
        self.rList.append(PushButton("识别用时 🦄", self.panel))
        self.rList.append(PushButton("x坐标 🦄", self.panel))
        self.rList.append(PushButton("y坐标 🐴", self.panel))
        self.rList.append(PushButton("宽 🦄", self.panel))
        self.rList.append(PushButton("高 🐴", self.panel))

    def addwidget(self,layout:QLayout):
        for r in self.rList:
            layout.addWidget(r)