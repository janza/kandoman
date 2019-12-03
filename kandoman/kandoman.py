#!/usr/bin/env python3
import sys
import signal

from PyQt5.QtWidgets import QApplication
from kandoman.board import Board


def kandoman():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    widget = Board()
    widget.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    kandoman()
