# coding:utf-8
import copy
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QSplitter
from qfluentwidgets import FlowLayout, PrimaryPushButton
from PyQt5.QtWidgets import QFileDialog
from qfluentwidgets import FluentIcon as FIF
from assembly.DataInfo import DataInfo
from assembly.DraggableImageLabel import DraggableImageLabel
from assembly.InfoDisplayCards import InfoDisplayCards
from assembly.ResultDisplay import ResultDisplayCard
from assembly.asyncProcessor import ImagePredictThread
from assembly.displayNumericSlider import DisplayNumericSlider
from assembly.YoloMod import YoloModel
from confSet import ConfGlobals


class _LeftContent:
    def __init__(self, frame: QFrame):

        self.leftPanel = frame
        self.MaximumWidth = 400
        self.leftPanel.setMinimumWidth(int(self.MaximumWidth * 0.01))
        self.leftPanel.setMaximumWidth(self.MaximumWidth)
        self.leftLayout = FlowLayout(self.leftPanel, needAni=True)
        self.loadImage1Btn = PrimaryPushButton(FIF.UPDATE, ' 加载图片 ', self.leftPanel)
        self.slider2 = None
        self.slider1 = None
        self.setSliderchackConfIou()
        self.resultInfoCard = ResultDisplayCard(self.leftPanel)
        self._addWidgets()

    def setSliderchackConfIou(self):
        self.slider1 = DisplayNumericSlider(name="iou  ", parent=self.leftPanel)
        self.slider2 = DisplayNumericSlider(name="conf", parent=self.leftPanel)
        if ('iou' in ConfGlobals) and type(ConfGlobals['iou']) == float and 0.0 < ConfGlobals['iou'] <= 1.0:
            self.slider1.setValue(ConfGlobals['iou'])
        if ('conf' in ConfGlobals) and type(ConfGlobals['conf']) == float and 0.0 < ConfGlobals['conf'] <= 1.0:
            self.slider2.setValue(ConfGlobals['conf'])

    def _addWidgets(self):
        self.leftLayout.addWidget(self.loadImage1Btn)
        self.slider1.addwidget(self.leftLayout)
        self.slider2.addwidget(self.leftLayout)
        self.leftLayout.addWidget(self.resultInfoCard)

class _RightContent:
    def __init__(self, frame: QFrame):
        self.rightPanel = frame
        self.rightLayout = FlowLayout(self.rightPanel, needAni=True)
        self.imageLabel1 = DraggableImageLabel(self.rightPanel)
        self.imageLabel2 = DraggableImageLabel(self.rightPanel)
        # self.imageLabel1.setCustomImage('resource/cut_RGB_20240719084737.png')

        self.imageLabel1.setBorderRadius(10, 10, 10, 10)
        self.imageLabel2.setBorderRadius(10, 10, 10, 10)
        self._addWidgets()

    def _addWidgets(self):
        self.rightLayout.addWidget(self.imageLabel1)
        self.rightLayout.addWidget(self.imageLabel2)


class HomeInterface(QFrame):
    def __init__(self, yoloMod:YoloModel, datainfo:DataInfo, parent=None):
        super().__init__(parent=parent)
        self.yolo = yoloMod
        self.dataInfo = datainfo
        self.hBoxLayout = QHBoxLayout(self)
        self.splitter = QSplitter()
        self.leftRegion = _LeftContent(QFrame(self))
        self.rightRegion = _RightContent(QFrame(self))
        self.homeDisplayCard = InfoDisplayCards(self)
        self.predictWork = None
        self.setupUI()
        self.setObjectName('HomeInterface')

        self.leftRegion.loadImage1Btn.clicked.connect(lambda:self.loadImage())

    def setupUI(self):
        self.splitter.addWidget(self.leftRegion.leftPanel)
        self.splitter.addWidget(self.rightRegion.rightPanel)
        self.hBoxLayout.addWidget(self.splitter)


    def loadImage(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            f"选择一张图片进行预测",
            "./",
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if len(file_path) == 0: return
        self.rightRegion.imageLabel1.setCustomImage(file_path)
        # 更新信息
        pixmap = QPixmap(file_path)
        self.dataInfo.imgAddInfo(index=-1, key="org", info={"pixmap": pixmap,'path':file_path})
        self._modelPredict(file_path)

    def _modelPredict(self, filePath):
        iou, conf = self.leftRegion.slider1.getvalue, self.leftRegion.slider2.getvalue
        # 显示加载模型卡
        self.homeDisplayCard.computationPredictCard()
        predictData = [filePath, iou, conf]
        tempYoloModel = copy.deepcopy(self.yolo)
        self.predictWork = ImagePredictThread(tempYoloModel, predictData, name="home_predictWork1")
        self.predictWork.varSignalConnector.connect(self._modelPredictOut)
        self.predictWork.start()

    def _modelPredictOut(self, predictResultsList: list):
        [savePath, rectanglePosDict, scores, classes, imgshape, orgimgpath, inferenceTime] = predictResultsList
        pre_info = {"path": savePath,
                    "rectangle_pos": rectanglePosDict,
                    "scores": scores,
                    "classes": classes,
                    "inference_time": inferenceTime}
        self.dataInfo.imgAddInfo(index=-1, key="pre", info=pre_info)
        if rectanglePosDict is None:
            self.homeDisplayCard.InfoBarErr(parent=self.leftRegion.leftPanel)
        self.leftRegion.resultInfoCard.homeShow(savePath, rectanglePosDict, scores, classes, inferenceTime)
        self.rightRegion.imageLabel2.setCustomImage(savePath)
        self.rightRegion.imageLabel2.zoom_factor = 1.0
        self.homeDisplayCard.computationPredictCard()

