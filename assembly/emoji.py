import random
import time

# 在程序开始时设置一个动态的种子值

EmojiList = [
    "😀", "😆", "😊", "😇", "🥰", "😍", "😘", "😁",
     "😜",  "😋",  "🤗", "🤩", "🥳", "😏", "😎", "🎉", "😘",
    "👏", "👍", "💪", "🏆", "🌟", "✨", "😍",
     "🎈", "✨", "🎉", "🔥", "😀", "😁", "😆"]

sadnessEmojiList = [
    "😢", "😞", "😔", "😟", "😕", "😭", "😓", "😖",
    "😩", "😫", "😿", "🥺", "😥", "😪",
]

def getEmj(n=1):
    random.seed(time.time())
    res = ""
    for i in range(n):
        res += random.choice(EmojiList)+" "
    return res

def getSadnessEmj(n=1):
    random.seed(time.time())
    res = ""
    for i in range(n):
        res += random.choice(sadnessEmojiList)+" "
    return res