from PyQt5.QtWidgets import QAction
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from qfluentwidgets import RoundMenu, FluentIcon as FIF, PrimarySplitPushButton
from assembly.common import getEmj


class SetThreadCountBtn(PrimarySplitPushButton):
    thread_count_changed = pyqtSignal(int)  # 定义一个信号，参数为字符串

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setText(" 线程数 "+getEmj())
        self.setIcon(FIF.DEVELOPER_TOOLS)
        self.menu = RoundMenu(parent=parent)
        for i in range(1, 9):
            action = QAction(text=f" {i} " + getEmj(), parent=self.menu)
            action.triggered.connect(self._create_set_text_lambda(i))
            self.menu.addAction(action)
        self.setFlyout(self.menu)

    def _create_set_text_lambda(self, i):
        return lambda: self.setTextAndEmitSignal(f"线程数 {i} " + getEmj(), i)

    @pyqtSlot(str)
    def setTextAndEmitSignal(self, text, count):
        super().setText(text)
        self.thread_count_changed.emit(count)  # 触发信号


# 使用示例
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget

    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout(window)

    btn = SetThreadCountBtn(parent=window)
    layout.addWidget(btn)


    @pyqtSlot(str)
    def on_text_changed(new_text):
        print(f"文本已改变为: {new_text}")


    btn.textChanged.connect(on_text_changed)

    window.show()
    sys.exit(app.exec_())
