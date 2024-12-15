from PyQt5.QtWidgets import QFrame, QWidget, QLayout
from qfluentwidgets import TextBrowser, PushButton
from assembly.autoResizePushButton import AutoResizePushButton


class ResultDisplayCard():
    def __init__(self,widthLimit:int , frame:QFrame,):
        self.panel = frame
        self.rList = []
        self.widthLimit = widthLimit
        self.originalList = ["识别结果: 🦄","置信度: 🦄","识别用时: 🦄","x坐标: 🦄",
                             "y坐标: 🦄","宽: 🦄","高: 🦄","文件路径: 🦄"]
        self.rList.append(PushButton(self.originalList[0], self.panel))
        self.rList.append(PushButton(self.originalList[1], self.panel))
        self.rList.append(PushButton(self.originalList[2], self.panel))
        self.rList.append(PushButton(self.originalList[3], self.panel))
        self.rList.append(PushButton(self.originalList[4], self.panel))
        self.rList.append(PushButton(self.originalList[5], self.panel))
        self.rList.append(PushButton(self.originalList[6], self.panel))
        self.rList.append(AutoResizePushButton(self.widthLimit, None, self.originalList[7], self.panel, widthLimitFactor=1.0, ))

    def _showOriginal(self):
        for i in range(len(self.originalList)):
            self.rList[i].setText(self.originalList[i])

    def show(self,saveDir,rectanglePos,scores,classes,inferenceTime):
        self._showOriginal()
        ans = []
        ans.append(classes)
        ans.append(scores)
        ans.append(inferenceTime)
        ans.append(rectanglePos["x"])
        ans.append(rectanglePos["y"])
        ans.append(rectanglePos["width"])
        ans.append(rectanglePos["height"])
        ans.append(saveDir)
        if len(ans)!=len(self.rList):
            print("显示信息出现问题")
            return
        for i in range(len(self.rList)):
            new_inf = self.rList[i].text().replace("🦄",str(ans[i]))
            print(new_inf)
            self.rList[i].setText(new_inf)

    def addwidget(self,layout:QLayout):
        for r in self.rList:
            layout.addWidget(r)