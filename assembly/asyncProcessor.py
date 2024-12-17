from PyQt5.QtCore import QThread, pyqtSignal


class _ImagePredictThread(QThread):
    # list的数值分别为：saveDir, rectanglePosDict, scores, classes, inferenceTime
    varSignalConnector = pyqtSignal(list)
    def __init__(self, requestsFunction, predictData: list, parent=None):
        super().__init__(parent)
        self.predictData = predictData
        self.requestsFunction = requestsFunction

    def run(self):
        print("run, begin")
        res = self.requestsFunction(self.predictData)
        if res is None:
            self.varSignalConnector.emit([None,None,None,None,None])
        else:
            saveDir = res["save_dir"]
            rectanglePosDict = res["rectangle_pos"]
            scores = res["scores"]
            classes = res["classes"]
            inferenceTime = res["inference_time"]
            self.varSignalConnector.emit([saveDir, rectanglePosDict, scores, classes, inferenceTime])