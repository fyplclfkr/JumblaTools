# -*- coding: utf-8 -*-
import sys

import sys

from PySide6.QtWidgets import QWidget, QApplication


class TimelogInterface(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__initWidget()

    def __initWidget(self):
        self.setObjectName('TimelogInterface')
        self.__initLayout()
        self.__initStyle()
        self.__connectSignalToSlot()
        
    def __initStyle(self):
        pass    

    def __initLayout(self):
        pass
        
    def __connectSignalToSlot(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = TimelogInterface()
    w.show()
    app.exec()