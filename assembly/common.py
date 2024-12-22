import os
import random
import string
import time


EmojiList = [
    "😀", "😆", "😊", "🥰", "😍", "😘", "😁",
    "😜", "😋", "🤗", "🤩", "🥳", "😏", "😎", "🎉", "😘",
    "👏", "👍", "💪", "🏆", "🌟", "✨", "😍",
    "🎈", "✨", "🎉", "🔥", "😀", "😁", "😆"]

sadnessEmojiList = [
    "😢", "😞", "😔", "😟", "😕", "😭", "😓", "😖",
    "😩", "😫", "😿", "🥺", "😥", "😪",
]
random.seed(time.time())

def path_to_absolute(path):
    absolute_path = os.path.abspath(path)
    return absolute_path

def getEmj(n=1):
    res = ""
    for i in range(n):
        res += random.choice(EmojiList) + " "
    return res


def getSadnessEmj(n=1):
    res = ""
    for i in range(n):
        res += random.choice(sadnessEmojiList) + " "
    return res


def getSpillFilepath(indexPaths: list, number: int, slidersValue: list):
    """

    """
    res = []
    for i in range(number):
        res.append([])
    for i, indexPath in enumerate(indexPaths):
        index = indexPath[0]
        path = indexPath[1]
        res[i % number].append(path)
        res[i % number].extend(slidersValue)
        res[i % number].append(index)
    predictDatas = []
    for i in range(len(res)):
        lst = res[i]
        chunk_size = len(slidersValue) + 2
        temp = [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]
        predictDatas.append(temp)
    return predictDatas


def randomName():
    name = "".join(random.choices(string.ascii_letters + string.digits, k=16))
    return name

def roundToR(num:float, r = None):
    if r is None:
            r = 2
    newNum = round(num, r )
    return str(newNum)

def checkFloat(data):
    if type(data) == float:
        return True
    else:
        return False
def checkInt(data):
    if type(data) == int:
        return True
    else:
        return False

if __name__ == '__main__':
    paths = ["file1", "file2", "file3", "file4", "file5", "f6", "f7", "f8", "f9", "f10"]
    number = 2
    slidersValue = [0.5, 1.0]
    print(getSpillFilepath(paths, number, slidersValue))
    print(randomName())
