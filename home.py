# coding:utf-8
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QSplitter
from qfluentwidgets import FlowLayout, StateToolTip, PrimaryPushButton, InfoBar, InfoBarPosition
from PyQt5.QtWidgets import QFileDialog
from qfluentwidgets import FluentIcon as FIF
from assembly.DraggableImageLabel import DraggableImageLabel
from assembly.ResultDisplayCard import ResultDisplayCard
from assembly.clockShow import ClockShow
from assembly.displayNumericSlider import DisplayNumericSlider
from assembly.common import getEmj
from post.requestSent import PredictionClient

class _LeftContent():
    def __init__(self, frame: QFrame):
        self.MaximumWidth = 350
        self.leftPanel = frame
        self.leftPanel.setMinimumWidth(int(self.MaximumWidth*0.5))
        self.leftPanel.setMaximumWidth(self.MaximumWidth)
        self.leftLayout = FlowLayout(self.leftPanel, needAni=True)
        self.loadImage1Btn = PrimaryPushButton(FIF.UPDATE, ' 加载图片 ', self.leftPanel)
        self.slider1 = DisplayNumericSlider(int(self.MaximumWidth*0.7),name="iou  ",parent=self.leftPanel)
        self.slider2 = DisplayNumericSlider(int(self.MaximumWidth * 0.7), name="conf", parent=self.leftPanel)
        self.resultInfoCard = ResultDisplayCard(int(self.MaximumWidth*0.7),self.leftPanel)
        self.timeClock = ClockShow(self.leftPanel)
        self._addWidgets()

    def _addWidgets(self):
        self.leftLayout.addWidget(self.loadImage1Btn)
        self.slider1.addwidget(self.leftLayout)
        self.slider2.addwidget(self.leftLayout)
        self.resultInfoCard.addwidget(self.leftLayout)
        self.leftLayout.addWidget(self.timeClock)

class _RightContent():
    def __init__(self, frame: QFrame):
        self.rightPanel = frame
        self.rightLayout = FlowLayout(self.rightPanel, needAni=True)
        self.imageLabel1 = DraggableImageLabel(self.rightPanel)
        self.imageLabel2 = DraggableImageLabel(self.rightPanel)
        self.imageLabel1.setCustomImage('resource/painting_girl.png')
        self.imageLabel2.setCustomImage('resource/painting_girl.png')
        self.imageLabel1.setBorderRadius(10, 10, 10, 10)
        self.imageLabel2.setBorderRadius(10, 10, 10, 10)
        self._addWidgets()

    def _addWidgets(self):
        self.rightLayout.addWidget(self.imageLabel1)
        self.rightLayout.addWidget(self.imageLabel2)

class HomeInterface(QFrame):
    def __init__(self, client:PredictionClient, parent=None):
        super().__init__(parent=parent)
        self.client = client
        self.hBoxLayout = QHBoxLayout(self)
        self.splitter = QSplitter()
        self.leftRegion = _LeftContent(QFrame(self))
        self.rightRegion = _RightContent(QFrame(self))
        self.predictWork = None
        self.stateTooltip = None
        self.setupUI()
        self.setObjectName('HomeInterface')

    def setupUI(self):
        self.splitter.addWidget(self.leftRegion.leftPanel)
        self.splitter.addWidget(self.rightRegion.rightPanel)
        self.hBoxLayout.addWidget(self.splitter)
        self.leftRegion.loadImage1Btn.clicked.connect(lambda:self.loadImage())

    def loadImage(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            f"选择一张图片进行预测",
            "./",
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if len(file_path) == 0: return
        self.rightRegion.imageLabel1.setCustomImage(file_path)
        self.modelPredict(file_path, self.leftRegion.slider1.getvalue(),
                              self.leftRegion.slider2.getvalue())


    def modelPredict(self, filePath, iou, conf):
        # 显示加载模型卡
        self.ComputationDisplayCard()
        predictData = [filePath, iou, conf]
        print(predictData)
        self.predictWork = _ImagePredictThread(self.client.predict, predictData)
        self.predictWork.varSignalConnector.connect(self._modelPredictOut)
        self.predictWork.start()


    def _modelPredictOut(self,predictResultsList:list):
        [saveDir, rectanglePosDict, scores, classes, inferenceTime] = predictResultsList
        if saveDir is None or rectanglePosDict is None or scores is None or classes is None\
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
        self.ComputationDisplayCard()

    def ComputationDisplayCard(self):
        if self.stateTooltip:
            self.stateTooltip.setContent('结束啦' + getEmj())
            self.stateTooltip.setState(True)
            self.stateTooltip = None
        else:
            self.stateTooltip = StateToolTip('模型正在全力计算中' + getEmj(), '请耐心等待呦~~', self)
            self.stateTooltip.move(510, 30)
            self.stateTooltip.show()


class _ImagePredictThread(QThread):
    # list的数值分别为：saveDir, rectanglePosDict, scores, classes, inferenceTime
    varSignalConnector = pyqtSignal(list)
    def __init__(self, requestsFunction, predictData: list, parent=None):
        super().__init__(parent)
        self.predictData = predictData
        self.requestsFunction = requestsFunction

    def run(self):
        print("run, begin")
        res = self.requestsFunction(self.predictData)
        if res is None:
            self.varSignalConnector.emit([None,None,None,None,None])
        else:
            saveDir = res["save_dir"]
            rectanglePosDict = res["rectangle_pos"]
            scores = res["scores"]
            classes = res["classes"]
            inferenceTime = res["inference_time"]
            self.varSignalConnector.emit([saveDir, rectanglePosDict, scores, classes, inferenceTime])