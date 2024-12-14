import random
import string

def getEmj():
    # 这里简单地用ASCII字符模拟表情符号生成
    return random.choice(string.ascii_letters)

def predict_result():
    # 确保随机数生成部分被执行
    result = str(random.randint(1, 101))
    confidence = str(random.randint(1, 101))
    emojis = getEmj() * 5  # 生成5个随机表情符号

    predictResultInfo = [
        " 识别结果: ??? \n 置信度: ??? ",
        " 识别结果: {} \n置信度:{}% \n {}".format(result, confidence, emojis)
    ]
    return predictResultInfo

print(predict_result())
