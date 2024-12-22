from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QPixmap, QPainter, QPen
from qfluentwidgets import ImageLabel, SmoothScrollArea
from qfluentwidgets import RoundMenu, Action, MenuAnimationType
from qfluentwidgets import FluentIcon as FIF


class AdaptiveImageLabel(ImageLabel):
    indexImgInfoSignal = pyqtSignal(int, str)
    def __init__(self, index:int, key='org', parent=None):
        super().__init__(parent)
        self.index = index
        self.key = key
        self.original_pixmap = None
        self.path = None
        self.radius = 18
        self.setBorderRadius(self.radius, self.radius, self.radius, self.radius)
        self.setScaledContents(True)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.is_hovered = False
        self.is_selected = False
        # 设置部件接受悬停事件
        self.setMouseTracking(True)
        self.path = None

    def setPixmap(self,pixmap):
        self.original_pixmap = pixmap
        super().setPixmap(pixmap)
        QTimer.singleShot(0, self.updateSize)

    def setCustomImage(self, image_path: str):
        self.path = image_path
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
        if self.original_pixmap.width() > 0:
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

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.is_selected = True
            self.indexImgInfoSignal.emit(self.index, self.key)
            self.update()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.is_selected = False

    def paintEvent(self, event):
        """绘制事件"""
        super().paintEvent(event)
        if self.is_selected:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)  # 使绘图更加平滑
            # 创建一个 QPen 对象并设置其属性
            pen = QPen(Qt.red, 5)
            pen.setJoinStyle(Qt.RoundJoin)  # 设置线条连接处为圆角
            painter.setPen(pen)
            # 创建一个圆角矩形
            # 使用 drawRoundedRect 方法绘制圆角矩形
            painter.drawRoundedRect(self.rect(), self.radius, self.radius)
        elif self.is_hovered:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)  # 使绘图更加平滑
            # 创建一个 QPen 对象并设置其属性
            pen = QPen(Qt.blue, 5)
            pen.setJoinStyle(Qt.RoundJoin)  # 设置线条连接处为圆角
            painter.setPen(pen)
            # 创建一个圆角矩形
            # 使用 drawRoundedRect 方法绘制圆角矩形
            painter.drawRoundedRect(self.rect(), self.radius, self.radius)

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
