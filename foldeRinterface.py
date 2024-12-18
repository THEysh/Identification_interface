# coding:utf-8
import time
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QFileDialog,
                             QSplitter, QGridLayout)
from PyQt5.QtGui import QPixmap, QResizeEvent
from qfluentwidgets import (PrimaryPushButton, FlowLayout, PushButton)
from qfluentwidgets import FluentIcon as FIF
from pathlib import Path
from assembly.AdaptiveImageLabel import AdaptiveImageLabel
from assembly.InfoDisplayCards import InfoDisplayCards
from assembly.PredictionState import PredictionStateMachine, Status
from assembly.ResultDisplayCard import ResultDisplayCard
from assembly.asyncProcessor import ImageLoaderThread, ImagePredictFolderThread, \
    AsyncFolderInterfaceWork
from assembly.autoResizePushButton import AutoResizePushButton
from assembly.clockShow import ClockShow
from assembly.common import getSpillFilepath
from assembly.displayNumericSlider import DisplayNumericSlider
from assembly.smoothResizingScrollArea import SmoothResizingScrollArea
from post.requestSent import PredictionClient


class _LeftContent():
    def __init__(self, frame: QFrame):
        self.MaximumWidth = 400
        # 左侧面板
        self.leftPanel = frame
        self.leftPanel.setMinimumWidth(int(self.MaximumWidth * 0.5))
        self.leftPanel.setMaximumWidth(self.MaximumWidth)
        self.leftLayout = FlowLayout(self.leftPanel, needAni=True)
        # 左侧按钮和标签
        self.selectFolderBtn = PrimaryPushButton(FIF.FOLDER_ADD, ' 选择文件夹 ', self.leftPanel)
        # 图片数量
        self.imageCountBtn = PushButton(FIF.PHOTO, " 图片数量: 0", self.leftPanel)
        self.preModelbtn = PrimaryPushButton(FIF.SEND, "开始预测", self.leftPanel)
        self.slider1 = DisplayNumericSlider(int(self.MaximumWidth * 0.5), name="iou  ", parent=self.leftPanel)
        self.slider2 = DisplayNumericSlider(int(self.MaximumWidth * 0.5), name="conf", parent=self.leftPanel)
        self.modelInputData = ["iou", "conf"]
        self.folderInfoBtn = AutoResizePushButton(self.MaximumWidth, FIF.FOLDER, " 未选择 ", self.leftPanel)
        self.resultInfoCard = ResultDisplayCard(int(self.MaximumWidth * 0.7), self.leftPanel)
        self.timeClock = ClockShow(self.leftPanel)

        self._addWidget()

    def _addWidget(self):
        # 添加到左侧布局
        self.leftLayout.addWidget(self.selectFolderBtn)
        self.leftLayout.addWidget(self.imageCountBtn)
        self.leftLayout.addWidget(self.preModelbtn)
        self.slider1.addwidget(self.leftLayout)
        self.slider2.addwidget(self.leftLayout)
        self.resultInfoCard.addwidget(self.leftLayout)
        self.leftLayout.addWidget(self.folderInfoBtn)
        self.leftLayout.addWidget(self.timeClock)

    def updateImgCount(self, newnum):
        self.imageCountBtn.setText(f"图片数量: {str(newnum).zfill(3)}")


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
    def __init__(self, client: PredictionClient, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        # 创建一个 QSplitter 并设置为水平方向
        self.splitter = QSplitter()
        self.leftRegion = _LeftContent(QFrame(self))
        self.rightRegion = _RightContent(QFrame(self))
        self.client = client
        self.maxImgCount = 0
        self.imgFilesPath = []
        self.thread = None
        self.threadWorks = AsyncFolderInterfaceWork(ThreadCount=2)  # 异步线程数目
        self.foldPlayCards = InfoDisplayCards(self)
        self.setObjectName('FolderInterface')
        self.setupUI()
        # 状态机
        self.predictState = PredictionStateMachine()
        # 创建按钮链接
        self.leftRegion.preModelbtn.clicked.connect(lambda: self._loadModelFunction())
        # 加载默认路径
        folder_path = "./resource/some_img"
        self._loadimg(folder_path)

    def _statusDisplayUpdate(self):
        if self.predictState.status == Status.PREDICT_STOPING or self.predictState.status == Status.PREDICTED:
            self.leftRegion.preModelbtn.setEnabled(False)
        else:
            self.leftRegion.preModelbtn.setEnabled(True)
        text = self.predictState.statusValue
        self.leftRegion.preModelbtn.setText(text)

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
            self._modelPredict()
        elif self.predictState.status == Status.PREDICTING:
            self.predictState.stop_prediction()
            self.leftRegion.preModelbtn.setEnabled(False)
        self._statusDisplayUpdate()

    @property
    def getslidersValue(self):
        iou, conf = self.leftRegion.slider1.getvalue(), self.leftRegion.slider2.getvalue()
        return [iou, conf]

    def _modelPredict(self):
        # 显示加载模型卡
        if len(self.imgFilesPath) <= 0: return
        slidersValue = self.getslidersValue
        predictDatas = getSpillFilepath(self.imgFilesPath, self.threadWorks.threadCount, slidersValue)
        for i in range(self.threadWorks.threadCount):
            tempName = f"predictWork{i + 1}"
            predictWork = ImagePredictFolderThread(self.client.predict, predictDatas[i],
                                                   name=tempName)
            predictWork.varSignalConnector.connect(self._finishOneTask)
            # predictWork.finished.connect(self._finishwork)
            # 保存线程
            self.threadWorks.addPreThread(tempName, predictWork)
            predictWork.start()



    def _finishOneTask(self, predictResultsList: list):
        [saveDir, rectanglePosDict, scores, classes, inferenceTime, threadName] = predictResultsList
        if saveDir is None or rectanglePosDict is None or scores is None or classes is None \
                or inferenceTime is None:
            print(self.predictState)
            print("len", len(self.threadWorks.preThreads))
            if len(self.threadWorks.preThreads) == 0:
                # 线程已经清理完毕
                self.predictState.stoping_notprediction()
                self._statusDisplayUpdate()
            else:
                # 异常显示
                self.foldPlayCards.InfoBarErr()
                # 异常，当前线程,删除
                self.threadWorks.stopOnePreThread(name=threadName)
                # 预测中-》停止中
                self.predictState.stop_prediction()
                self._statusDisplayUpdate()

        else:
            self.leftRegion.resultInfoCard.show(saveDir, rectanglePosDict, scores, classes, inferenceTime)
            # 加载图片
        # 显示加载模型卡-完成
        # self.foldPlayCards.computationPredictCard()

    def resizeEvent(self, event: QResizeEvent):
        """窗口大小改变时更新所有图片的大小"""
        super().resizeEvent(event)

    def updateAllImages(self):
        """更新所有图片的大小"""
        self.rightRegion.updataScrollAreaItem()

    def _clearImages(self):
        """清除所有现有的图片"""
        self.maxImgCount = 0
        self.imgFilesPath = []
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
        self.imgFilesPath = []
        for image_file in image_files:
            self.imgFilesPath.append(str(image_file))
        if len(self.imgFilesPath) > 0:
            # 开始显示加载的卡片
            self.foldPlayCards.computationLoadImageCard()
        thread = ImageLoaderThread(image_files, parent=None)
        thread.varSignalConnector.connect(self._addImageLabel)
        self.threadWorks.addLoadimgThread(name="loadimgThread", work=thread)
        thread.start()

    def _addImageLabel(self, pixmap: QPixmap, index: int):
        imageLabel = AdaptiveImageLabel(self.rightRegion)
        imageLabel.setPixmap(pixmap)
        row = index
        col = 0
        self.rightRegion.layout.addWidget(imageLabel, row, col)
        if index + 1 > self.maxImgCount:
            self.maxImgCount = index + 1
            self.leftRegion.updateImgCount(self.maxImgCount)
        if index + 1 == len(self.imgFilesPath):
            # 结束显示加载的卡片
            self.foldPlayCards.computationLoadImageCard()
