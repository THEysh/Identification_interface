from PyQt5.QtCore import pyqtSignal, QObject


class DataInfo(QObject):
    nowImgCount_changed = pyqtSignal(int)
    nowPreImgCount_changed = pyqtSignal(int)
    def __init__(self):
        super().__init__()
        self._imgFilesPath = []
        self._allImgInfo = {}
        self._nowImgCount = 0
        self._nowPreImgCount = 0
        self.setNowPreImgCount(0)
        self.setNowPreImgCount(0)

    def setNowPreImgCount(self,count):
        self._nowPreImgCount = count
        self.nowPreImgCount_changed.emit(count)

    def setNowImgCount(self,count):
        self._nowImgCount = count
        self.nowImgCount_changed.emit(count)

    @property
    def getNowImgCount(self):
        return self._nowImgCount

    @property
    def getNowPreImgCount(self):
        return self._nowPreImgCount

    @property
    def getLenImgFilesPath(self):
        return len(self._imgFilesPath)

    @property
    def getImgFilesPath(self):
        return self._imgFilesPath

    @property
    def getAllImgInfo(self):
        return self._allImgInfo
    @property
    def getUnpredictedPath(self):
        if len(self._allImgInfo)==0: return []
        result = []
        for index,value in self._allImgInfo.items():
            if len(self._allImgInfo[index])<=1:
                result.append([index, self._allImgInfo[index]['org']['path']])
        return result

    def appendImgFilesPath(self,path:str):
        self._imgFilesPath.append(path)

    def imgAddInfo(self, index: int, key: str, info: dict):
        """key是org,或者pre"""
        if index in self._allImgInfo:
            if key in self._allImgInfo[index]:
                self._allImgInfo[index][key].update(info)
            else:
                self._allImgInfo[index][key] = info
        else:
            self._allImgInfo[index] = {key: info}

    def imgAddOrgPathInfo(self,index:int, path:str):
        self._allImgInfo[index] = {'org':{'path':path}}

    def reseat(self):
        self._imgFilesPath = []
        self._allImgInfo = {}
        self.setNowImgCount(0)
        self.setNowPreImgCount(0)