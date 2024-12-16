# coding:utf-8
import copy
import time

from PyQt5.QtCore import Qt, QTimer, QSize, QEasingCurve, QEventLoop, QThread, pyqtSignal, QCoreApplication
from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QFileDialog,
                             QSplitter, QLabel, QGridLayout)
from PyQt5.QtGui import QPixmap, QResizeEvent, QFontMetrics
from qfluentwidgets import (PrimaryPushButton, ImageLabel,
                            SmoothScrollArea, FlowLayout, PushButton, FlyoutView, Flyout, InfoBar, InfoBarPosition,
                            SwitchButton, TogglePushButton)
from qfluentwidgets import FluentIcon as FIF
from pathlib import Path

from assembly.AdaptiveImageLabel import AdaptiveImageLabel
from assembly.autoResizePushButton import AutoResizePushButton
from assembly.smoothResizingScrollArea import SmoothResizingScrollArea


class _LeftContent():
    def __init__(self, frame: QFrame):
        self.MaximumWidth = 300
        # 左侧面板
        self.leftPanel = frame
        self.leftPanel.setMinimumWidth(int(self.MaximumWidth*0.5))
        self.leftPanel.setMaximumWidth(self.MaximumWidth)
        self.leftLayout = FlowLayout(self.leftPanel, needAni=True)
        # 左侧按钮和标签
        self.selectFolderBtn = PrimaryPushButton(FIF.FOLDER_ADD, ' 选择文件夹 ', self.leftPanel)
        self.loadModelbtn = TogglePushButton(FIF.SEND, "加载模型", self.leftPanel)
        self.imageCountBtn = PushButton(FIF.PHOTO," 图片数量：0 ", self.leftPanel)
        self.folderInfoBtn = AutoResizePushButton(self.MaximumWidth, FIF.FOLDER, " 未选择 ", self.leftPanel)

        self.loadModelbtn.clicked.connect(lambda:self._loadModelFunction())
        self._addWidget()

    def _loadModelFunction(self):
        if self.loadModelbtn.text()=="加载模型":
            self.loadModelbtn.setText("正在加载模型中...")
        elif self.loadModelbtn.text()=="正在加载模型中...":
            self.loadModelbtn.setText("加载模型已经被终止")
            QTimer.singleShot(1500, self._loadModelFunction)
        elif self.loadModelbtn.text()== "加载模型已经被终止":
            self.loadModelbtn.setText("加载模型")

    def _addWidget(self):
        # 添加到左侧布局
        self.leftLayout.addWidget(self.selectFolderBtn)
        self.leftLayout.addWidget(self.loadModelbtn)
        self.leftLayout.addWidget(self.folderInfoBtn )
        self.leftLayout.addWidget(self.imageCountBtn )


class _RightContent(SmoothResizingScrollArea):
    def __init__(self, frame: QFrame):
        super().__init__(frame)
        # 设置右侧滚动区域
        self.panel = QFrame()
        self.layout = QGridLayout(self.panel)
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.setWidget(self.panel)
        self.setWidgetResizable(True)
        # 设置滚动区域滚动条始终不显示
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # 在setWidget后设置透明背景
        self.enableTransparentBackground()
        self.image_extensions = {'.png', '.jpg', '.jpeg', '.bmp'}

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
        folder_path = "./resource/some_img"
        self.loadimg(folder_path)

    def setupUI(self):
        # 设置主布局
        self.splitter.addWidget(self.leftRegion.leftPanel)
        self.splitter.addWidget(self.rightRegion)
        self.hBoxLayout.addWidget(self.splitter)
        # 连接信号
        self.leftRegion.selectFolderBtn.clicked.connect(self.selectFolder)

    def resizeEvent(self, event: QResizeEvent):
        """窗口大小改变时更新所有图片的大小"""
        super().resizeEvent(event)

    def updateAllImages(self):
        """更新所有图片的大小"""
        self.rightRegion.updataScrollAreaItem()

    def clearImages(self):
        """清除所有现有的图片"""
        self.rightRegion.clearScrollAreaItem()

    def selectFolder(self):
        folderPath = QFileDialog.getExistingDirectory(
            self,
            "选择图片文件夹",
            "./",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        if not folderPath:
            return
        self.loadimg(folderPath)

    def loadimg(self, folder_path):
        # 清除现有图片
        self.clearImages()
        # 更新文件夹信息
        self.leftRegion.folderInfoBtn.setText(f"{folder_path}")
        # 获取所有图片文件
        image_files = []
        for ext in self.rightRegion.image_extensions:
            image_files.extend(Path(folder_path).glob(f'*{ext}'))
        # 更新图片数量
        self.leftRegion.imageCountBtn.setText(f"图片数量：{len(image_files)}")
        for i, image_path in enumerate(image_files):
            imageLabel1 = AdaptiveImageLabel(self.rightRegion)
            imageLabel1.setCustomImage(str(image_path))
            row = i
            col = 0
            self.rightRegion.layout.addWidget(imageLabel1, row, col)
