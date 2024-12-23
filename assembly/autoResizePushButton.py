from PyQt5.QtGui import QFontMetrics
from PyQt5.QtWidgets import  QWidget
from qfluentwidgets import FluentIconBase, PushButton



class AutoResizePushButton(PushButton):
    def __init__(self, icon: FluentIconBase, text: str, parent: QWidget = None):
        super().__init__(parent=parent)
        super().setText(text)
        super().setIcon(icon)
        self.widthLimit = 300
        self.textLen = 0
    def wrap_text(self, text:str):
        metrics = QFontMetrics(self.font())
        res = ""
        ans = ""
        for word in text:
            newMetrics = metrics.width(res)
            if newMetrics <= self.widthLimit:
                res += word
            else:
                ans += res + "\n"
                res = ""
        ans += res
        return ans

    def setText(self, text):
        text = self.wrap_text(text)
        super().setText(text)
