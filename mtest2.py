from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 创建网格布局
        layout = QGridLayout()

        # 添加按钮到布局
        layout.addWidget(QPushButton('Button 1'), 0, 0)  # 第1行，第1列
        layout.addWidget(QPushButton('Button 2'), 0, 1)  # 第1行，第2列
        layout.addWidget(QPushButton('Button 3'), 1, 0, 1, 2)  # 第2行，第1列，跨越2列

        # 设置布局到窗口
        self.setLayout(layout)

        self.setWindowTitle('QGridLayout Example')
        self.show()

if __name__ == '__main__':
    app = QApplication([])
    window = MyWindow()
    app.exec_()
