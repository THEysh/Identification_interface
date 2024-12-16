from PyQt5.QtCore import QEasingCurve, Qt, QTimer
from PyQt5.QtWidgets import QFrame, QGridLayout, QLabel
from qfluentwidgets import SmoothScrollArea


class SmoothResizingScrollArea(SmoothScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        # customize scroll animation
        self.setScrollAnimation(Qt.Vertical, 400, QEasingCurve.OutQuint)
        self.setScrollAnimation(Qt.Horizontal, 400, QEasingCurve.OutQuint)
    def resizeEvent(self, event):
        super().resizeEvent(event)
        QTimer.singleShot(0, self.updataScrollAreaItem)

    def updataScrollAreaItem(self):
        if self.layout is not None:
            for i in range(self.layout.count()):
                widget = self.layout.itemAt(i).widget()
                if isinstance(widget, QLabel):
                    widget.updateSize()

    def clearScrollAreaItem(self):
        """清除所有现有的图片"""
        if self.layout is not None:
            while self.layout.count():
                item = self.layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()