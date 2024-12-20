import sys
from PyQt5.QtCore import pyqtSignal, QObject, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel

class DataInfo(QObject):
    total_img_count_changed = pyqtSignal(int)
    pre_img_count_changed = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.total_img_count = 0
        self.pre_img_count = 0

    def set_total_img_count(self, count):
        self.total_img_count = count
        self.total_img_count_changed.emit(count)

    def set_pre_img_count(self, count):
        self.pre_img_count = count
        self.pre_img_count_changed.emit(count)

class _LeftContent(QWidget):
    def __init__(self, parent=None, data_info: DataInfo = None):
        super().__init__(parent)
        self.data_info = data_info
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        self.total_img_label = QLabel("图片数量: 0", self)
        self.pre_img_label = QLabel("预测图片数量: 0", self)
        layout.addWidget(self.total_img_label)
        layout.addWidget(self.pre_img_label)

        # 连接信号和槽
        self.data_info.total_img_count_changed.connect(self.update_total_img_count)
        self.data_info.pre_img_count_changed.connect(self.update_pre_img_count)

    def update_total_img_count(self, new_count):
        self.total_img_label.setText(f"图片数量: {str(new_count).zfill(3)}")

    def update_pre_img_count(self, new_count):
        self.pre_img_label.setText(f"预测图片数量: {str(new_count).zfill(3)}")

class FolderInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.data_info = DataInfo()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        self.left_region = _LeftContent(parent=self, data_info=self.data_info)
        self.load_img_btn = QPushButton("加载图片", self)
        self.predict_img_btn = QPushButton("预测图片", self)
        layout.addWidget(self.left_region)
        layout.addWidget(self.load_img_btn)
        layout.addWidget(self.predict_img_btn)

        self.load_img_btn.clicked.connect(self.load_img)
        self.predict_img_btn.clicked.connect(self.predict_img)

    def load_img(self):
        # 模拟加载图片
        new_img_count = 10  # 假设加载了10张图片
        self.data_info.set_total_img_count(new_img_count)

    def predict_img(self):
        # 模拟预测图片
        if self.data_info.total_img_count > 0:
            new_pre_img_count = 5  # 假设预测了5张图片
            self.data_info.set_pre_img_count(new_pre_img_count)
        else:
            print("没有图片可以预测")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FolderInterface()
    window.show()
    sys.exit(app.exec_())
