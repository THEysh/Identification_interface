import sys
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread, pyqtSignal, Qt


# 异步加载图片的线程
class LoadImageThread(QThread):
    image_loaded = pyqtSignal(QPixmap)
    def __init__(self, path, parent=None):
        super().__init__(parent)
        self.path = path
    def run(self):
        # 加载图片
        pixmap = QPixmap(self.path)
        if not pixmap.isNull():
            # 图片加载成功，触发信号
            self.image_loaded.emit(pixmap)
        else:
            # 图片加载失败，可以触发一个错误信号
            print(f"Failed to load image from {self.path}")

# 主窗口类
class MainWindow(QMainWindow):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.image_path = image_path
        self.initUI()
        self.start_loading()

    def initUI(self):
        self.setWindowTitle("Async Image Loader")
        self.setGeometry(100, 100, 400, 300)

        # 创建一个QLabel用来显示图片
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        # 创建一个布局，并添加QLabel
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)

        # 创建一个中心窗口，并设置布局
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def start_loading(self):
        # 创建并启动加载图片的线程
        self.load_thread = LoadImageThread(self.image_path)
        self.load_thread.image_loaded.connect(self.display_image)
        self.load_thread.start()

    def display_image(self, pixmap):
        # 在主线程中显示图片
        self.image_label.setPixmap(pixmap)
        self.image_label.adjustSize()

# 主函数
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 图片路径
    image_path = "resource/painting_girl.png"

    mainWin = MainWindow(image_path)
    mainWin.show()

    sys.exit(app.exec_())
