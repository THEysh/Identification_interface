from distutils.command.check import check

from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QTableWidgetItem, QHeaderView
from qfluentwidgets import TableWidget
from torch import classes
from ultralytics.solutions import inference
from assembly.DataInfo import DataInfo
from assembly.HistoryRecordTable import HistoryRecordTable
from assembly.ResultDisplay import processPreResDict
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
            self.updateTable( 1, conf_str)
            self.updateTable( 2, inference_time)
            self.updateTable( 3, path_str)
            if 'path' in dic['org']:
                orgPath = path_to_absolute(dic['org']['path'])
                self.updateTable(4, orgPath)
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
