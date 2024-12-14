from PyQt5.QtCore import QEasingCurve, Qt, QTimer
from PyQt5.QtWidgets import QFrame, QGridLayout, QLabel
from qfluentwidgets import SmoothScrollArea


class SmoothResizingScrollArea(SmoothScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 设置右侧滚动区域
        self.panel = QFrame()
        self.layout = QGridLayout(self.panel)
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.setWidget(self.panel)
        self.setWidgetResizable(True)
        # 设置滚动区域滚动条始终不显示
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # 自定义平滑滚动动画
        self.setScrollAnimation(Qt.Vertical, 200, QEasingCurve.OutQuint)
        # 在setWidget后设置透明背景
        self.enableTransparentBackground()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        QTimer.singleShot(0, self.updataScrollAreaItem)

    def updataScrollAreaItem(self):
        for i in range(self.layout.count()):
            widget = self.layout.itemAt(i).widget()
            if isinstance(widget, QLabel):
                widget.updateSize()

    def clearScrollAreaItem(self):
        """清除所有现有的图片"""
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()