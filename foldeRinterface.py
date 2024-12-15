# coding:utf-8
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QFileDialog,
                             QSplitter, QLabel)
from PyQt5.QtGui import QPixmap, QResizeEvent, QFontMetrics
from qfluentwidgets import (PrimaryPushButton, ImageLabel,
                            SmoothScrollArea, FlowLayout, PushButton)
from qfluentwidgets import FluentIcon as FIF
from pathlib import Path
from assembly.autoResizePushButton import AutoResizePushButton
from assembly.smoothResizingScrollArea import SmoothResizingScrollArea


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

class _LeftContent():
    def __init__(self, frame: QFrame):
        self.MaximumWidth = 300
        # 左侧面板
        self.leftPanel = frame
        self.leftPanel.setMaximumWidth(self.MaximumWidth)
        self.leftLayout = FlowLayout(self.leftPanel, needAni=True)
        # 左侧按钮和标签
        self.selectFolderBtn = PrimaryPushButton(FIF.FOLDER_ADD, ' 选择文件夹 ', self.leftPanel)
        self.imageCountBtn = PushButton(FIF.PHOTO," 图片数量：0 ", self.leftPanel)
        self.folderInfoBtn = AutoResizePushButton(self.MaximumWidth, FIF.FOLDER, " 未选择 ", self.leftPanel)
        self._addWidget()


    def _addWidget(self):
        # 添加到左侧布局
        self.leftLayout.addWidget(self.selectFolderBtn)
        self.leftLayout.addWidget(self.folderInfoBtn )
        self.leftLayout.addWidget(self.imageCountBtn )




class _RightContent():
    def __init__(self, frame: QFrame):
        # 右侧面板
        self.rightScrollArea = SmoothResizingScrollArea(frame)


class FolderInterface(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        # 创建一个 QSplitter 并设置为水平方向
        self.splitter = QSplitter()

        self.leftRegion = _LeftContent(QFrame(self))
        self.rightRegion = _RightContent(QFrame(self))
        self.setObjectName('FolderInterface')

        self.setupUI()
        # 加载默认路径
        folder_path = "resource/some_img"
        self.loadimg(folder_path)

    def setupUI(self):
        # 设置主布局
        self.splitter.addWidget(self.leftRegion.leftPanel)
        self.splitter.addWidget(self.rightRegion.rightScrollArea)
        self.hBoxLayout.addWidget(self.splitter)
        # 连接信号
        self.leftRegion.selectFolderBtn.clicked.connect(self.selectFolder)

    def resizeEvent(self, event: QResizeEvent):
        """窗口大小改变时更新所有图片的大小"""
        super().resizeEvent(event)

    def updateAllImages(self):
        """更新所有图片的大小"""
        self.rightRegion.rightScrollArea.updataScrollAreaItem()

    def clearImages(self):
        """清除所有现有的图片"""
        self.rightRegion.rightScrollArea.clearScrollAreaItem()

    def selectFolder(self):
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "选择图片文件夹",
            "./",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        if not folder_path:
            return
        self.loadimg(folder_path)

    def loadimg(self,folder_path):

        # 清除现有图片
        self.clearImages()

        # 更新文件夹信息
        print(folder_path)
        self.leftRegion.folderInfoBtn.setText(f"{folder_path}")

        # 获取所有图片文件
        image_files = []
        for ext in self.rightRegion.rightScrollArea.image_extensions:
            image_files.extend(Path(folder_path).glob(f'*{ext}'))

        # 更新图片数量
        self.leftRegion.imageCountBtn.setText(f"图片数量：{len(image_files)}")

        # 添加图片到网格布局
        for i, image_path in enumerate(image_files):
            image_label = AdaptiveImageLabel(self.rightRegion.rightScrollArea.panel)
            image_label.setCustomImage(str(image_path))
            row = i // 2
            col = i % 2
            self.rightRegion.rightScrollArea.layout.addWidget(image_label, row, col)

        self.updateAllImages()
