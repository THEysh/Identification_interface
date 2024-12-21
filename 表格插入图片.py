from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
import sys

class TableWithImages(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建 QTableWidget
        self.table_widget = QTableWidget(4, 3)  # 4行3列

        # 设置列宽
        self.table_widget.setColumnWidth(0, 100)
        self.table_widget.setColumnWidth(1, 150)
        self.table_widget.setColumnWidth(2, 100)

        # 设置表头
        self.table_widget.setHorizontalHeaderLabels(['Column 1', 'Column 2', 'Column 3'])

        # 插入图片
        for row in range(4):
            for col in range(3):
                if col == 1:  # 在第二列插入图片
                    label = QLabel(self)
                    pixmap = QPixmap('resource/logo.png')
                    label.setPixmap(pixmap)
                    label.setAlignment(Qt.AlignCenter)
                    # 创建一个 QWidget 作为容器
                    container = QWidget()
                    layout = QVBoxLayout()
                    layout.addWidget(label)
                    layout.setAlignment(Qt.AlignCenter)
                    layout.setContentsMargins(0, 0, 0, 0)
                    container.setLayout(layout)
                    # 将容器添加到表格中
                    self.table_widget.setCellWidget(row, col, container)
                else:
                    item = QTableWidgetItem(f'Row {row} Col {col}')
                    self.table_widget.setItem(row, col, item)
        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TableWithImages()
    ex.show()
    sys.exit(app.exec_())
