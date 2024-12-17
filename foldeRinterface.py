# coding:utf-8
import copy
import time
from PyQt5.QtCore import Qt, QTimer, QSize, QEasingCurve, QEventLoop, QThread, pyqtSignal, QCoreApplication
from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QFileDialog,
                             QSplitter, QLabel, QGridLayout)
from PyQt5.QtGui import QPixmap, QResizeEvent, QFontMetrics, QImage
from qfluentwidgets import (PrimaryPushButton, ImageLabel,
                            SmoothScrollArea, FlowLayout, PushButton, FlyoutView, Flyout, InfoBar, InfoBarPosition,
                            SwitchButton, TogglePushButton, StateToolTip, InfoBadge, InfoBadgePosition, ToolButton)
from qfluentwidgets import FluentIcon as FIF
from pathlib import Path
from assembly.AdaptiveImageLabel import AdaptiveImageLabel
from assembly.InfoDisplayCards import InfoDisplayCards
from assembly.PredictionState import PredictionStateMachine, Status
from assembly.ResultDisplayCard import ResultDisplayCard
from assembly.asyncProcessor import _ImagePredictThread
from assembly.autoResizePushButton import AutoResizePushButton
from assembly.clockShow import ClockShow
from assembly.common import getEmj
from assembly.displayNumericSlider import DisplayNumericSlider
from assembly.smoothResizingScrollArea import SmoothResizingScrollArea


class _LeftContent():
    def __init__(self, frame: QFrame):
        self.MaximumWidth = 400
        # 左侧面板
        self.leftPanel = frame
        self.leftPanel.setMinimumWidth(int(self.MaximumWidth*0.5))
        self.leftPanel.setMaximumWidth(self.MaximumWidth)
        self.leftLayout = FlowLayout(self.leftPanel, needAni=True)
        # 左侧按钮和标签
        self.selectFolderBtn = PrimaryPushButton(FIF.FOLDER_ADD, ' 选择文件夹 ', self.leftPanel)
        # 图片数量
        self.imageCountBtn = PushButton(FIF.PHOTO," 图片数量: 0", self.leftPanel)
        self.preModelbtn = PrimaryPushButton(FIF.SEND, "开始预测", self.leftPanel)
        self.slider1 = DisplayNumericSlider(int(self.MaximumWidth*0.5),name="iou  ",parent=self.leftPanel)
        self.slider2 = DisplayNumericSlider(int(self.MaximumWidth * 0.5), name="conf", parent=self.leftPanel)
        self.folderInfoBtn = AutoResizePushButton(self.MaximumWidth, FIF.FOLDER, " 未选择 ", self.leftPanel)
        self.resultInfoCard = ResultDisplayCard(int(self.MaximumWidth*0.7),self.leftPanel)
        self.timeClock = ClockShow(self.leftPanel)

        self._addWidget()

    def _addWidget(self):
        # 添加到左侧布局
        self.leftLayout.addWidget(self.selectFolderBtn)
        self.leftLayout.addWidget(self.imageCountBtn )
        self.leftLayout.addWidget(self.preModelbtn)
        self.slider1.addwidget(self.leftLayout)
        self.slider2.addwidget(self.leftLayout)
        self.resultInfoCard.addwidget(self.leftLayout)
        self.leftLayout.addWidget(self.folderInfoBtn)
        self.leftLayout.addWidget(self.timeClock)

    def updateImgCount(self, newnum):
        try:
            self.imageCountBtn.setText(f"图片数量: {str(newnum).zfill(3)}")
        except:
            pass

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
        self.maxImgCount = 0
        self.files = 0
        self.predictWork = None
        self.foldPlayCards = InfoDisplayCards(self)
        self.setObjectName('FolderInterface')
        self.setupUI()
        # 状态机
        self.predictState = PredictionStateMachine()
        # 创建按钮链接
        self.leftRegion.preModelbtn.clicked.connect(lambda:self._loadModelFunction())
        # 加载默认路径
        folder_path = "./resource/some_img"
        self._loadimg(folder_path)
    def setupUI(self):
        # 设置主布局
        self.splitter.addWidget(self.leftRegion.leftPanel)
        self.splitter.addWidget(self.rightRegion)
        self.hBoxLayout.addWidget(self.splitter)
        # 连接信号
        self.leftRegion.selectFolderBtn.clicked.connect(self._selectFolder)

    def _loadModelFunction(self):
        print(self.predictState)
        if self.predictState.status == Status.NOT_PREDICTED:
            self.predictState.start_prediction()
            self.leftRegion.preModelbtn.setText("预测中...")


        elif self.predictState.status == Status.PREDICTING:
            self.predictState.stop_prediction()
            self.leftRegion.preModelbtn.setText("预测已经被停止")
            self.leftRegion.preModelbtn.setEnabled(False)

    def _modelPredict(self):
        # 显示加载模型卡
        iou, conf = self.leftRegion.slider1.getvalue(), self.leftRegion.slider2.getvalue()
        self.foldPlayCards.computationPredictCard()
        for i in range(len(self.files)):
            predictData = [self.files[i], iou, conf]
            self.predictWork = _ImagePredictThread(self.client.predict, predictData)
            self.predictWork.varSignalConnector.connect(self._finishOneTask)
            self.predictWork.start()
    def _finishOneTask(self, predictResultsList: list):

        [saveDir, rectanglePosDict, scores, classes, inferenceTime] = predictResultsList

        if saveDir is None or rectanglePosDict is None or scores is None or classes is None \
                or inferenceTime is None:
            InfoBar.error(
                title='错误',
                content="服务器未响应",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_LEFT,
                duration=-1,
                parent=self.leftRegion.leftPanel
            )
        else:
            self.leftRegion.resultInfoCard.show(saveDir, rectanglePosDict, scores, classes, inferenceTime)
            # 显示加载模型卡-完成
            # 加载图片
            self.rightRegion.imageLabel2.setCustomImage(saveDir)
            self.rightRegion.imageLabel2.zoom_factor = 1.0
        self._computationDisplayCard()

    def resizeEvent(self, event: QResizeEvent):
        """窗口大小改变时更新所有图片的大小"""
        super().resizeEvent(event)

    def updateAllImages(self):
        """更新所有图片的大小"""
        self.rightRegion.updataScrollAreaItem()

    def _clearImages(self):
        """清除所有现有的图片"""
        self.maxImgCount = 0
        self.files = 0
        self.leftRegion.updateImgCount(0)
        self.rightRegion.clearScrollAreaItem()

    def _selectFolder(self):
        folderPath = QFileDialog.getExistingDirectory(
            self,
            "选择图片文件夹",
            "./",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        if not folderPath:
            return
        self._loadimg(folderPath)

    def _loadimg(self, folder_path):
        # 清除现有图片
        self._clearImages()
        # 更新文件夹信息
        self.leftRegion.folderInfoBtn.setText(f"{folder_path}")
        # 获取所有图片文件
        image_files = []
        for ext in self.rightRegion.image_extensions:
            image_files.extend(Path(folder_path).glob(f'*{ext}'))
        self.files = len(image_files)
        if self.files > 0:
            # 开始显示加载的卡片
            self.foldPlayCards.computationLoadImageCard()
        self.thread = _ImageLoaderThread(image_files, parent=None)
        self.thread.varSignalConnector.connect(self._addImageLabel)
        self.thread.start()

    def _addImageLabel(self, pixmap:QPixmap, index:int):
        imageLabel = AdaptiveImageLabel(self.rightRegion)
        imageLabel.setPixmap(pixmap)
        row = index
        col = 0
        self.rightRegion.layout.addWidget(imageLabel, row, col)
        if index+1 > self.maxImgCount:
            self.maxImgCount = index + 1
            self.leftRegion.updateImgCount(self.maxImgCount)
        if index+1==self.files:
            # 结束显示加载的卡片
            self.foldPlayCards.computationLoadImageCard()

class _ImageLoaderThread(QThread):
    varSignalConnector = pyqtSignal(QPixmap, int)
    def __init__(self, image_files, parent=None):
        super().__init__(parent)
        self.image_files = image_files
    def run(self):
        for i, image_path in enumerate(self.image_files):
            pixmap = QPixmap(str(image_path))
            # 延迟加载，避免卡顿
            time.sleep(0.002)
            self.varSignalConnector.emit(pixmap, i)

