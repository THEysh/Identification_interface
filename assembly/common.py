import random
import time
from PyQt5.QtCore import QEventLoop, QTimer
from PyQt5.QtWidgets import QFrame, QWidget




EmojiList = [
    "😀", "😆", "😊", "🥰", "😍", "😘", "😁",
     "😜",  "😋",  "🤗", "🤩", "🥳", "😏", "😎", "🎉", "😘",
    "👏", "👍", "💪", "🏆", "🌟", "✨", "😍",
     "🎈", "✨", "🎉", "🔥", "😀", "😁", "😆"]

sadnessEmojiList = [
    "😢", "😞", "😔", "😟", "😕", "😭", "😓", "😖",
    "😩", "😫", "😿", "🥺", "😥", "😪",
]
random.seed(time.time())
def getEmj(n=1):

    res = ""
    for i in range(n):
        res += random.choice(EmojiList)+" "
    return res

def getSadnessEmj(n=1):

    res = ""
    for i in range(n):
        res += random.choice(sadnessEmojiList)+" "
    return res

def getSpillFilepath(paths:list,number:int,slidersValue:list):
    """
    函数 getSpillFilepath 的功能是对输入的文件路径列表 paths 进行分组，并结合滑块值 slidersValue 生成一个新的数据结构.
    假设 paths = ["file1", "file2", "file3", "file4", "file5"]，number = 2，slidersValue = [0.5, 1.0]，则：
    将 paths 分为 2 组，结果是：
    res[0] = ["file1", "file3", "file5"]
    res[1] = ["file2", "file4"]
    对每个组中的路径和 slidersValue 进行组合：
    对 res[0] 中的每个文件路径，结果是：
    ["file1", 0.5, 1.0]
    ["file3", 0.5, 1.0]
    ["file5", 0.5, 1.0]
    对 res[1] 中的每个文件路径，结果是：
    ["file2", 0.5, 1.0]
    ["file4", 0.5, 1.0]
    最终的 predictDatas 将是：
    :param paths:
    :param number:
    :param slidersValue:
    :return:
    """
    res = []
    for i in range(number):
        res.append([])
    for i,path in enumerate(paths):
        res[i%number].append(path)
    # predictDatas最终生产一个3维数组
    predictDatas = []
    for i,d1 in enumerate(res):
        temp1 = []
        for j,d2 in enumerate(d1):
            temp2 = []
            temp2.append(d2)
            temp2.extend(slidersValue)
            temp1.append(temp2)
        predictDatas.append(temp1)
    return predictDatas