from PySide.QtGui import QApplication
from qtlayoutbuilder.api.build import build_from_multi_line_string

app = QApplication([])

layouts = build_from_multi_line_string("""
    top_widget            QWidget
      rows                QVBoxLayout
        greeting          QLabel(Welcome to QtBuilder)
        some_buttons      QHBoxLayout
          button_a        QPushButton(Hello)
          button_b        QPushButton(World)
""")

# Access the objects created like this...
hello = layouts.at('button_a')

layouts.at('top_widget').show()
app.exec_()