import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QThread, pyqtSignal
import time

class ImageLoaderThread(QThread):
    image_loaded = pyqtSignal(QImage)
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):
        time.sleep(1)  # 模拟加载延迟
        try:
            image = QImage(self.file_path)
            if not image.isNull():
                self.image_loaded.emit(image)
            else:
                print("Failed to load image")
        except Exception as e:
            print(f"Error: {e}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("异步加载本地图片示例")
        self.setGeometry(100, 100, 800, 600)

        self.label = QLabel(self)
        self.label.setGeometry(100, 100, 600, 400)

        self.button = QPushButton("加载图片", self)
        self.button.setGeometry(350, 50, 100, 30)
        self.button.clicked.connect(self.load_image)

        self.image_loader = None

    def load_image(self):
        if self.image_loader is not None and self.image_loader.isRunning():
            return

        file_path = "resource/painting_girl.png"  # 替换为你的本地图片路径
        self.image_loader = ImageLoaderThread(file_path)
        self.image_loader.image_loaded.connect(self.show_image)
        self.image_loader.start()

    def show_image(self, image):
        pixmap = QPixmap.fromImage(image)
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
