from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget

app = QApplication([])

window = QWidget()
layout = QVBoxLayout()

# 创建 QPushButton
button = QPushButton("这是一个非常长的按钮文本，它应该在按钮达到限制宽度时自动换行。")
button.setFixedWidth(100)  # 设置按钮宽度，超出文本会换行

layout.addWidget(button)

window.setLayout(layout)
window.show()
app.exec_()
