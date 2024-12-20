
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
        self.yolo = YOLO("./best.pt", task="detect")
        self.inf = {0: '11 ', 1: '02 ', 2: '07 ', 3: '03 ', 4: '2 ', 5: '13 ', 6: '25 ', 7: '28 ', 8: '04 '}
        self.saveMif = 3

    def run_inference(self, data: list):
        print("----YoloModel开始,data:{}----".format(data) * 3)

        orgimgpath = data[0]
        if not isinstance(orgimgpath, str):
            raise TypeError("路径必须要是字符串")
        iou = data[1]
        conf = data[2]
        print("开始")
        try:
            time.sleep(random.random()*0.05)
            results = self.yolo.predict(source=orgimgpath, show=False, save=True, iou=iou, conf=conf)
        except:

            return [None, None, None, None, None, orgimgpath, None]
        imgshape = results[0].orig_shape

        runtime = results[0].speed['inference']

        save_dir = results[0].save_dir

        newimgName = modifySuffix(orgimgpath, r=".jpg")

        newimgpath = os.path.join(save_dir, newimgName)

        if len(results[0].boxes) <= 0:
            return [newimgpath, None, None, None, imgshape, orgimgpath, runtime]
            print("未识别")
        rectangle_pos = {
            "x": round(results[0].boxes.xyxy[0][0].item(), self.saveMif),
            "y": round(results[0].boxes.xyxy[0][1].item(), self.saveMif),
            "width": round((results[0].boxes.xyxy[0][2] - results[0].boxes.xyxy[0][0]).item(), self.saveMif),
            "height": round((results[0].boxes.xyxy[0][3] - results[0].boxes.xyxy[0][1]).item(), self.saveMif)
        }

        scores = results[0].boxes.conf
        classes = results[0].boxes.cls
        print("-" * 100)
        return [newimgpath, rectangle_pos, round(float(scores[0]), self.saveMif), self.inf[int(classes[0])],
                imgshape, orgimgpath, round(runtime, self.saveMif)]
