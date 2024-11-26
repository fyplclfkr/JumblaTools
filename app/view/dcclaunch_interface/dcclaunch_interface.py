# -*- coding: utf-8 -*-
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QSplitter, QVBoxLayout, QLabel, QListWidgetItem
from qfluentwidgets import ListWidget

from app.common.cgtdata import CGTData
from app.common.style_sheet import StyleSheet

from .dcc_card import DccCardView

sys.path.append(r'S:\pipeline\pipeline_code')
import pipeline_core.api.core as pip
import pipeline_core.api.to_cgt as to_cgt


class DCCLaunchInterface(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.cgt_data = CGTData()

        self.mainLayout = QHBoxLayout(self)

        self.splitter = QSplitter()

        self.projectWidget = QWidget()
        # self.projectWidget.setStyleSheet('background-color: green;')
        self.projectLayout = QVBoxLayout()
        self.projectLabel = QLabel('项目列表')
        self.projectList = ListWidget()

        self.dccWidget = QWidget()
        # self.dccWidget.setStyleSheet('background-color: green;')
        self.dccLayout = QVBoxLayout()
        self.dccLabel = QLabel('DCC启动器')
        self.dccList = DccCardView()

        self.__initWidget()

    def __initWidget(self):
        self.setObjectName('DCCLaunchInterface')
        self.projectLabel.setObjectName('projectLabel')
        self.dccLabel.setObjectName('dccLabel')

        self.__initLayout()
        self.__initStyle()
        self.__connectSignalToSlot()

    def __initStyle(self):
        StyleSheet.DCCLAUNCH_INTERFACE.apply(self)

    def __initLayout(self):
        self.mainLayout.addWidget(self.splitter)

        self.splitter.addWidget(self.projectWidget)
        self.splitter.addWidget(self.dccWidget)
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 6)

        self.projectWidget.setLayout(self.projectLayout)
        self.projectLayout.addWidget(self.projectLabel)
        self.projectLayout.addWidget(self.projectList)

        self.dccWidget.setLayout(self.dccLayout)
        self.dccLayout.addWidget(self.dccLabel)
        self.dccLayout.addWidget(self.dccList)

    def __connectSignalToSlot(self):
        self.set_project_list()
        self.projectList.itemClicked.connect(self.project_list_clicked)

    def set_project_list(self):
        project_list = []
        project_list = self.cgt_data.project_list
        for project in project_list:
            _item = QListWidgetItem(project['project.full_name'])
            _item.setData(Qt.UserRole, project)
            self.projectList.addItem(_item)

    def project_list_clicked(self):
        self.dccList.clean_cards()
        project_data = to_cgt.data_transition([self.projectList.currentItem().data(Qt.UserRole)])
        # print(project_data)
        dcc_list = pip.launch._get_dcc_list(project_data[0])
        # print(dcc_list)
        for dcc_data in dcc_list:
            # print(dcc_data)
            self.dccList.add_card(dcc_data, project_data)
