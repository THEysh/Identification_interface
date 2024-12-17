import sys
import time
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QLabel, QTextEdit


class Worker(QThread):
    finished = pyqtSignal(str)
    update_progress = pyqtSignal(str, int)

    def __init__(self, name, tasks):
        super().__init__()
        self.name = name
        self.tasks = tasks
        self.canRunning = True

    def run(self):
        total_tasks = len(self.tasks)
        for i, task in enumerate(self.tasks):
            if self.canRunning:
                # 模拟任务处理
                self.update_progress.emit(self.name, i + 1)
                time.sleep(0.1)
            else:
                break
        self.finished.emit(self.name)

    def stop(self):
        self.canRunning = False


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.threads = {}

    def initUI(self):
        self.layout = QVBoxLayout()
        self.start_button = QPushButton('Start Threads', self)
        self.start_button.clicked.connect(self.start_threads)
        self.stop_button = QPushButton('Stop Threads', self)
        self.stop_button.clicked.connect(self.stop_threads)
        self.log_text = QTextEdit(self)

        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.stop_button)
        self.layout.addWidget(self.log_text)

        self.setLayout(self.layout)

    def start_threads(self):
        self.threads = {}
        tasks = list(range(1, 101))  # 100个任务
        num_threads = 3
        task_per_thread = len(tasks) // num_threads
        extra_tasks = len(tasks) % num_threads

        start_index = 0
        for i in range(num_threads):
            end_index = start_index + task_per_thread + (1 if i < extra_tasks else 0)
            thread_tasks = tasks[start_index:end_index]
            worker = Worker(f'Thread{i+1}', thread_tasks)
            self.threads[f'Thread{i+1}'] = worker
            worker.update_progress.connect(self.update_progress)
            worker.finished.connect(self.thread_finished)
            worker.start()
            start_index = end_index

    def stop_threads(self):
        for name, worker in self.threads.items():
            worker.stop()
        self.log_text.append('All threads stopped')

    def update_progress(self, name, value):
        self.log_text.append(f'{name} Progress: {value}/{len(self.threads[name].tasks)}')

    def thread_finished(self, name):
        self.log_text.append(f'{name} finished')
        if all(not thread.isRunning() for thread in self.threads.values()):
            self.log_text.append('All threads finished')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
