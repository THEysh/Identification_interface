import asyncio
import os
from concurrent.futures import ThreadPoolExecutor
from ultralytics import YOLO
from yoloMod import modifySuffix


class YoloModel:
    def __init__(self):
        self.yolo = YOLO("./best.pt", task="detect")
        self.inf = {0: '11 ', 1: '02 ', 2: '07 ', 3: '03 ', 4: '2 ', 5: '13 ', 6: '25 ', 7: '28 ', 8: '04 '}
        self.saveMif = 3
        self.executor = ThreadPoolExecutor()  # 创建线程池

    async def run_inference(self, data: list):
        print("run_inference:", data)
        orgimgpath = data[0]
        if not isinstance(orgimgpath, str):
            raise TypeError("路径必须要是字符串")
        iou = data[1]
        conf = data[2]
        try:
            print("YOLO object attributes before predict:", dir(self.yolo))
            # 使用线程池来执行同步函数
            loop = asyncio.get_event_loop()
            results = await loop.run_in_executor(self.executor, self.yolo.predict, orgimgpath, False, True, iou, conf)
            print("Results object:", results)
            print("Results object attributes:", dir(results[0]))
        except AttributeError as e:
            print("AttributeError occurred:", e)
            raise
        except Exception as e:
            print("Exception occurred during prediction:", e)
            raise

        imgshape = results[0].orig_shape
        runtime = results[0].speed['inference']
        save_dir = results[0].save_dir
        newimgName = modifySuffix(orgimgpath, r=".jpg")
        newimgpath = os.path.join(save_dir, newimgName)

        if len(results[0].boxes) <= 0:
            return [newimgpath, None, None, None, imgshape, orgimgpath, runtime]

        rectangle_pos = {
            "x": round(results[0].boxes.xyxy[0][0].item(), self.saveMif),
            "y": round(results[0].boxes.xyxy[0][1].item(), self.saveMif),
            "width": round((results[0].boxes.xyxy[0][2] - results[0].boxes.xyxy[0][0]).item(), self.saveMif),
            "height": round((results[0].boxes.xyxy[0][3] - results[0].boxes.xyxy[0][1]).item(), self.saveMif)
        }

        scores = results[0].boxes.conf
        classes = results[0].boxes.cls

        return [newimgpath, rectangle_pos, round(float(scores[0]), self.saveMif), self.inf[int(classes[0])],
                imgshape, orgimgpath, round(runtime, self.saveMif)]

# 示例主程序
async def main():
    model = YoloModel()
    data = ["resource/cut_RGB_20240719084737.png", 0.5, 0.4]  # 替换为实际数据
    result = await model.run_inference(data)
    print(result)

if __name__ == '__main__':
    asyncio.run(main())
