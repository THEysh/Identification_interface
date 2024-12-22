from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView, QWidget, QVBoxLayout
from qfluentwidgets import TableWidget, SmoothMode, ImageLabel
from assembly.common import getEmj


class HistoryRecordTable(TableWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setBorderVisible(True)
        self.setBorderRadius(8)
        # 自动换行
        self.setWordWrap(False)
        self.setRowCount(0)
        self.setColumnCount(6)
        self.setSelectRightClickedRow(True)
        # 根据内容调整列宽
        # self.resizeColumnsToContents()
        self.scrollDelagate.verticalSmoothScroll.setSmoothMode(SmoothMode.NO_SMOOTH)
        #隐藏表头
        # self.verticalHeader().hide()
        self.setHorizontalHeaderLabels(['识别结果 '+getEmj() ,
                                        '识别区域 '+getEmj() ,
                                        '置信度 ' + getEmj() ,
                                        '用时' + getEmj() ,
                                        '识别保存路径 ' + getEmj() ,
                                        '原图路径 '+getEmj()])
        self.setColumnWidth(0, 90)
        self.setColumnWidth(1, 90)
        self.setColumnWidth(2, 80)
        self.setColumnWidth(3, 70)
        self.setColumnWidth(4,210)
        self.setColumnWidth(5, 210)



