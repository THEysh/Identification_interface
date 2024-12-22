# coding:utf-8
import sys
from PyQt5.QtCore import Qt, QEventLoop, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout
from qfluentwidgets import (NavigationItemPosition, MessageBox, FluentWindow,
                            NavigationAvatarWidget, SubtitleLabel, setFont,SplashScreen)
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow import StandardTitleBar
from HomeInterface import HomeInterface
from FolderInterface import FolderInterface
from TableInterface import TableInterface
from YoloMod import YoloModel
from assembly.DataInfo import DataInfo


class Widget(QFrame):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)
        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))


class Window(FluentWindow):
    def __init__(self):
        super().__init__()
        self.splashScreen = None
        self.load()

    def initNavigation(self):
        self.yoloMod = YoloModel()
        self.datainfo = DataInfo()
        self.homeInterface = HomeInterface(self.yoloMod, datainfo = self.datainfo, parent=self)
        self.folderInterface = FolderInterface(self.yoloMod, datainfo =self.datainfo, parent=self)
        self.TableInterface = TableInterface(datainfo = self.datainfo, parent=self)
        # self.settingInterface = Widget('Setting Interface', self)
        self.addSubInterface(self.homeInterface, FIF.HOME, '欢迎回来')
        self.addSubInterface(self.folderInterface, FIF.FOLDER, '文件夹')
        self.addSubInterface(self.TableInterface, FIF.LABEL, "预测记录")
        # add custom widget to bottom
        self.navigationInterface.addWidget(
            routeKey='avatar',
            widget=NavigationAvatarWidget('HELLO', 'resource/logo.png'),
            onClick=self.showMessageBox,
            position=NavigationItemPosition.BOTTOM,
        )
        # self.addSubInterface(self.settingInterface, FIF.SETTING, '设置', NavigationItemPosition.BOTTOM)

    def load(self):
        # 1. 创建启动页面
        self.resize(900, 700)
        self.setWindowIcon(QIcon('resource/logo.png'))
        self.setWindowTitle('基于多级注意力特征融合的YOLO11模型铸字识别检测系统设计')
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.splashScreen = SplashScreen(self.windowIcon(), self, enableShadow=False)
        titleBar = StandardTitleBar(self.splashScreen)
        titleBar.setIcon(self.windowIcon())
        titleBar.setTitle(self.windowTitle())
        self.splashScreen.setTitleBar(titleBar)
        # 2. 在创建其他子页面前先显示主界面
        self.show()
        # 2-1 加载页面
        self.initNavigation()
        loop = QEventLoop(self)
        QTimer.singleShot(1500, loop.quit)
        loop.exec()
        # 4. 隐藏启动页面
        self.splashScreen.finish()

    def showMessageBox(self):
        w = MessageBox(
            '🥰AI铸字识别',
            '古代铸字历史悠久，铸字艺术独具特色，例如青铜器、陶瓷器、度量衡器等上面都有铸字。这些铸字不仅代表着当时的文字形式，也蕴含着丰富的历史文化信息。🥤。'
            '古代铸字历史悠久，铸字艺术独具特色，例如青铜器、陶瓷器、度量衡器等上面都有铸字。这些铸字不仅代表着当时的文字形式，也蕴含着丰富的历史文化信息。🚀',
            self
        )
        w.yesButton.setText('科技引领进步')
        w.cancelButton.setText('科技引领进步')

        if w.exec():
            pass


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    # setTheme(Theme.DARK)

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec_()