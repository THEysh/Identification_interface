import sys
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QTextEdit

class WorkerThread(QThread):
    # 定义一个信号，用于传递异步函数的结果
    result_ready = pyqtSignal(str)

    def run(self):
        # 模拟一个耗时的异步任务
        import time
        time.sleep(2)  # 模拟耗时操作
        result = "异步任务完成！"
        self.result_ready.emit(result)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口标题和大小
        self.setWindowTitle("PyQt5 异步函数示例")
        self.setGeometry(100, 100, 300, 200)

        # 创建布局
        layout = QVBoxLayout()

        # 创建标签和文本编辑框
        self.label = QLabel("点击按钮开始异步任务")
        self.text_edit = QTextEdit()

        # 创建按钮
        self.button = QPushButton("开始异步任务")
        self.button.clicked.connect(self.start_async_task)

        # 添加控件到布局
        layout.addWidget(self.label)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.button)

        # 设置布局
        self.setLayout(layout)

    def start_async_task(self):
        # 创建并启动工作线程
        self.worker = WorkerThread()
        self.worker.result_ready.connect(self.update_ui)
        self.worker.start()

    def update_ui(self, result):
        # 更新 UI
        self.text_edit.append(result)
        self.label.setText("任务完成")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
