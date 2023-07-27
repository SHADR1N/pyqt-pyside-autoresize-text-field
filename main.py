import sys
from PySide6.QtWidgets import QTextEdit, QSizePolicy, QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtGui import QTextDocument
from PySide6.QtCore import Qt, QTimer


class AutoResizeText(QTextEdit):

    def __init__(self, parent=None, message_text=""):
        super().__init__(parent=parent)
        self.setFrameStyle(QTextEdit.Shape.NoFrame)  # Remove the frame around QTextEdit
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setObjectName(u"textChat")

        self.adjustHeightOnShow = True
        self.resizing = False

        self.minimal_width = 0
        self.maximum_width = 350

        self.setReadOnly(True)

        self.setText(message_text)
        self.setMaximumWidth(self.maximum_width)

    def hasHeightForWidth(self):
        return True

    def disableResizing(self):
        self.resizing = False

    def heightForWidth(self, event_width):
        width = event_width
        size = self.document().size()
        if self.resizing:
            self.setFixedHeight(size.height() + 2)
            return self.document().size().height()

        width = self.get_optimal_width(width)

        self.resizing = True
        self.setFixedSize(width + 5, size.height() + 2)
        self.document().setTextWidth(width)
        if event_width:
            QTimer.singleShot(300, self.disableResizing)
        return size.height()

    def get_optimal_width(self, width=None):
        if not width:
            width = self.minimal_width

        text = self.toPlainText()
        font = self.font()

        # Use QTextDocument to get the text width considering line wrapping
        text_document = QTextDocument()
        text_document.setDefaultFont(font)
        text_document.setPlainText(text)

        text_width = text_document.idealWidth()

        if text_width <= self.maximum_width:
            width = text_width
        elif text_width >= self.maximum_width:
            width = self.maximum_width

        if width <= self.minimal_width:
            width = self.minimal_width

        return width

    def resizeEvent(self, event):
        if self.adjustHeightOnShow:

            width = self.get_optimal_width()
            size = self.document().size()

            self.setFixedSize(width + 5, size.height() + 2)
            self.document().setTextWidth(width)
            self.adjustHeightOnShow = False
            self.resizing = True

        super().resizeEvent(event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        big_message = """
Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
        """.strip()

        small_message = "Hello world!"
        one_symbol = "."
        vertical_message = """
1


2
        """.strip()

        custom_text_field = AutoResizeText(parent=self, message_text=big_message)
        custom_text_field.setStyleSheet("color: white; background: gray;")

        custom_text_field1 = AutoResizeText(parent=self, message_text=small_message)
        custom_text_field1.setStyleSheet("color: white; background: gray;")

        custom_text_field2 = AutoResizeText(parent=self, message_text=vertical_message)
        custom_text_field2.setStyleSheet("color: white; background: gray;")

        custom_text_field3 = AutoResizeText(parent=self, message_text=one_symbol)
        custom_text_field3.setStyleSheet("color: white; background: gray;")

        central_widget = QWidget()  # Create a central widget
        self.setCentralWidget(central_widget)  # Set the central widget

        layout = QVBoxLayout(central_widget)  # Use the central widget as the layout parent
        layout.addWidget(custom_text_field, alignment=(
            Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight
        ))
        layout.addWidget(custom_text_field1, alignment=(
            Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft
        ))
        layout.addWidget(custom_text_field2, alignment=(
            Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight
        ))
        layout.addWidget(custom_text_field3, alignment=(
            Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft
        ))

        # Call this methods after add widget in frame
        custom_text_field.heightForWidth(None)
        custom_text_field.resizing = True

        custom_text_field1.heightForWidth(None)
        custom_text_field1.resizing = True

        custom_text_field2.heightForWidth(None)
        custom_text_field2.resizing = True

        custom_text_field3.heightForWidth(None)
        custom_text_field3.resizing = True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
