import random
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QSlider, QHBoxLayout, QVBoxLayout
from qfluentwidgets import Slider, Flyout, InfoBarIcon, PushButton, ToolTipFilter, ToolTipPosition, BodyLabel, \
    StrongBodyLabel


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

    def changevalue(self):
        self.valueLabel.setText(self.name +":{}%".format(self.slider.value()))

    def addwidget(self,layout):
        layout.addWidget(self)


