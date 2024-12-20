import time

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QLayout
from qfluentwidgets import PushButton, InfoBar, InfoBarPosition
from assembly.autoResizePushButton import AutoResizePushButton
from assembly.common import getEmj, getSadnessEmj


class ResultDisplayCard():
    def __init__(self, widthLimit: int, frame: QFrame, ):
        self.panel = frame
        self.rList = []
        self.widthLimit = widthLimit
        self._setOriginalList()
        self.rList.append(PushButton(self.originalList[0], self.panel))
        self.rList.append(PushButton(self.originalList[1], self.panel))
        self.rList.append(PushButton(self.originalList[2], self.panel))
        self.rList.append(PushButton(self.originalList[3], self.panel))
        self.rList.append(PushButton(self.originalList[4], self.panel))
        self.rList.append(PushButton(self.originalList[5], self.panel))
        self.rList.append(PushButton(self.originalList[6], self.panel))
        self.rList.append(
            AutoResizePushButton(self.widthLimit, None, self.originalList[7], self.panel, widthLimitFactor=1.0, ))

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

    def _showOriginal(self):
        self._setOriginalList()
        for i in range(len(self.originalList)):
            self.rList[i].setText(self.originalList[i])

    def show(self, saveDir, rectanglePos, scores, classes, inferenceTime):
        self._showOriginal()
        scores = scores if scores is not None else ""
        classes = classes if classes is not None else ""
        ans = [classes, scores, inferenceTime]
        if rectanglePos is not None:
            ans.extend([rectanglePos["x"], rectanglePos["y"], rectanglePos["width"], rectanglePos["height"]])
        else:
            ans.extend(["", "", "", ""])
        ans.append(saveDir)
        try:
            for i in range(len(self.rList)):
                tempStr = self.rList[i].text()
                new_inf = self._replace_last_occurrence(tempStr, tempStr[-1], str(ans[i]))
                self.rList[i].setText(new_inf)
        except Exception as e:
            InfoBar.warning(
                title='警告',
                content="数据" + getSadnessEmj() + "\n匹配出现错误",
                orient=Qt.Horizontal,
                isClosable=True,  # disable close button
                position=InfoBarPosition.TOP_LEFT,
                duration=20000,
                parent=self.panel
            )

    def _replace_last_occurrence(self, s, old, new):
        return s.rsplit(old, 1)[0] + new + s.rsplit(old, 1)[1]

    def addwidget(self, layout: QLayout):
        for r in self.rList:
            layout.addWidget(r)
