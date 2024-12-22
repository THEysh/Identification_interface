from distutils.command.check import check
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QTableWidgetItem, QHeaderView, QVBoxLayout
from qfluentwidgets import TableWidget, ImageLabel
from torch import classes
from ultralytics.solutions import inference
from assembly.DataInfo import DataInfo
from assembly.HistoryRecordTable import HistoryRecordTable
from assembly.ResultDisplay import processPreResDict, cropPreImagePath
from assembly.common import roundToR, getEmj, getSadnessEmj, path_to_absolute


class TableInterface(QWidget):
    def __init__(self,datainfo:DataInfo, parent=None):
        super().__init__(parent)
        self.dataInfo = datainfo
        self.setObjectName('TableInterface')
        # setTheme(Theme.DARK)
        self.hBoxLayout = QHBoxLayout(self)
        self.tableView = HistoryRecordTable(self)
        # 设置了布局的边距
        self.hBoxLayout.setContentsMargins(50, 30, 50, 30)
        self.hBoxLayout.addWidget(self.tableView)
        self.dataInfo.predictDataTable_changed.connect(self.tableChangedSlot)
        self.deduplicationCheck = {}


    def tableChangedSlot(self, dic:dict, index:int):
        if 'pre' in dic and 'org' in dic:
            # 检查表格是否有数据
            if 'path' in dic['org']:
                orgPath = path_to_absolute(dic['org']['path'])
                if self.checkOrgPath(orgPath): return
            (path_str, x_float_or_str, y_float_or_str, width_float_or_str, height_float_or_str,
             conf_str, classes_str, runtime_str) = processPreResDict(dic['pre'])
            inference_time = runtime_str + "ms"
            if len(conf_str)>=1:
                conf_str = conf_str + "%"
            # 添加数据
            self.updateTable(0, classes_str)
            self.addCropPreImg(self.tableView.rowCount()-1,1, path_str,
                               x_float_or_str, y_float_or_str, width_float_or_str, height_float_or_str)
            self.updateTable( 2, conf_str)
            self.updateTable( 3, inference_time)
            self.updateTable( 4, path_str)
            if 'path' in dic['org']:
                orgPath = path_to_absolute(dic['org']['path'])
                self.updateTable(5, orgPath)
                # 添加去重复处理
                self.deduplicationCheck[orgPath] = True
        else:
            return
    def updateTable(self, col, data):
        """
        更新表格
        """
        current_rows = self.tableView.rowCount()
        if col==0:
            self.tableView.setRowCount(current_rows+1)
            self.tableView.setItem(current_rows, col, QTableWidgetItem(data))
        else:
            self.tableView.setItem(current_rows-1, col, QTableWidgetItem(data))

    def checkOrgPath(self, orgPath):
        if orgPath in self.deduplicationCheck:
            return True
        else:
            return False

    def addCropPreImg(self,row, col, image_path: str, x: float, y: float, width: float, height: float):
        if type(x)==float and type(y)==float and type(width)==float and type(height)==float:
            pixmap = cropPreImagePath(image_path, x, y, width, height)
            # 按比例缩放 QPixmap
            pixmap = pixmap.scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            cropImage = ImageLabel(parent=self.tableView)
            cropImage.setPixmap(pixmap)
            # 设置居中对齐
            cropImage.setAlignment(Qt.AlignCenter)
            # 创建一个 QWidget 作为容器
            container = QWidget()
            layout = QVBoxLayout()
            layout.addWidget(cropImage)
            #  设置 QVBoxLayout 的对齐方式为居中对齐。这样，布局中的所有子控件都会在布局的中心位置显示
            layout.setAlignment(Qt.AlignCenter)
            layout.setContentsMargins(5, 5, 5, 5)
            container.setLayout(layout)
            # 将容器添加到表格中
            self.tableView.setCellWidget(row, col, container)