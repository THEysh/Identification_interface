import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from PIL import Image

class ImageCropper(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Image Cropper')
        self.setGeometry(100, 100, 800, 600)

        self.label = QLabel(self)
        self.label.setGeometry(10, 10, 780, 540)
        self.label.setAlignment(Qt.AlignCenter)

        self.button = QPushButton('Load Image', self)
        self.button.setGeometry(10, 560, 100, 30)
        self.button.clicked.connect(self.loadImage)

        self.crop_button = QPushButton('Crop Image', self)
        self.crop_button.setGeometry(120, 560, 100, 30)
        self.crop_button.clicked.connect(self.cropImage)

        self.save_button = QPushButton('Save Cropped Image', self)
        self.save_button.setGeometry(230, 560, 150, 30)
        self.save_button.clicked.connect(self.saveCroppedImage)

        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0

    def loadImage(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Images (*.png *.xpm *.jpg *.bmp *.gif)", options=options)
        if file_name:
            self.image = Image.open(file_name)
            self.label.setPixmap(QPixmap.fromImage(self.pilToQImage(self.image)))

    def pilToQImage(self, image):
        data = image.convert("RGBA").tobytes("raw", "RGBA")
        qimage = QImage(data, image.width, image.height, QImage.Format_RGBA8888)
        return qimage

    def cropImage(self):
        if self.image:
            # YOLO 返回的尺寸 (x, y, width, height)
            x = self.x
            y = self.y
            width = self.width
            height = self.height
            # 根据尺寸截取图片
            self.cropped_image = self.image.crop((x, y, x + width, y + height))
            # 显示截取的图片
            self.label.setPixmap(QPixmap.fromImage(self.pilToQImage(self.cropped_image)))

    def saveCroppedImage(self):
        if self.cropped_image:
            options = QFileDialog.Options()
            file_name, _ = QFileDialog.getSaveFileName(self, "Save Cropped Image", "", "Images (*.png *.xpm *.jpg *.bmp *.gif)", options=options)
            if file_name:
                self.cropped_image.save(file_name)

    def setCrop(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = ImageCropper()

    # 设置 YOLO 返回的尺寸
    mainWin.setCrop(260.82, 158.58, 31.25, 30.38)

    mainWin.show()
    sys.exit(app.exec_())
