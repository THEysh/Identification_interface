from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGridLayout, QWidget
from qfluentwidgets import PushButton, ImageLabel
from assembly.autoResizePushButton import AutoResizePushButton
from assembly.clockShow import ClockShow
from assembly.common import getEmj, path_to_absolute, roundToR, checkFloat, checkInt
from qfluentwidgets import FluentIcon as FIF
RoundNumber = 2

def processPreResDict(redDict: dict):
    if redDict['path'] is not None:
        path_str = path_to_absolute(redDict['path'])
    else:
        path_str = ''
    if redDict['rectangle_pos'] is not None:
        x_float_or_str = round(float(redDict['rectangle_pos']['x']), RoundNumber)
        y_float_or_str = round(float(redDict['rectangle_pos']['y']), RoundNumber)
        width_float_or_str = round(float(redDict['rectangle_pos']['width']), RoundNumber)
        height_float_or_str = round(float(redDict['rectangle_pos']['height']), RoundNumber)
    else:
        x_float_or_str = ''
        y_float_or_str = ''
        width_float_or_str = ''
        height_float_or_str = ''
    if redDict['scores'] is not None:
        conf_str = roundToR(float(redDict['scores']) * 100, r=RoundNumber)
    else:
        conf_str = ''
    if redDict['classes'] is not None:
        classes_str = redDict['classes']
    else:
        classes_str = ''
    if redDict['inference_time'] is not None:
        runtime_str = roundToR(float(redDict['inference_time']), RoundNumber)
    else:
        runtime_str = ''
    return (path_str, x_float_or_str, y_float_or_str, width_float_or_str, height_float_or_str,
            conf_str, classes_str, runtime_str)


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
        self.roundNumber = RoundNumber
        self.ImgDetectorBtn = PushButton("识别结果: " + getEmj() + " ", self.panel)
        self.cropImgLabel = ImageLabel()
        self.cropped_pixmap = None # 用于显示裁剪的图片
        self.cropImgLabel.setVisible(False)
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

    def reset(self):
        self.CoordinatePointBtn.setVisible(False)
        self.cropImgLabel.setVisible(False)
        self.setImgDetectorBtnText("")
        self.setConfBtnText("")
        self.setRunTimeBtnText("")
        self.setXBtnText("")
        self.setYBtnText("")
        self.setWidthBtnText("")
        self.setHeightBtnText("")
        self.setPathBtnText("")
        self.folderInfoBtn.setVisible(False)

    def dataProcess(self, num:float, r = None):
        if r is None:
            r = self.roundNumber
        newNum = round(num, r )
        return str(newNum)

    def displayOriginalDir(self,originalDir):
        originalDir = path_to_absolute(originalDir)
        self.folderInfoBtn.setText("原始图文件夹: " + getEmj() + " " + originalDir)
        self.folderInfoBtn.setVisible(True)

    def preShow(self, redDict:dict):
        self.CoordinatePointBtn.setVisible(True)
        (path_str, x_float_or_str, y_float_or_str, width_float_or_str, height_float_or_str,
         conf_str, classes_str, runtime_str) = processPreResDict(redDict)
        self.setPathBtnText(path_str)
        if (checkFloat(x_float_or_str) and
            checkFloat(y_float_or_str) and
            checkFloat(width_float_or_str) and
            checkFloat(height_float_or_str)):
            # 数据是float:
            self.cropImgLabel.setVisible(True)
            self.setXBtnText(str(x_float_or_str))
            self.setYBtnText(str(y_float_or_str))
            self.setWidthBtnText(str(width_float_or_str))
            self.setHeightBtnText(str(height_float_or_str))
            if redDict['pixmap'] is not None:
                self.cropPreImage(redDict['pixmap'],x_float_or_str,y_float_or_str,
                                  width_float_or_str,height_float_or_str)
        else:
            self.cropImgLabel.setVisible(False)
            self.setXBtnText('')
            self.setYBtnText('')
            self.setWidthBtnText('')
            self.setHeightBtnText('')
        self.setConfBtnText(conf_str)
        self.setImgDetectorBtnText(classes_str)
        self.setRunTimeBtnText(runtime_str)
        if 'row' in redDict:
            self.setCoordinatePointBtnText((int(redDict['row']), 1))
        else:
            self.setCoordinatePointBtnText('')

    def cropPreImage(self,pixmap:QPixmap, x:float, y:float, width:float, height:float):
        if pixmap:
            # 根据尺寸截取图片
            self.cropped_pixmap = pixmap.copy(x, y, width, height)
            # 显示截取的图片
            self.cropImgLabel.setPixmap(self.cropped_pixmap)

    def cropPreImagePath(self, image_path: str, x: float, y: float, width: float, height: float):
        try:
            pixmap = QPixmap(image_path)
        except:
            return
        if not pixmap.isNull():
            # 根据尺寸截取图片
            self.cropped_pixmap = pixmap.copy(x, y, width, height)
            # 显示截取的图片
            self.cropImgLabel.setPixmap(self.cropped_pixmap)
        else:
            print("Error: Invalid image path")

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
            path = path_to_absolute(resDic['path'])
            self.setPathBtnText(path)
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
            savePath = path_to_absolute(savePath)
            self.setPathBtnText(savePath)
        else:
            self.setPathBtnText('')
        if rectanglePosDict is not None:
            x = float(rectanglePosDict['x'])
            y = float(rectanglePosDict['y'])
            width = float(rectanglePosDict['width'])
            height = float(rectanglePosDict['height'])
            self.cropImgLabel.setVisible(True)
            self.cropPreImagePath(savePath,x,y,width,height)
            x = self.dataProcess(float(x))
            y = self.dataProcess(float(y))
            width = self.dataProcess(float(width))
            height = self.dataProcess(float(height))
            self.setXBtnText(x)
            self.setYBtnText(y)
            self.setWidthBtnText(width)
            self.setHeightBtnText(height)
        else:
            self.cropImgLabel.setVisible(False)
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