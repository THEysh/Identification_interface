import os.path
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QTableWidgetItem, QVBoxLayout,QFileDialog
from qfluentwidgets import ImageLabel, PrimaryPushButton, InfoBar, InfoBarPosition
from assembly.DataInfo import DataInfo
from assembly.HistoryRecordTable import HistoryRecordTable
from assembly.PredictionState import PredictionStateMachine, Status
from assembly.ResultDisplay import processPreResDict, cropPreImagePath
from assembly.common import path_to_absolute, getTimeStr, copyFileToDir, getEmj
from qfluentwidgets import FluentIcon as FIF

from confSet import ConfGlobals


class TableInterface(QWidget):
    def __init__(self,datainfo:DataInfo, predictState:PredictionStateMachine, parent=None):
        super().__init__(parent)
        self.dataInfo = datainfo
        self.predictState = predictState
        # 用于检查重复的数据
        self.deduplicationCheck = {}
        self.setObjectName('TableInterface')
        # setTheme(Theme.DARK)
        self.hBoxLayout = QVBoxLayout(self)
        self.tableView = HistoryRecordTable(self)
        # 创建一个水平布局来放置self.outDataBtn按钮
        self.buttonLayout = QHBoxLayout()
        self.outDataBtn = PrimaryPushButton(FIF.LIBRARY_FILL, ' 导出数据 ', self)

        # 设置按钮布局的对齐方式，使其左对齐
        self.buttonLayout.addWidget(self.outDataBtn, alignment=Qt.AlignLeft)
        # 将按钮布局添加到主布局中
        self.hBoxLayout.addLayout(self.buttonLayout)
        # 将表格添加到主布局中
        self.hBoxLayout.addWidget(self.tableView)
        # 设置主布局的边距
        self.hBoxLayout.setContentsMargins(50, 30, 50, 30)
        # 设置主窗口的布局
        self.setLayout(self.hBoxLayout)
        # connect
        self.dataInfo.predictDataTable_changed.connect(self.tableChangedSlot)
        self.outDataBtn.clicked.connect(self._outDataBtnClicked)
        self.predictState.Status_changed.connect(self.outDataChange)

    def checkSavePathExist(self):
        # 检查路径是否存在
        if ('dataSaveDirectory' in ConfGlobals) and os.path.exists(ConfGlobals['dataSaveDirectory']):
            print("ini dataSaveDirectory路径存在， 加载成功")
            return ConfGlobals['dataSaveDirectory']
        else:
            return None

    def outDataChange(self, nowState):
        if nowState == Status.PREDICTED or nowState == Status.NOT_PREDICTED:
            self.outDataBtn.setEnabled(True)
        else:
            self.outDataBtn.setEnabled(False)

    def _getSavePath(self):
        path = self._checkSavePathExist()
        if path is None:
            folderPath = QFileDialog.getExistingDirectory(
                self,
                "选择保存文件夹",
                "./",
                QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
            )
            if not folderPath:
                return None
        else:
            return path

    def _outDataBtnClicked(self):
        tabledata = self.tableView.getTableData()
        if len(tabledata) == 0 : return
        folderPath = self._getSavePath()
        if folderPath is None : return
        nowTime = getTimeStr()
        saveImgPath = os.path.join(folderPath, "预测图_" + nowTime)
        os.makedirs(saveImgPath, exist_ok=False)
        # 写入文件
        with open(os.path.join(folderPath, '数据保存日志_' + nowTime + '.txt'), 'w') as file:
            for i, data1 in enumerate(tabledata):
                temp = ''
                for j, data2 in enumerate(data1):
                    if j==1: continue
                    if j==4:
                        # 保存图片
                        copyFileToDir(data2, saveImgPath)
                    temp += data2 + "; "
                # 去掉每行末尾多余的 "; "
                temp = temp.rstrip("; ")
                file.write(temp + "\n")
        InfoBar.success(
            title='成功',
            content="保存成功 " + getEmj(),
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            # position='Custom',   # NOTE: use custom info bar manager
            duration=2000,
            parent=self
        )

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
            self._addCropPreImg(self.tableView.rowCount()-1,1, path_str,
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

    def _addCropPreImg(self,row, col, image_path: str, x: float, y: float, width: float, height: float):
        if type(x)==float and type(y)==float and type(width)==float and type(height)==float:
            pixmap = cropPreImagePath(image_path, x, y, width, height)
            # 按比例缩放 QPixmap
            pixmap = pixmap.scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            cropImage = ImageLabel(parent=self.tableView)
            cropImage.setPixmap(pixmap)
            # 设置居中对齐
            # cropImage.setAlignment(Qt.AlignCenter)
            # 创建一个 QWidget 作为容器
            container = QWidget()
            layout = QVBoxLayout()
            layout.addWidget(cropImage)
            # 设置 QVBoxLayout 的对齐方式为居中对齐。这样，布局中的所有子控件都会在布局的中心位置显示
            layout.setAlignment(Qt.AlignCenter)
            # 设置margin
            layout.setContentsMargins(0, 0, 0, 0)
            container.setLayout(layout)
            # 将容器添加到表格中
            self.tableView.setCellWidget(row, col, container)