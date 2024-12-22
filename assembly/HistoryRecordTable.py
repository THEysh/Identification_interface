from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView, QWidget, QVBoxLayout
from docutils.nodes import title
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
        # 点击会选中一列
        self.setSelectRightClickedRow(True)
        # 根据内容调整列宽
        # self.resizeColumnsToContents()
        self.scrollDelagate.verticalSmoothScroll.setSmoothMode(SmoothMode.NO_SMOOTH)
        #隐藏表头
        # self.verticalHeader().hide()
        # 设置行高不可调整
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.verticalHeader().setDefaultSectionSize(40) # 行高
        self.setHorizontalHeaderLabels(['识别结果 '+getEmj() ,
                                        '识别区域 '+getEmj() ,
                                        '置信度 ' + getEmj() ,
                                        '用时' + getEmj() ,
                                        '识别保存路径 ' + getEmj() ,
                                        '原图路径 '+getEmj()])
        self.setColumnWidth(0, 90)
        self.setColumnWidth(1, 90)
        self.setColumnWidth(2, 80)
        self.setColumnWidth(3, 95)
        self.setColumnWidth(4,200)
        self.setColumnWidth(5, 200)

    def getTableData(self):
        data = []
        for row in range(self.rowCount()):
            row_data = []
            for column in range(self.columnCount()):
                item = self.item(row, column)
                if item is not None:
                    row_data.append(item.text())
                else:
                    row_data.append('')
            data.append(row_data)
        return data

    def getTableTitle(self):
        headers = []
        for column in range(self.columnCount()):
            header_item = self.horizontalHeaderItem(column)
            if header_item is not None:
                headers.append(header_item.text())
            else:
                headers.append('')
        return headers