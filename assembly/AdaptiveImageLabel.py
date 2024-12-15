import time
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QAction
from qfluentwidgets import ImageLabel, SmoothScrollArea
from qfluentwidgets import RoundMenu, Action, MenuAnimationType
from qfluentwidgets import FluentIcon as FIF


class AdaptiveImageLabel(ImageLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.original_pixmap = None
        self.setBorderRadius(18, 18, 18, 18)
        self.setScaledContents(True)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def setCustomImage(self, image_path: str):
        """设置图片并保存原始图片"""
        self.original_pixmap = QPixmap(image_path)
        self.setPixmap(self.original_pixmap)
        QTimer.singleShot(0, self.updateSize)

    def updateSize(self):
        """更新图片大小"""
        if not self.original_pixmap or not self.parent():
            return

        scroll_area = self.parent().parent().parent()
        if isinstance(scroll_area, SmoothScrollArea):
            available_width = scroll_area.viewport().width()
        else:
            available_width = self.parent().width()

        target_width = (available_width - 60) // 2
        ratio = self.original_pixmap.height() / self.original_pixmap.width()
        target_height = int(target_width * ratio)
        self.setFixedSize(target_width, target_height)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)

    def contextMenuEvent(self, e):
        menu = RoundMenu(parent=self)
        # add actions
        menu.addAction(Action(FIF.COPY, '复制'))
        menu.actions()[0].setCheckable(True)
        menu.actions()[0].setChecked(True)

        # add sub menu
        submenu = RoundMenu("添加到", self)
        submenu.setIcon(FIF.ADD)
        submenu.addActions([
            Action(FIF.VIDEO, '收藏'),
        ])
        menu.addMenu(submenu)

        # show menu
        menu.exec(e.globalPos(), aniType=MenuAnimationType.DROP_DOWN)
