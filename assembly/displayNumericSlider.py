import random
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame,QHBoxLayout
from qfluentwidgets import Slider, StrongBodyLabel


class DisplayNumericSlider(QFrame):
    def __init__(self, name:str, parent=None):
        super().__init__(parent)
        _layout = QHBoxLayout()
        self.name = name
        self.slider = Slider(Qt.Horizontal, self)
        self.slider.setFixedWidth(300)
        self.slider.setRange(0, 1000)
        self.slider.setValue(random.randint(300,700))
        self.slider.valueChanged.connect(lambda :self.changevalue())
        self.valueLabel = StrongBodyLabel()
        self.changevalue()
        _layout.addWidget(self.valueLabel)
        _layout.addWidget(self.slider)
        # 为当前 QFrame 设置布局
        self.setLayout(_layout)

    def setValue(self, value:float) -> None:
        self.slider.setValue(int(value*1000))

    def updataSliderWidth(self,width):
        self.slider.setFixedWidth(width)

    def changevalue(self):
        v = self.getvalue
        self.valueLabel.setText(self.name + ": {:.3f}".format(v))

    @property
    def getvalue(self):
        return self.slider.value()/1000

    def addwidget(self,layout):
        layout.addWidget(self)


