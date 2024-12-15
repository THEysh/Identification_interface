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

def mockDuration(parent:QWidget):
    loop = QEventLoop(parent)
    QTimer.singleShot(1500, loop.quit)
    loop.exec()