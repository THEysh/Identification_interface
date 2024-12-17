from enum import Enum

class Status(Enum):
    NOT_PREDICTED = "未预测"
    PREDICTING = "预测中"
    PREDICTED = "预测完成"

class PredictionState:
    def __init__(self):
        self._status = Status.NOT_PREDICTED

    def __repr__(self):
        return f"当前状态: {self._status.value}"

    @property
    def status(self):
        return self._status.value

    def start_prediction(self):
        if self._status != Status.NOT_PREDICTED:
            print(f"当前状态为 {self._status.value}，无法开始预测")
            return
        self._status = Status.PREDICTING
        print(f"状态已更新为 {self._status.value}")

    def complete_prediction(self):
        if self._status != Status.PREDICTING:
            print(f"当前状态为 {self._status.value}，无法完成预测")
            return
        self._status = Status.PREDICTED
        print(f"状态已更新为 {self._status.value}")

    def reset(self):
        if self._status == Status.NOT_PREDICTED:
            print(f"当前状态已为 {self._status.value}，无需重置")
            return
        self._status = Status.NOT_PREDICTED
        print(f"状态已重置为 {self._status.value}")

class Predictor:
    def __init__(self, state):
        self.state = state

    def start(self):
        self.state.start_prediction()

    def end(self):
        self.state.complete_prediction()

    def reset(self):
        self.state.reset()

if __name__ == "__main__":
    state_machine = PredictionState()
    predictor = Predictor(state_machine)

    print(state_machine)
    # 尝试启动预测
    predictor.start()
    print(state_machine)
    # 尝试完成预测
    predictor.end()
    print(state_machine)
    # 尝试重置状态机
    predictor.reset()
    print(state_machine)
