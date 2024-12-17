import time
from enum import Enum

class Status(Enum):
    NOT_PREDICTED = "未预测"
    PREDICTING = "预测中"
    PREDICT_STOPING = "预测终止中"
    PREDICTED = "预测完成"


class StateMachineError(Exception):
    """状态机错误"""
    pass


class PredictionStateMachine:
    def __init__(self):
        self._status = Status.NOT_PREDICTED

    def __repr__(self):
        return f"当前状态: {self._status.value}"

    @property
    def statusValue(self):
        return self._status.value

    @property
    def status(self):
        return self._status

    def start_prediction(self):
        # 未预测-》预测中
        if self._status != Status.NOT_PREDICTED:
            raise StateMachineError(f"当前状态为 {self._status.value}，无法开始预测")
        self._status = Status.PREDICTING
        print(f"状态已更新为 {self._status.value}")

    def complete_prediction(self):
        # 预测中-》完成预测
        if self._status != Status.PREDICTING:
            raise StateMachineError(f"当前状态为 {self._status.value}，无法完成预测")
        self._status = Status.PREDICTED
        print(f"状态已更新为 {self._status.value}")

    def reset(self):
        if self._status == Status.NOT_PREDICTED:
            raise StateMachineError(f"当前状态已为 {self._status.value}，无需重置")
        self._status = Status.NOT_PREDICTED
        print(f"状态已重置为 {self._status.value}")

    def stop_prediction(self):
        # 预测中-》停止中
        if self._status != Status.PREDICTING:
            raise StateMachineError(f"当前状态为 {self._status.value}，无法停止预测")
        self._status = Status.PREDICT_STOPING
        # 停止中-》未预测
        # time.sleep(3)
        # self._status = Status.NOT_PREDICTED
        # btn.setText("开始预测")
        # btn.setEnabled(True)




# 使用示例
if __name__ == "__main__":
    sm = PredictionStateMachine()
    print(sm.status == Status.NOT_PREDICTED)
    print(sm)
    # 尝试启动预测
    sm.start_prediction()
    print(sm)
    # 尝试完成预测
    sm.complete_prediction()
    print(sm)
    # 尝试重置状态机
    try:
        sm.reset()
    except StateMachineError as e:
        print(f"异常处理: {e}")
    print(sm)
