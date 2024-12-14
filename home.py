# coding:utf-8
from PIL.ImagePalette import random
from PyQt5.QtCore import Qt, QPoint, QEventLoop, QTimer
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QSplitter, QLayout
from PyQt5.QtGui import QWheelEvent, QMouseEvent, QPixmap
from qfluentwidgets import ImageLabel, FlowLayout, StrongBodyLabel, StateToolTip, PrimaryPushButton, PillPushButton, \
    PushButton
from PyQt5.QtWidgets import QFileDialog
import random
from qfluentwidgets import FluentIcon as FIF
from assembly.emoji import getEmj, getSadnessEmj


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


class leftContent(QFrame):
    def __init__(self, frame: QFrame):
        super().__init__(frame)
        self.leftPanel = frame
        self.leftPanel.setMaximumWidth(250)
        self.leftLayout = FlowLayout(self.leftPanel, needAni=True)
        self.loadImage1Btn = PrimaryPushButton(FIF.UPDATE, '加载图片 ', self.leftPanel)
        self.resultInfo = " 识别结果: ??? \n 置信度: ??? "
        self.predictionResultBt = PushButton(FIF.CALENDAR, self.resultInfo, self.leftPanel)
        self.predictionResultBt.setEnabled(False)

        self._addWidgets()

    def updatePredictResultInfo(self):
        inf_temp = random.randint(1, 101)
        inf_emj = getEmj(n=5)
        if inf_temp < 60:
            inf_emj = getSadnessEmj(n=5)
        self.resultInfo = " 识别结果: {} \n置信度:{}% \n {}".format(str(random.randint(1, 101)), str(inf_temp), inf_emj)
        return self.resultInfo

    def setPredictResultInfo(self, inf):
        self.updatePredictResultInfo()
        self.predictionResultBt.setText(self.resultInfo)

    def _addWidgets(self):
        self.leftLayout.addWidget(self.loadImage1Btn)
        self.leftLayout.addWidget(self.predictionResultBt)


class rightContent(QFrame):
    def __init__(self, frame: QFrame):
        super().__init__(frame)
        self.rightPanel = frame
        self.rightLayout = FlowLayout(self.rightPanel, needAni=True)
        self.imageLabel1 = DraggableImageLabel(self.rightPanel)
        self.imageLabel2 = DraggableImageLabel(self.rightPanel)
        self.imageLabel1.setCustomImage('resource/painting_girl.png')
        self.imageLabel2.setCustomImage('resource/painting_girl.png')
        self.imageLabel1.setBorderRadius(10, 10, 10, 10)
        self.imageLabel2.setBorderRadius(10, 10, 10, 10)
        self.addWidgets()

    def addWidgets(self):
        self.rightLayout.addWidget(self.imageLabel1)
        self.rightLayout.addWidget(self.imageLabel2)


class HomeInterface(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.splitter = QSplitter()
        self.leftRegion = leftContent(QFrame(self))
        self.rightRegion = rightContent(QFrame(self))
        self.setupUI()
        self.setObjectName('HomeInterface')

    def setupUI(self):
        self.stateTooltip = None
        self.splitter.addWidget(self.leftRegion.leftPanel)
        self.splitter.addWidget(self.rightRegion.rightPanel)
        self.hBoxLayout.addWidget(self.splitter)

        self.leftRegion.loadImage1Btn.clicked.connect(lambda:self.loadImage())

    def loadImage(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            f"选择一张图片进行预测",
            "./",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if len(file_path) == 0: return
        self.rightRegion.imageLabel1.setCustomImage(file_path)
        self.rightRegion.imageLabel1.zoom_factor = 1.0
        self.predictedOutputs(file_path)

    def predictedOutputs(self, file_path):
        self.ComputationDisplayCard()
        loop = QEventLoop(self)
        QTimer.singleShot(1500, loop.quit)
        loop.exec()
        self.ComputationDisplayCard()
        self.rightRegion.imageLabel2.setCustomImage(file_path)
        self.rightRegion.imageLabel2.zoom_factor = 1.0
        self.leftRegion.setPredictResultInfo(None)

    def ComputationDisplayCard(self):
        if self.stateTooltip:
            self.stateTooltip.setContent('完成啦' + getEmj())
            self.stateTooltip.setState(True)
            self.stateTooltip = None
        else:
            self.stateTooltip = StateToolTip('模型正在全力计算中' + getEmj(), '请耐心等待呦~~', self)
            self.stateTooltip.move(510, 30)
            self.stateTooltip.show()
