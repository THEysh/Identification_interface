import time

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QLayout
from qfluentwidgets import PushButton, InfoBar, InfoBarPosition
from assembly.autoResizePushButton import AutoResizePushButton
from assembly.common import getEmj, getSadnessEmj


def _replace_last_occurrence(s, old, new):
    parts = s.rsplit(old, 1)  # 从右边分割字符串，最多分割一次
    if len(parts) == 1:
        return s  # 如果没有找到 old，直接返回原字符串
    return parts[0] + new + parts[1]  # 替换最后一次出现的 old


class ResultDisplayCard():
    def __init__(self, widthLimit: int, frame: QFrame, ):
        self.panel = frame
        self.rList = []
        self.widthLimit = widthLimit
        # 保留几位小数
        self.roundNumber = 2
        self._setOriginalList()
        self.CoordinatePointBtn = PushButton("位置: "+ getEmj() + " ", self.panel)
        self.rList.append(PushButton(self.originalList[0], self.panel))
        self.rList.append(PushButton(self.originalList[1], self.panel))
        self.rList.append(PushButton(self.originalList[2], self.panel))
        self.rList.append(PushButton(self.originalList[3], self.panel))
        self.rList.append(PushButton(self.originalList[4], self.panel))
        self.rList.append(PushButton(self.originalList[5], self.panel))
        self.rList.append(PushButton(self.originalList[6], self.panel))
        self.rList.append(AutoResizePushButton(self.widthLimit, None,
                                               self.originalList[7],
                                               self.panel,
                                               widthLimitFactor=1.0, ))

    def _setOriginalList(self):
        self.originalList = ["识别结果: " + getEmj() + " ",
                             "置信度: " + getEmj() + " ",
                             "识别用时: " + getEmj() + " ",
                             "x坐标: " + getEmj() + " ",
                             "y坐标: " + getEmj() + " ",
                             "宽: " + getEmj() + " ",
                             "高: " + getEmj() + " ",
                             "文件路径: " + getEmj() + " ",
                             ]

    def dataProcess(self, num:float):
        newNum = round(num,self.roundNumber)
        return str(newNum)

    def _showOrgCoordinatePoint(self, CoordinatePoint):
        new_tuple = tuple(item + 1 for item in CoordinatePoint)
        self.CoordinatePointBtn.setText("位置: " + getEmj() + str(new_tuple))

    def show(self, saveDir, rectanglePos, scores, classes, inferenceTime, CoordinatePoint= None):
        if CoordinatePoint is not None:
            self._showOrgCoordinatePoint(CoordinatePoint)
        scores = self.dataProcess(float(scores*100)) + "%" if scores is not None else ""
        classes = self.dataProcess(float(inferenceTime)) if classes is not None else ""
        ans = [classes, scores, inferenceTime]
        if rectanglePos is not None:
            x = self.dataProcess(float(rectanglePos["x"]))
            y = self.dataProcess(float(rectanglePos["y"]))
            width = self.dataProcess(float(rectanglePos["width"]))
            heght = self.dataProcess(float(rectanglePos["height"]))
            ans.extend([x, y, width, heght])
        else:
            ans.extend(["", "", "", ""])
        ans.append(saveDir)
        try:
            for i in range(len(self.originalList)):
                tempStr = self.originalList[i]
                new_inf = _replace_last_occurrence(tempStr, " ", str(ans[i]))
                self.rList[i].setText(new_inf)
        except Exception as e:
            InfoBar.warning(
                title='警告',
                content="数据" + getSadnessEmj() + "\n匹配出现错误" + str(e),
                orient=Qt.Horizontal,
                isClosable=True,  # disable close button
                position=InfoBarPosition.TOP_LEFT,
                duration=2000,
                parent=self.panel
            )

    def orgShow(self,path, CoordinatePoint):
        self._showOrgCoordinatePoint(CoordinatePoint)
        for i in range(len(self.originalList)):
            # 如果是文件路径的情况（最后一个）：
            if i==len(self.originalList)-1:
                tempStr = self.originalList[i]
                new_inf = _replace_last_occurrence(tempStr, " ", str(path))
            else:
                new_inf = self.originalList[i]
            self.rList[i].setText(new_inf)

    def addwidget(self, layout: QLayout, isAddCoordinatePointBtn=False):
        layout.addWidget(self.CoordinatePointBtn)
        if isAddCoordinatePointBtn is False:
            self.CoordinatePointBtn.hide()
        for r in self.rList:
            layout.addWidget(r)