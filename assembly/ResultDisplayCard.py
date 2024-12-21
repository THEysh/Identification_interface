import time

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QLayout, QGridLayout, QWidget
from qfluentwidgets import PushButton, InfoBar, InfoBarPosition
from assembly.autoResizePushButton import AutoResizePushButton
from assembly.clockShow import ClockShow
from assembly.common import getEmj, getSadnessEmj
from qfluentwidgets import FluentIcon as FIF

def _replace_last_occurrence(s, old, new):
    parts = s.rsplit(old, 1)  # 从右边分割字符串，最多分割一次
    if len(parts) == 1:
        return s  # 如果没有找到 old，直接返回原字符串
    return parts[0] + new + parts[1]  # 替换最后一次出现的 old



class ResultDisplayCard(QWidget):
    def __init__(self, widthLimit: int, parent: QWidget = None):
        super().__init__(parent)
        self.panel = parent
        self.widthLimit = widthLimit
        # 保留几位小数
        self.roundNumber = 2
        self.CoordinatePointBtn = PushButton("位置: "+ getEmj() + " ", self.panel)
        self.ImgDetectorBtn = PushButton("识别结果: " + getEmj() + " ", self.panel)
        self.confBtn = PushButton("置信度: " + getEmj() + " ", self.panel)
        self.runTimeBtn = PushButton("识别用时: " + getEmj() + " ", self.panel)
        self.xBtn = PushButton("x坐标: " + getEmj() + " ", self.panel)
        self.yBtn = PushButton("y坐标: " + getEmj() + " ", self.panel)
        self.widthBtn = PushButton("宽: " + getEmj() + " ", self.panel)
        self.heightBtn = PushButton("高: " + getEmj() + " ", self.panel)
        self.pathBtn = AutoResizePushButton(self.widthLimit, FIF.PHOTO,
                                            "图路径: " + getEmj() + " ",self.panel, widthLimitFactor=1.0)
        # 原图文件夹
        self.folderInfoBtn = AutoResizePushButton(self.widthLimit,
                                                  FIF.FOLDER, " 未选择 ", self.panel,widthLimitFactor=1.0)
        self.folderInfoBtn.setVisible(False)
        self.timeClock = ClockShow(self.panel)
        # 创建布局
        self.layout = QGridLayout(self)
        # 将控件添加到布局中
        self.layout.addWidget(self.CoordinatePointBtn, 0, 0)
        self.layout.addWidget(self.ImgDetectorBtn, 0, 2)
        self.layout.addWidget(self.xBtn, 1, 0)
        self.layout.addWidget(self.yBtn, 1, 2)
        self.layout.addWidget(self.widthBtn, 2, 0)
        self.layout.addWidget(self.heightBtn, 2, 2)
        # 位置信息文本
        self.layout.addWidget(self.confBtn, 3, 0)
        self.layout.addWidget(self.runTimeBtn, 3, 2)
        self.layout.addWidget(self.pathBtn, 4, 0, 1, 3)  # 横跨3列
        self.layout.addWidget(self.folderInfoBtn, 5, 0, 1, 3)
        self.layout.addWidget(self.timeClock, 6, 0, 1, 2)
        # 设置组件布局
        self.setLayout(self.layout)

    def dataProcess(self, num:float, r = None):
        if r is None:
            r = self.roundNumber
        newNum = round(num, r )
        return str(newNum)

    def displayOriginalDir(self,originalDir):
        self.folderInfoBtn.setText(f"原始图文件夹: {originalDir}")
        self.folderInfoBtn.setVisible(True)

    def preShow(self, redDict:dict):
        if redDict['path'] is not None:
            self.setPathBtnText(redDict['path'])
        else:
            self.setPathBtnText('')
        if redDict['rectangle_pos'] is not None:
            x = self.dataProcess(float(redDict['rectangle_pos']['x']))
            y = self.dataProcess(float(redDict['rectangle_pos']['y']))
            width = self.dataProcess(float(redDict['rectangle_pos']['width']))
            height = self.dataProcess(float(redDict['rectangle_pos']['height']))
            self.setXBtnText(x)
            self.setYBtnText(y)
            self.setWidthBtnText(width)
            self.setHeightBtnText(height)
        else:
            self.setXBtnText('')
            self.setYBtnText('')
            self.setWidthBtnText('')
            self.setHeightBtnText('')
        if redDict['scores'] is not None:
            conf = self.dataProcess(float(redDict['scores']))
            self.setConfBtnText(conf)
        else:
            self.setConfBtnText('')
        if redDict['classes'] is not None:
            classes = redDict['classes']
            self.setImgDetectorBtnText(classes)
        else:
            self.setImgDetectorBtnText('')
        if redDict['inference_time'] is not None:
            runtime = self.dataProcess(float(redDict['inference_time']), r=0)
            self.setRunTimeBtnText(runtime)
        else:
            self.setRunTimeBtnText('')
        if redDict['row'] is not None:
            row = int(redDict['row'])
            self.setCoordinatePointBtnText((row,1))
        else:
            self.setCoordinatePointBtnText('')

    def orgShow(self,resDic:dict):
        try:
            self.setCoordinatePointBtnText((resDic['row'],resDic['col']))
        except:
            self.setCoordinatePointBtnText('')
        self.setImgDetectorBtnText("")
        self.setConfBtnText("")
        self.setRunTimeBtnText("")
        self.setXBtnText("")
        self.setYBtnText("")
        self.setWidthBtnText("")
        self.setHeightBtnText("")
        try:
            self.setPathBtnText(resDic['path'])
        except:
            self.setPathBtnText('')

    def homeShow(self, savePath, rectanglePosDict, scores, classes, inferenceTime):
        if inferenceTime is not None:
            self.setRunTimeBtnText(self.dataProcess(float(inferenceTime), 0))
        else:
            self.setRunTimeBtnText('')
        if classes is not None:
            self.setImgDetectorBtnText(classes)
        else:
            self.setImgDetectorBtnText('')
        if scores is not None:
            self.setConfBtnText(self.dataProcess(float(scores)))
        else:
            self.setConfBtnText('')
        if savePath is not None:
            self.setPathBtnText(savePath)
        else:
            self.setPathBtnText('')

        if rectanglePosDict is not None:
            x = self.dataProcess(float(rectanglePosDict['x']))
            y = self.dataProcess(float(rectanglePosDict['y']))
            width = self.dataProcess(float(rectanglePosDict['width']))
            height = self.dataProcess(float(rectanglePosDict['height']))
            self.setXBtnText(x)
            self.setYBtnText(y)
            self.setWidthBtnText(width)
            self.setHeightBtnText(height)
        else:
            self.setXBtnText('')
            self.setYBtnText('')
            self.setWidthBtnText('')
            self.setHeightBtnText('')

    def getCoordinatePointBtnText(self) -> str:
        return self.CoordinatePointBtn.text()

    def setCoordinatePointBtnText(self, CoordinatePoint):
        if CoordinatePoint == '':
            self.CoordinatePointBtn.setText("位置: " + getEmj())
        else:
            new_tuple = tuple(item + 1 for item in CoordinatePoint)
            self.CoordinatePointBtn.setText("位置: " + getEmj() + str(new_tuple))

    def getImgDetectorBtnText(self) -> str:
        return self.ImgDetectorBtn.text()

    def setImgDetectorBtnText(self, text: str):
        self.ImgDetectorBtn.setText("识别结果: " + getEmj() + " " + text)

    def getConfBtnText(self) -> str:
        return self.confBtn.text()

    def setConfBtnText(self, text: str):
        self.confBtn.setText("置信度: " + getEmj() + " " + text)

    def getRunTimeBtnText(self) -> str:
        return self.runTimeBtn.text()

    def setRunTimeBtnText(self, text: str):
        self.runTimeBtn.setText("识别用时: " + getEmj() + " " + text + "ms")

    def getXBtnText(self) -> str:
        return self.xBtn.text()

    def setXBtnText(self, text: str):
        self.xBtn.setText("x: " + getEmj() + " " + text)

    def getYBtnText(self) -> str:
        return self.yBtn.text()

    def setYBtnText(self, text: str):
        self.yBtn.setText("y: " + getEmj() + " " + text)

    def getWidthBtnText(self) -> str:
        return self.widthBtn.text()

    def setWidthBtnText(self, text: str):
        self.widthBtn.setText("宽: " + getEmj() + " " + text)

    def getHeightBtnText(self) -> str:
        return self.heightBtn.text()

    def setHeightBtnText(self, text: str):
        self.heightBtn.setText("高: " + getEmj() + " " + text)

    def getPathBtnText(self) -> str:
        return self.pathBtn.text()

    def setPathBtnText(self, text: str):
        self.pathBtn.setText("图路径: " + getEmj() + " " + text)