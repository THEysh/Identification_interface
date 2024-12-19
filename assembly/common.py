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


def getSpillFilepath(paths: list, number: int, slidersValue: list):
    """

    """
    res = []
    for i in range(number):
        res.append([])
    for i, path in enumerate(paths):
        res[i % number].append(path)
        res[i % number].extend(slidersValue)
        res[i % number].append(i)
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





if __name__ == '__main__':
    paths = ["file1", "file2", "file3", "file4", "file5", "f6", "f7", "f8", "f9", "f10"]
    number = 2
    slidersValue = [0.5, 1.0]
    print(getSpillFilepath(paths, number, slidersValue))
    print(randomName())
