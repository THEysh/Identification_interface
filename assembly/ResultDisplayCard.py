from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFrame, QLayout, QGridLayout, QWidget
from qfluentwidgets import PushButton, InfoBar, InfoBarPosition, ImageLabel
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
        self.ImgDetectorBtn = PushButton("识别结果: " + getEmj() + " ", self.panel)
        self.cropImgLabel = ImageLabel()
        self.cropped_pixmap = None # 用于显示裁剪的图片
        self.cropImgLabel.setVisible(True)
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
                                                  FIF.FOLDER, getEmj() + "未选择 ", self.panel,widthLimitFactor=1.0)
        self.folderInfoBtn.setVisible(False)
        self.CoordinatePointBtn = PushButton("位置: "+ getEmj() + " ", self.panel)
        self.CoordinatePointBtn.setVisible(False)
        self.timeClock = ClockShow(self.panel)
        # 创建布局
        self.layout = QGridLayout(self)
        # 将控件添加到布局中
        self.layout.addWidget(self.ImgDetectorBtn, 0, 0, 1, 1)
        self.layout.addWidget(self.cropImgLabel, 0, 2, 2, 2)
        self.layout.addWidget(self.xBtn, 2, 0)
        self.layout.addWidget(self.yBtn, 2, 2)
        self.layout.addWidget(self.widthBtn, 3, 0)
        self.layout.addWidget(self.heightBtn, 3, 2)
        # 位置信息文本
        self.layout.addWidget(self.confBtn, 4, 0)
        self.layout.addWidget(self.runTimeBtn, 4, 2)
        self.layout.addWidget(self.pathBtn, 5, 0, 1, 3)  # 横跨3列
        self.layout.addWidget(self.folderInfoBtn, 6, 0, 1, 3)
        self.layout.addWidget(self.CoordinatePointBtn, 7, 0)
        self.layout.addWidget(self.timeClock, 8, 0, 1, 2)

        # 设置组件布局
        self.setLayout(self.layout)

    def dataProcess(self, num:float, r = None):
        if r is None:
            r = self.roundNumber
        newNum = round(num, r )
        return str(newNum)

    def displayOriginalDir(self,originalDir):
        self.folderInfoBtn.setText("原始图文件夹: " + getEmj() + " " + originalDir)
        self.folderInfoBtn.setVisible(True)

    def preShow(self, redDict:dict):
        self.CoordinatePointBtn.setVisible(True)
        if redDict['path'] is not None:
            self.setPathBtnText(redDict['path'])
        else:
            self.setPathBtnText('')
        if redDict['rectangle_pos'] is not None:
            self.cropImgLabel.setVisible(True)
            x_float = float(redDict['rectangle_pos']['x'])
            y_float = float(redDict['rectangle_pos']['y'])
            width_float = float(redDict['rectangle_pos']['width'])
            height_float = float(redDict['rectangle_pos']['height'])
            x = self.dataProcess(x_float)
            y = self.dataProcess(y_float)
            width = self.dataProcess(width_float)
            height = self.dataProcess(height_float)
            self.setXBtnText(x)
            self.setYBtnText(y)
            self.setWidthBtnText(width)
            self.setHeightBtnText(height)
            self.cropPreImage(redDict['pixmap'],x_float,y_float,width_float,height_float)
        else:
            self.cropImgLabel.setVisible(False)
            self.setXBtnText('')
            self.setYBtnText('')
            self.setWidthBtnText('')
            self.setHeightBtnText('')
        if redDict['scores'] is not None:
            str_conf = self.dataProcess(float(redDict['scores'])*100)
            self.setConfBtnText(str_conf)
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

    def cropPreImage(self,pixmap:QPixmap, x:float, y:float, width:float, height:float):
        if pixmap:
            # 根据尺寸截取图片
            self.cropped_pixmap = pixmap.copy(x, y, width, height)
            # 显示截取的图片
            self.cropImgLabel.setPixmap(self.cropped_pixmap)


    def orgShow(self,resDic:dict):
        self.CoordinatePointBtn.setVisible(True)
        self.cropImgLabel.setVisible(False)
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
            str_conf = self.dataProcess(float(scores)*100)
            self.setConfBtnText(str_conf)

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
        if len(text)>=1:
            self.confBtn.setText("置信度: " + getEmj() + " " + text + "%")
        else:
            self.confBtn.setText("置信度: " + getEmj())

    def getRunTimeBtnText(self) -> str:
        return self.runTimeBtn.text()

    def setRunTimeBtnText(self, text: str):
        if len(text)>=1:
            self.runTimeBtn.setText("识别用时: " + getEmj() + " " + text + "ms")
        else:
            self.runTimeBtn.setText("识别用时: " + getEmj())

    def getXBtnText(self) -> str:
        return self.xBtn.text()

    def setXBtnText(self, text: str):
        if len(text)>=1:
            self.xBtn.setText("x: " + getEmj() + " " + text + "px")
        else:
            self.xBtn.setText("x: " + getEmj())

    def getYBtnText(self) -> str:
        return self.yBtn.text()

    def setYBtnText(self, text: str):
        if len(text)>=1:
            self.yBtn.setText("y: " + getEmj() + " " + text + "px")
        else:
            self.yBtn.setText("y: " + getEmj())

    def getWidthBtnText(self) -> str:
        return self.widthBtn.text()

    def setWidthBtnText(self, text: str):
        if len(text)>=1:
            self.widthBtn.setText("宽: " + getEmj() + " " + text + "px")
        else:
            self.widthBtn.setText("宽: " + getEmj())

    def getHeightBtnText(self) -> str:
        return self.heightBtn.text()

    def setHeightBtnText(self, text: str):
        if len(text)>=1:
            self.heightBtn.setText("高: " + getEmj() + " " + text + "px")
        else:
            self.heightBtn.setText("高: " + getEmj())

    def getPathBtnText(self) -> str:
        return self.pathBtn.text()

    def setPathBtnText(self, text: str):
        self.pathBtn.setText("图路径: " + getEmj() + " " + text)