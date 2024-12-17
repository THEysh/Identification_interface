import time
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap


class AsyncFolderInterfaceWork:
    def __init__(self, ThreadCount=3, parent=None):
        self.threadCount = ThreadCount
        self.parent = parent
        self.preThreads = {}
        self.loadimgThreads = {}

    def stopPreThread(self):
        #  停止所有预测任务
        for name, worker in self.preThreads.items():
            worker.stop()
        print(f"\033[93m警告: - 所有线程均已经停止 - \033[0m")

    def addPreThread(self, name, work):
        self.preThreads[name] = work

    def addLoadimgThread(self, name, work):
        self.loadimgThreads[name] = work


class ImagePredictThread(QThread):
    finished = pyqtSignal(str)
    # list的数值分别为：saveDir, rectanglePosDict, scores, classes, inferenceTime
    varSignalConnector = pyqtSignal(list)

    def __init__(self, requestsFunction, predictData: list, name: str, parent=None):
        super().__init__(parent)
        self.predictData = predictData
        self.requestsFunction = requestsFunction
        self.name = name
        self.canRunning = True

    def run(self):
        if self.canRunning:
            res = self.requestsFunction(self.predictData)
            if res is None:
                self.varSignalConnector.emit([None, None, None, None, None])
            else:
                saveDir = res["save_dir"]
                rectanglePosDict = res["rectangle_pos"]
                scores = res["scores"]
                classes = res["classes"]
                inferenceTime = res["inference_time"]
                self.varSignalConnector.emit([saveDir, rectanglePosDict, scores, classes, inferenceTime])
        self.finished.emit(self.name)

    def stop(self):
        self.canRunning = False


class ImagePredictFolderThread(QThread):
    finished = pyqtSignal(str)
    # list的数值分别为：saveDir, rectanglePosDict, scores, classes, inferenceTime
    varSignalConnector = pyqtSignal(list)

    def __init__(self, requestsFunction, predictDatas: list, name: str, parent=None):
        super().__init__(parent)
        self.predictDatas = predictDatas
        self.requestsFunction = requestsFunction
        self.name = name
        self.canRunning = True

    def run(self):

        for data in self.predictDatas:
            if self.canRunning:
                res = self.requestsFunction(data)
                if res is None:
                    self.varSignalConnector.emit([None, None, None, None, None])
                else:
                    saveDir = res["save_dir"]
                    rectanglePosDict = res["rectangle_pos"]
                    scores = res["scores"]
                    classes = res["classes"]
                    inferenceTime = res["inference_time"]
                    self.varSignalConnector.emit([saveDir, rectanglePosDict, scores, classes, inferenceTime])
        if self.canRunning:
            # 成功完成任务状态
            self.finished.emit(self.name+"_1")
        else:
            # 被迫中断
            self.finished.emit(self.name + "_0")

    def stop(self):
        self.canRunning = False


class ImageLoaderThread(QThread):
    varSignalConnector = pyqtSignal(QPixmap, int)

    def __init__(self, image_files, parent=None):
        super().__init__(parent)
        self.image_files = image_files

    def run(self):
        for i, image_path in enumerate(self.image_files):
            pixmap = QPixmap(str(image_path))
            # 延迟加载，避免卡顿
            time.sleep(0.002)
            self.varSignalConnector.emit(pixmap, i)
