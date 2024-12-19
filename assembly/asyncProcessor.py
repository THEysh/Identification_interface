import os
import time
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap


class AsyncFolderInterfaceWork:
    def __init__(self, ThreadCount=3, parent=None):
        self.threadCount = ThreadCount
        self.parent = parent
        self.preThreads = {}
        self.loadimgThreads = {}
        self.loadimgPreThreads = {}

    def addPreThread(self, name, work):
        self.preThreads[name] = work

    def stopOnePreThread(self, name):
        #  停止预测任务
        if name in self.preThreads:
            worker = self.preThreads[name]
            worker.stop()
            del self.preThreads[name]
            print(f"\033[93m警告: - {name}线程已经停止 - \033[0m")

    def stopAllPrediction(self):
        names = list(self.preThreads.keys())
        for name in names:
            worker = self.preThreads[name]
            worker.stop()
            del self.preThreads[name]
            print(f"\033[93m警告: - {name}线程已经手动停止 - \033[0m")

    def addLoadimgThread(self, name, work):
        self.loadimgPreThreads[name] = work

    def finishedOneloadPreimgThreads(self, name):
        if name in self.loadimgPreThreads:
            worker = self.loadimgPreThreads[name]
            del self.loadimgPreThreads[name]
            print(f"\033[93m加载预测的图片完成: - 线程name:{name},已经停止 - \033[0m")

    @property
    def loadimgPreThreadsCount(self):
        return len(self.loadimgPreThreads)




class ImagePredictThread(QThread):
    # list的数值分别为：saveDir, rectanglePosDict, scores, classes, inferenceTime
    varSignalConnector = pyqtSignal(list)
    error_signal = pyqtSignal(str)
    def __init__(self, requestsFunction, predictData: list, name: str, parent=None):
        super().__init__(parent)
        self.predictData = predictData
        self.requestsFunction = requestsFunction
        self.name = name
        self.canRunning = True

    def run(self):
        if self.canRunning:
            try:
                # 调用模型的推理方法
                result = self.requestsFunction(self.predictData)
                # 发出信号，传递结果
                self.varSignalConnector.emit(result)
            except Exception as e:
                # 如果出现异常，发出错误信号
                self.error_signal.emit(str(e))

    def stop(self):
        self.canRunning = False


class ImagePredictFolderThread(QThread):
    # list的数值分别为：saveDir, rectanglePosDict, scores, classes, inferenceTime, threadname
    varSignalConnector = pyqtSignal(list)

    def __init__(self, requestsFunction, predictDatas: list, threadName: str, parent=None):
        super().__init__(parent)
        self.predictDatas = predictDatas
        self.requestsFunction = requestsFunction
        self.threadName = threadName
        self.canRunning = True

    def run(self):
        for data in self.predictDatas:
            if self.canRunning:
                index = data[3]
                res = self.requestsFunction(data)
                self.varSignalConnector.emit(res)

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


class loadPredictionImageThread(QThread):
    varSignalConnector = pyqtSignal(QPixmap, int, str)

    def __init__(self, predictionPath: str, index: int, threadName: str, parent=None):
        super().__init__(parent)
        self.predictionFile = predictionPath
        self.index = index
        self.threadName = threadName

    def run(self):
        pixmap = QPixmap(self.predictionFile)
        # 延迟加载，避免卡顿
        time.sleep(0.002)
        self.varSignalConnector.emit(pixmap, self.index, self.threadName)
