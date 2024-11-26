# -*- coding: utf-8 -*-
import functools
import sys

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QApplication, QFrame, QMainWindow
from qfluentwidgets import SingleDirectionScrollArea, IconWidget, FlowLayout, ImageLabel, InfoBarPosition, InfoBar
from app.common.icon import Icon
from app.common.style_sheet import StyleSheet
from app.common import resource

sys.path.append(r'S:\pipeline\pipeline_code')
import pipeline_core.api.core as pip


class DCCCard(QFrame):
    leftClickSignal = Signal(dict)

    def __init__(self, dcc_data, project_data):
        super().__init__()
        # self.setFixedSize(192, 250)
        self.dcc_data = dcc_data
        self.project_data = project_data
        self.setFixedWidth(192)
        self.vBoxLayout = QVBoxLayout(self)
        self.iconWidget = ImageLabel(':/app/images/{}.png'.format(dcc_data.get('dcc_name')), self)
        self.labelLayout = QVBoxLayout()
        self.titleLabel = QLabel(dcc_data.get('dcc_name'), self)
        self.descriptionLabel = QLabel(dcc_data.get('description'), self)

        self.__initWidget()

    def __initWidget(self):
        self.setCursor(Qt.PointingHandCursor)
        self.iconWidget.setBorderRadius(8, 8, 0, 0)

        self.iconWidget.setFixedSize(190, 190)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 10)

        self.labelLayout.setContentsMargins(10, 0, 10, 0)
        self.labelLayout.setSpacing(5)

        self.titleLabel.setWordWrap(True)
        self.descriptionLabel.setWordWrap(True)
        self.descriptionLabel.setToolTip(self.descriptionLabel.text())

        self.vBoxLayout.addWidget(self.iconWidget)
        self.vBoxLayout.addLayout(self.labelLayout)
        self.labelLayout.addWidget(self.titleLabel)
        self.labelLayout.addWidget(self.descriptionLabel)

        self.titleLabel.setObjectName('titleLabel')
        self.descriptionLabel.setObjectName('descriptionLabel')

        self.__connectSignalToSlot()

    def __connectSignalToSlot(self):
        self.leftClickSignal.connect(self.start_dcc)

    def start_dcc(self, dcc_data):
        dcc_name = dcc_data.get('dcc_name')
        state, message = pip.launch.start_dcc(dcc_name, self.project_data[0])
        if state:
            InfoBar.success(
                title='',
                content=message,
                orient=Qt.Horizontal,
                position=InfoBarPosition.TOP,
                parent=self.parent()
            )
        else:
            InfoBar.error(
                title='',
                content=message,
                orient=Qt.Horizontal,
                position=InfoBarPosition.TOP,
                parent=self.parent()
            )

    def find_main_window(self):
        parent = self.parent()
        while parent:
            if isinstance(parent, QMainWindow):
                return parent
            parent = parent.parent()
        return None


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print('Left click')
            self.leftClickSignal.emit(self.dcc_data)
        if event.button() == Qt.RightButton:
            print('Right click')


class DccCardView(SingleDirectionScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent, Qt.Horizontal)
        self.view = QWidget(self)
        self.hBoxLayout = FlowLayout(self.view)

        self.hBoxLayout.setContentsMargins(12, 0, 0, 0)
        self.hBoxLayout.setSpacing(12)
        self.hBoxLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.view.setObjectName('view')
        StyleSheet.DCC_CARD.apply(self)

    def add_card(self, dcc_data, project_data):
        card = DCCCard(dcc_data, project_data)
        self.hBoxLayout.addWidget(card)

    def clean_cards(self):
        count = self.hBoxLayout.count()
        print(count)
        if count > 0:
            for i in reversed(range(count)):
                self.hBoxLayout.itemAt(i).widget().setParent(None)
                self.hBoxLayout.takeAt(i)




if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = DccCardView()
    w.add_card(':/app/images/maya.png', 'Title1', 'Description1')
    w.add_card(Icon.HOUDINI, 'Title2', 'Description2')
    w.add_card(Icon.UNREAL, 'Title3', 'Description3')
    w.show()
    sys.exit(app.exec())
