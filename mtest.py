import sys
from PyQt5.QtCore import QThread, QMutex, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel

class WorkerThread(QThread):
    update_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.mutex = QMutex()
        self.running = True

    def run(self):
        count = 0
        while self.running:
            self.mutex.lock()
            count += 1
            self.update_signal.emit(f'Count: {count}')
            self.mutex.unlock()
            self.msleep(500)  # 模拟耗时操作

    def stop(self):
        self.running = False
        self.quit()
        self.wait()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.worker_thread = WorkerThread()
        self.worker_thread.update_signal.connect(self.update_label)
        self.worker_thread.start()

    def initUI(self):
        self.setWindowTitle('PyQt5 Sync Lock Example')
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.label = QLabel('Count: 0', self)
        layout.addWidget(self.label)

        start_button = QPushButton('Start', self)
        start_button.clicked.connect(self.start_thread)
        layout.addWidget(start_button)

        stop_button = QPushButton('Stop', self)
        stop_button.clicked.connect(self.stop_thread)
        layout.addWidget(stop_button)

        self.setLayout(layout)

    def start_thread(self):
        if not self.worker_thread.isRunning():
            self.worker_thread = WorkerThread()
            self.worker_thread.update_signal.connect(self.update_label)
            self.worker_thread.start()

    def stop_thread(self):
        self.worker_thread.stop()

    def update_label(self, text):
        self.label.setText(text)

    def closeEvent(self, event):
        self.stop_thread()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
