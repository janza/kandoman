import sys
import random
from PySide2.QtWidgets import (
    QApplication, QLabel,
    QVBoxLayout, QWidget,
    QFrame, QHBoxLayout, QScrollArea)
from PySide2.QtGui import QDrag
from PySide2.QtCore import Slot, Qt, QMimeData

from db import get_todos

class BoldLabel(QLabel):
    def __init__(self, text):
        super().__init__('<b>' + text + '</b>')


class Filler(QLabel, QFrame):
    def __init__(self):
        super().__init__('---')
        self.setFrameStyle(QFrame.Box)
        self.setObjectName('label')
        self.setStyleSheet('#label { background: transparent; border: 2px dashed #ddd; }')


class DropZoneLabel(QLabel, QFrame):
    def __init__(self, text):
        super().__init__(text)
        self.setFrameStyle(QFrame.Box)
        self.setObjectName('label')
        self.setStyleSheet('#label { background: #fff; border: 2px solid #ddd; }')
        self.text = text
        self.setAcceptDrops(True)
        self.setWordWrap(True)

    def mouseMoveEvent(self, e):
        mimeData = QMimeData()
        mimeData.setText(self.text)

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())
        drag.exec_()

    def dragEnterEvent(self, event):
        event.ignore()

    def dragLeaveEvent(self, event):
        event.ignore()

    def dragMoveEvent(self, event):
        event.ignore()

    def dropEvent(self, event):
        self.setStyleSheet('#label { border: 2px solid #ddd; }')
        if event.source() == self:
            return

        col = self.parent()
        idx = col.layout.indexOf(self)
        col.layout.insertWidget(idx, event.source())
        event.setDropAction(Qt.MoveAction)
        event.accept()


class Column(QFrame):
    def __init__(self, text):
        QFrame.__init__(self)
        layout = QVBoxLayout()

        outsize_layout = QVBoxLayout()
        outsize_layout.addWidget(BoldLabel(text))
        outsize_layout.addLayout(layout)
        outsize_layout.addStretch()

        self.layout = layout

        self.setLayout(outsize_layout)
        self.setObjectName('frame')
        self.setAcceptDrops(True)

    def add(self, widget):
        self.layout.addWidget(widget)

    def dragMoveEvent(self, event):
        pos = event.pos()
        s = event.source()
        s.move(10, pos.y() - s.rect().center().y())
        event.accept()

    def dragEnterEvent(self, event):
        s = event.source()
        event.accept()
        self.add(s)
        self.layout.removeWidget(s)

    def dropEvent(self, event):
        self.add(event.source())
        event.setDropAction(Qt.MoveAction)
        event.accept()


class MyWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        l = QHBoxLayout()
        columns = [
            Column('To Do'),
            Column('In Progress'),
            Column('Done')
        ]
        for idx, c in enumerate(columns):
            sa = QScrollArea()
            sa.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            sa.setWidget(c)
            sa.setWidgetResizable(True)
            sa.setObjectName('scrollbox')
            sa.setStyleSheet('''
#scrollbox {
    border: none;
}

QScrollBar:vertical {
  border: none;
  background-color: rgb(240, 240, 240);
  width: 15px;
  margin: 0;
}

QScrollBar::handle:vertical {
  background-color: rgb(200, 200, 200);
  min-height: 25px;
}

 QScrollBar::add-line:vertical {
    border: none;
  background-color: rgb(241, 241, 241);
    height: 0;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}

QScrollBar::sub-line:vertical {
    border: 1px solid grey;
    background-color: rgb(241, 241, 241);
    height: 0;
    subcontrol-position: top;
    subcontrol-origin: margin;
}
                             ''')
            l.addWidget(sa)
            l.setStretch(idx, 1)

        for todo in get_todos():
            if todo.is_completed:
                columns[2].add(DropZoneLabel(todo.summary))
            elif todo.status == 'IN-PROCESS':
                columns[1].add(DropZoneLabel(todo.summary))
            else:
                columns[0].add(DropZoneLabel(todo.summary))


        self.setLayout(l)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = MyWidget()
    widget.show()

    sys.exit(app.exec_())
