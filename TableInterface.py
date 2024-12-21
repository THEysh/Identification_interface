from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QTableWidgetItem, QHeaderView
from qfluentwidgets import TableWidget
from torch import classes
from ultralytics.solutions import inference

from assembly.DataInfo import DataInfo
from assembly.HistoryRecordTable import HistoryRecordTable
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


    def tableChangedSlot(self, dic:dict, index:int):
        prePath = dic['path']
        prePath = path_to_absolute(prePath)
        self.path_cache[prePath] = prePath
        if dic['classes'] is not None:
            ImgDetector = dic['classes']
        else:
            ImgDetector = getSadnessEmj() + "图片无标记"
        if dic['scores'] is not None:
            conf = str( roundToR(float(dic['scores'])*100)) + "%"
        else:
            conf = getSadnessEmj() + "图片无标记"
        inference_time = str(roundToR(float(dic['inference_time']))) + "ms"
        self.updateTable(0, ImgDetector)
        self.updateTable( 1, prePath)
        self.updateTable( 2, conf)
        self.updateTable( 3, inference_time)
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

    def check(self, prePath):
        pass
