from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView
from qfluentwidgets import TableWidget, SmoothMode
from assembly.common import getEmj


class HistoryRecordTable(TableWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setBorderVisible(True)
        self.setBorderRadius(8)
        # 自动换行
        self.setWordWrap(False)
        self.setRowCount(0)
        self.setColumnCount(5)
        # 根据内容调整列宽
        self.setSelectRightClickedRow(True)
        # self.resizeColumnsToContents()
        self.scrollDelagate.verticalSmoothScroll.setSmoothMode(SmoothMode.NO_SMOOTH)
        #隐藏表头
        # self.verticalHeader().hide()
        self.setHorizontalHeaderLabels([' 识别结果 '+getEmj() ,
                                        ' 置信度 ' + getEmj(),
                                        ' 识别用时' + getEmj(),
                                        ' 识别保存路径 ' + getEmj(),
                                        ' 原图路径 '+getEmj()]),

        self.setColumnWidth(0, 80)
        self.setColumnWidth(1, 80)
        self.setColumnWidth(2, 80)
        self.setColumnWidth(3, 220)
        self.setColumnWidth(4,220)
