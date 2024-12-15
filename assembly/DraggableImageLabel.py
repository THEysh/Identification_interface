import os
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPixmap, QWheelEvent, QMouseEvent
from qfluentwidgets import FluentIcon as FIF, ImageLabel, RoundMenu, Action, MenuAnimationType


class DraggableImageLabel(ImageLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.dragging = True
        self.offset = QPoint()
        self.zoom_factor = 1.0
        self.original_height = 300
        self.current_pos = QPoint(0, 0)
        self.setScaledContents(True)

    def setCustomImage(self, image_path: str):
        if not os.path.isfile(image_path):
            print(f"文件夹: '{image_path}' 路径失效.")
            return
        self.setImage(image_path)
        self.scaledToHeight(self.original_height)
        self.original_pixmap = QPixmap(image_path)

    def wheelEvent(self, event: QWheelEvent):
        current_pos = self.pos()
        if event.angleDelta().y() > 0:
            self.zoom_factor *= 1.1
        else:
            self.zoom_factor *= 0.9
        self.zoom_factor = max(0.1, min(self.zoom_factor, 5.0))
        new_height = int(self.original_height * self.zoom_factor)
        new_width = int(new_height * self.original_pixmap.width() / self.original_pixmap.height())
        self.setFixedSize(new_width, new_height)
        self.move(current_pos)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.pos()
            self.raise_()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.dragging:
            new_pos = self.mapToParent(event.pos() - self.offset)
            self.move(new_pos)
            self.current_pos = new_pos

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.dragging = False
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