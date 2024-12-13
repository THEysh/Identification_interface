import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QEasingCurve
from qfluentwidgets import SmoothScrollArea, ImageLabel


class Demo(SmoothScrollArea):

    def __init__(self):
        super().__init__()
        # 加载一张分辨率很高的图片
        self.label = ImageLabel("resource/painting_girl.png")

        # 自定义平滑滚动动画
        self.setScrollAnimation(Qt.Vertical, 400, QEasingCurve.OutQuint)
        self.setScrollAnimation(Qt.Horizontal, 400, QEasingCurve.OutQuint)

        # 滚动到指定区域
        self.horizontalScrollBar().setValue(1900)

        self.setWidget(self.label)
        self.resize(1200, 800)


def main():
    app = QApplication(sys.argv)

    # 创建主窗口
    window = QWidget()
    window.setWindowTitle("PyQt5 Smooth Scroll Demo")
    window.setGeometry(100, 100, 1200, 800)

    # 创建布局
    layout = QVBoxLayout()
    window.setLayout(layout)

    # 创建并添加 Demo 实例
    demo = Demo()
    layout.addWidget(demo)

    # 显示主窗口
    window.show()

    # 运行应用程序
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
