import random
import time
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QFrame, QSlider, QHBoxLayout, QVBoxLayout
from qfluentwidgets import Slider, StrongBodyLabel


class DisplayNumericSlider(QFrame):
    def __init__(self, width:int, name:str, parent=None):
        super().__init__(parent)
        _layout = QHBoxLayout()
        self.name = name
        self.slider = Slider(Qt.Horizontal, self)
        self.slider.setFixedWidth(width)
        self.slider.setRange(0, 100)
        self.slider.setValue(random.randint(30,70))
        self.slider.valueChanged.connect(lambda :self.changevalue())
        self.valueLabel = StrongBodyLabel(name + ":{}%".format(self.slider.value()))
        _layout.addWidget(self.valueLabel)
        _layout.addWidget(self.slider)
        # 为当前 QFrame 设置布局
        self.setLayout(_layout)

    def updataSliderWidth(self,width):
        self.slider.setFixedWidth(width)

    def changevalue(self):
        v = self.slider.value()
        if v<=9:
            v = "0" + str(v)
        else:
            v = str(v)
        self.valueLabel.setText(self.name +":{}%".format(v))

    def getvalue(self):
        return self.slider.value()

    def addwidget(self,layout):
        layout.addWidget(self)


