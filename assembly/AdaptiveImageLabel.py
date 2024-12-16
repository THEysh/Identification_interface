import time
from PyQt5.QtCore import Qt, QTimer, QRectF
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QColor, QPen, QPainterPath
from qfluentwidgets import ImageLabel, SmoothScrollArea
from qfluentwidgets import RoundMenu, Action, MenuAnimationType
from qfluentwidgets import FluentIcon as FIF


class AdaptiveImageLabel(ImageLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.original_pixmap = None
        self.radius = 18
        self.setBorderRadius(self.radius, self.radius, self.radius, self.radius)
        self.setScaledContents(True)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.is_hovered = False
        self.is_selected = False

        # 设置部件接受悬停事件
        self.setMouseTracking(True)
        self.setStyleSheet("""
            AdaptiveImageLabel {
                border: 2px solid transparent;
            }
            AdaptiveImageLabel:hover {
                border: 2px solid #448AFF;
            }
            AdaptiveImageLabel:selected {
                border: 2px solid #FF4081;
            }
        """)

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

    def enterEvent(self, event):
        """鼠标进入事件"""
        super().enterEvent(event)
        self.is_hovered = True
        self.update()

    def leaveEvent(self, event):
        """鼠标离开事件"""
        super().leaveEvent(event)
        self.is_hovered = False
        self.update()


    def paintEvent(self, event):
        """绘制事件"""
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # 启用抗锯齿
        if self.is_hovered:
            painter.setBrush(QBrush(QColor(68, 136, 255, 128)))  # 半透明的蓝色
            pen = QPen(Qt.black, 4)  # 黑色边框，宽度为2像素
            painter.setPen(pen)
            # 创建一个带有圆角的矩形路径
            path = QPainterPath()
            rect = self.rect()
            path.addRoundedRect(QRectF(rect), 18, 18)
            # 绘制路径
            painter.drawPath(path)

    def contextMenuEvent(self, e):
        """右键菜单事件"""
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
