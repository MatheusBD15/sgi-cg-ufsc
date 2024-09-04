import sys
from PySide6.QtCore import Qt
from PySide6.QtQuick import QQuickView
from PySide6.QtWidgets import (
    QApplication,
)

if __name__ == "__main__":
    app = QApplication()
    view = QQuickView()

    view.setSource("./src/view.qml")
    view.setResizeMode(QQuickView.SizeRootObjectToView)

    view.show()
    sys.exit(app.exec())
