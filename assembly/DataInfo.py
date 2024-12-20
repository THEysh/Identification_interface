
class DataInfo:
    def __init__(self):
        self._maxImgCount = 0
        self._imgFilesPath = []
        self._allImgInfo = {}

    @property
    def getMaxImgCount(self):
        return self._maxImgCount

    @property
    def getLenImgFilesPath(self):
        return len(self._imgFilesPath)

    @property
    def getImgFilesPath(self):
        return self._imgFilesPath

    def appendImgFilesPath(self,path:str):
        self._imgFilesPath.append(path)

    def setMaxImgCount(self, maxImgCount:int):
        self._maxImgCount = maxImgCount

    def imgAddInfo(self, index: int, key: str, info: dict):
        "key是org,或者pre"
        if index in self._allImgInfo:
            if key in self._allImgInfo[index]:
                self._allImgInfo[index][key].update(info)
            else:
                self._allImgInfo[index][key] = info
        else:
            self._allImgInfo[index] = {key: info}

    def reseat(self):
        self._maxImgCount = 0
        self._imgFilesPath = []
        self._allImgInfo = {}