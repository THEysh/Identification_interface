import os
import random
import time
from ultralytics import YOLO


def modifySuffix(orgPath: str, r=".jpg"):
    # 获取文件名和扩展名
    file_name, file_extension = os.path.splitext(os.path.basename(orgPath))
    # 修改扩展名为 .jpg
    new_file_name = f"{file_name}{r}"
    return new_file_name


class YoloModel:
    def __init__(self):
        self.yolo = YOLO("resource/best.pt", task="detect")
        self.inf = {0: '11 ', 1: '02 ', 2: '07 ', 3: '03 ', 4: '2 ', 5: '13 ', 6: '25 ', 7: '28 ', 8: '04 '}

    def run_inference(self, data: list):
        print("----YoloModel开始,data:{}----".format(data))
        orgImgPath = data[0]
        if not isinstance(orgImgPath, str):
            raise TypeError("路径必须要是字符串")
        iou = data[1]
        conf = data[2]
        try:
            time.sleep(random.random()*0.05)
            results = self.yolo.predict(source=orgImgPath, show=False, save=True, iou=iou, conf=conf)
        except:
            return [None, None, None, None, None, orgImgPath, None]
        imgShape = results[0].orig_shape
        runtime = results[0].speed['inference']
        save_dir = results[0].save_dir
        newImgName = modifySuffix(orgImgPath, r=".jpg")
        newImgPath = os.path.join(save_dir, newImgName)
        if len(results[0].boxes) <= 0:
            print("path:{},未识别".format(newImgPath))
            return [newImgPath, None, None, None, imgShape, orgImgPath, runtime]
        rectangle_pos = {
            "x": results[0].boxes.xyxy[0][0].item(),
            "y": results[0].boxes.xyxy[0][1].item(),
            "width": (results[0].boxes.xyxy[0][2] - results[0].boxes.xyxy[0][0]).item(),
            "height": (results[0].boxes.xyxy[0][3] - results[0].boxes.xyxy[0][1]).item()
        }
        scores = results[0].boxes.conf
        classes = results[0].boxes.cls
        print("YoloModel结束"+"-" * 100)
        return [newImgPath, rectangle_pos, float(scores[0]),
                self.inf[int(classes[0])], imgShape, orgImgPath, runtime]
