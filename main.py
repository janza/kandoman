#!/usr/bin/env python3

import sys
import signal
import re
from PySide2.QtWidgets import (
    QApplication, QLabel,
    QVBoxLayout, QWidget,
    QFrame, QHBoxLayout, QScrollArea)
from PySide2.QtGui import QDrag
from PySide2.QtCore import Slot, Qt, QMimeData

from db import TodoMan

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
    def __init__(self, todo):
        text = re.sub(r'^\[.*\] ?', '', todo.summary)
        super().__init__(text)
        self.todo = todo
        self.setFrameStyle(QFrame.Box)
        self.setObjectName('label')
        self.setStyleSheet('#label { background: #fff; border: 2px solid #ddd; }')

        self.text = text
        self.setAcceptDrops(True)
        self.setWordWrap(True)

    def mouseMoveEvent(self, event):
        mime_data = QMimeData()
        mime_data.setText(self.text)

        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.setHotSpot(event.pos() - self.rect().topLeft())
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
    def __init__(self, todoman, text):
        QFrame.__init__(self)
        layout = QVBoxLayout()

        outsize_layout = QVBoxLayout()
        outsize_layout.addWidget(BoldLabel(text))
        outsize_layout.addLayout(layout)
        outsize_layout.addStretch()

        self.layout = layout
        self.todoman = todoman

        self.setLayout(outsize_layout)
        self.setObjectName('frame')
        self.setAcceptDrops(True)

    def add(self, widget):
        self.layout.addWidget(widget)

    def dragMoveEvent(self, event):
        pos = event.pos()
        source = event.source()
        source.move(10, pos.y() - source.rect().center().y())
        event.accept()

    def dragEnterEvent(self, event):
        source = event.source()
        event.accept()
        self.add(source)
        self.layout.removeWidget(source)

    def dropEvent(self, event):
        source = event.source()
        self.add(source)
        event.setDropAction(Qt.MoveAction)
        event.accept()
        self.drop(source.todo)

    def drop(self, todo):
        raise Exception('Not implemented')


class TodoColumn(Column):
    def __init__(self, todoman):
        Column.__init__(self, todoman, 'To Do')

    def drop(self, todo):
        self.todoman.todo(todo)


class InProgressColumn(Column):
    def __init__(self, todoman):
        Column.__init__(self, todoman, 'In Progress')

    def drop(self, todo):
        self.todoman.in_progress(todo)


class DoneColumn(Column):
    def __init__(self, todoman):
        Column.__init__(self, todoman, 'Done')

    def drop(self, todo):
        self.todoman.done(todo)


class CancelColumn(Column):
    def __init__(self, todoman):
        Column.__init__(self, todoman, 'Canceled')

    def drop(self, todo):
        self.todoman.cancel(todo)


class ScrollBar(QScrollArea):
    def __init__(self, containing):
        QScrollArea.__init__(self)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setWidget(containing)
        self.setWidgetResizable(True)
        self.setObjectName('scrollbox')
        self.setStyleSheet('''
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


class MyWidget(QWidget):
    todoman: TodoMan

    def __init__(self):
        QWidget.__init__(self)
        layout = QHBoxLayout()
        todoman = TodoMan()
        columns = [
            TodoColumn(todoman,),
            InProgressColumn(todoman),
            DoneColumn(todoman),
            CancelColumn(todoman)
        ]
        for idx, column in enumerate(columns):
            layout.addWidget(ScrollBar(column))
            layout.setStretch(idx, 1)

        for todo in todoman.get_todos():
            if todo.status == 'CANCELLED':
                columns[3].add(DropZoneLabel(todo))
            elif todo.is_completed:
                columns[2].add(DropZoneLabel(todo))
            elif todo.status == 'IN-PROCESS':
                columns[1].add(DropZoneLabel(todo))
            else:
                columns[0].add(DropZoneLabel(todo))


        self.setLayout(layout)



def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QApplication(sys.argv)

    widget = MyWidget()
    widget.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
