# coding:utf-8
from PyQt5.QtCore import Qt, QPoint, QSize
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QWheelEvent, QMouseEvent, QPixmap
from qfluentwidgets import PushButton, ImageLabel, FlowLayout, StrongBodyLabel

class DraggableImageLabel(ImageLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 用于拖动功能
        self.dragging = True
        self.offset = QPoint()
        # 用于缩放
        self.zoom_factor = 1.0
        self.original_height = 300
        self.current_pos = QPoint(0, 0)
        self.setScaledContents(True)

    def setCustomImage(self, image_path: str):
        """设置图片并初始化大小"""
        self.setImage(image_path)
        self.scaledToHeight(self.original_height)
        # 保存原始图片用于缩放
        self.original_pixmap = QPixmap(image_path)

    def wheelEvent(self, event: QWheelEvent):
        # 保存当前位置
        current_pos = self.pos()
        
        # 处理滚轮缩放
        if event.angleDelta().y() > 0:
            # 放大
            self.zoom_factor *= 1.1
        else:
            # 缩小
            self.zoom_factor *= 0.9
        
        # 限制缩放范围
        self.zoom_factor = max(0.1, min(self.zoom_factor, 5.0))
        
        # 计算新的大小
        new_height = int(self.original_height * self.zoom_factor)
        new_width = int(new_height * self.original_pixmap.width() / self.original_pixmap.height())
        
        # 设置新的大小
        self.setFixedSize(new_width, new_height)
        
        # 恢复位置
        self.move(current_pos)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.pos()
            self.raise_()  # 将被点击的图片置于顶层

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.dragging:
            new_pos = self.mapToParent(event.pos() - self.offset)
            self.move(new_pos)
            self.current_pos = new_pos

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.dragging = False

class HomeInterface(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)

        # 左侧面板
        self.leftPanel = QFrame(self)
        self.leftPanel.setMaximumWidth(150)
        self.leftLayout = QVBoxLayout(self.leftPanel)

        # 右侧面板
        self.rightPanel = QFrame(self)
        self.rightLayout = FlowLayout(self.rightPanel, needAni=True)

        self.setupUI()
        self.setObjectName('HomeInterface')

    def setupUI(self):
        # 添加左侧按钮
        self.loadImage1Btn = PushButton('加载图片1', self.leftPanel)
        self.loadImage2Btn = PushButton('加载图片2', self.leftPanel)
        self.inflabel = StrongBodyLabel("识别结果：11")

        self.leftLayout.addWidget(self.loadImage1Btn)
        self.leftLayout.addWidget(self.loadImage2Btn)
        self.leftLayout.addWidget(self.inflabel)
        self.leftLayout.addStretch()
        
        # 创建两个图片标签
        self.imageLabel1 = DraggableImageLabel(self.rightPanel)
        self.imageLabel2 = DraggableImageLabel(self.rightPanel)
        
        # 设置默认图片
        self.imageLabel1.setCustomImage('resource/painting_girl.png')
        self.imageLabel2.setCustomImage('resource/painting_girl.png')
        
        # 设置圆角
        self.imageLabel1.setBorderRadius(10, 10, 10, 10)
        self.imageLabel2.setBorderRadius(10, 10, 10, 10)
        
        # 添加图片到右侧布局
        self.rightLayout.addWidget(self.imageLabel1)
        self.rightLayout.addWidget(self.imageLabel2)
        
        # 设置右侧面板样式
        self.rightPanel.setStyleSheet("""
            QFrame {
                background-color: #f0f0f0;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        
        # 将左右面板添加到主布局
        self.hBoxLayout.addWidget(self.leftPanel)
        self.hBoxLayout.addWidget(self.rightPanel, 1)
        
        # 连接按钮信号
        self.loadImage1Btn.clicked.connect(lambda: self.loadImage(1))
        self.loadImage2Btn.clicked.connect(lambda: self.loadImage(2))

    def loadImage(self, image_num):
        from PyQt5.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            f"选择图片 {image_num}",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if file_path:
            if image_num == 1:
                self.imageLabel1.setCustomImage(file_path)
                self.imageLabel1.zoom_factor = 1.0  # 重置缩放因子
            else:
                self.imageLabel2.setCustomImage(file_path)
                self.imageLabel2.zoom_factor = 1.0  # 重置缩放因子
