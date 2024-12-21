from PyQt5.QtCore import Qt
from qfluentwidgets import StateToolTip, InfoBar, InfoBarPosition
from assembly.common import getEmj, getSadnessEmj


class InfoDisplayCards:
    def __init__(self, parent):
        self.parent = parent
        self._stateLoadImg = None
        self._predictStatus = None

    def _getParent(self, parent):
        if parent is None:
            parent = self.parent
        return parent
    def InfoPredictProcessingSuccess(self, parent=None):
        InfoBar.success(
            title='成功',
            content="所有图片已全部预测" + getEmj(),
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            # position='Custom',   # NOTE: use custom info bar manager
            duration=2000,
            parent=parent
        )

    def InfoPredictProcessingwarning(self, parent):
        InfoBar.warning(
            title='警告',
            content="当前文件夹为空 " + getSadnessEmj(),
            orient=Qt.Horizontal,
            isClosable=False,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=parent
        )

    def InfoSetThreadCountSuccess(self, parent=None):
        InfoBar.success(
            title='成功',
            content="线程数目设置成功 " + getEmj(),
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            # position='Custom',   # NOTE: use custom info bar manager
            duration=2000,
            parent=parent
        )

    def InfoSetThreadCountWarning(self, parent=None):
        InfoBar.warning(
            title='警告',
            content="当前不可设置线程数目 " + getSadnessEmj(),
            orient=Qt.Horizontal,
            isClosable=False,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=parent
        )

    def InfoBarErr(self, infStr=None, parent=None):
        # infDict 是个字典,传入有index的key
        parent = self._getParent(parent)
        if infStr is None:
            content = "此图的预测结果尚未确定"
        else:
            content = infStr
        InfoBar.warning(
            title='警告',
            content=content,
            orient=Qt.Horizontal,
            isClosable=False,
            position=InfoBarPosition.BOTTOM_LEFT,
            duration=750,
            parent=parent
        )

    def InfoSignalThread(self,instr:str, parent=None, ):
        InfoBar.error(
            title='错误',
            content=instr,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_LEFT,
            duration=-1,
            parent=parent
        )

    def InfoBarManualStop(self, parent=None):
        parent = self._getParent(parent)
        InfoBar.error(
            title='错误',
            content="手动终止",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_LEFT,
            duration=-1,
            parent=parent
        )

    def computationLoadImageCard(self, parent=None):
        parent = self._getParent(parent)
        if self._stateLoadImg:
            self._stateLoadImg.setContent('结束啦~' + getEmj())
            self._stateLoadImg.setState(True)
            self._stateLoadImg = None
        else:
            self._stateLoadImg = StateToolTip('正在全力加载图片' + getEmj(), '心急吃不了热豆腐~请耐心等待呦~~', parent)
            self._stateLoadImg.move(510, 30)
            self._stateLoadImg.show()

    def computationPredictCard(self, parent=None):
        parent = self._getParent(parent)
        if self._predictStatus:
            self._predictStatus.setContent('结束啦~' + getEmj())
            self._predictStatus.setState(True)
            self._predictStatus = None
        else:
            self._predictStatus = StateToolTip('模型正在全力计算中' + getEmj(), '心急吃不了热豆腐~请耐心等待呦~~',
                                               parent)
            self._predictStatus.move(510, 30)
            self._predictStatus.show()
