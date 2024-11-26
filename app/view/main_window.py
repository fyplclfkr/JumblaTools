# coding: utf-8
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, QColor
from PySide6.QtWidgets import QApplication
from qfluentwidgets import NavigationItemPosition, MSFluentWindow, SplashScreen, FluentWindow
from qfluentwidgets import FluentIcon as FIF

from .setting_interface import SettingInterface
from .timelog_interface import TimelogInterface
from .dcclaunch_interface import DCCLaunchInterface

from ..common.config import cfg
from ..common.icon import Icon
from ..common.signal_bus import signalBus
from ..common import resource


class MainWindow(FluentWindow):

    def __init__(self):
        super().__init__()
        self.initWindow()

        # TODO: create sub interface
        # self.homeInterface = HomeInterface(self)
        self.settingInterface = SettingInterface(self)
        self.dcclaunchInterface = DCCLaunchInterface(self)
        self.timelogInterface = TimelogInterface(self)

        self.connectSignalToSlot()

        # add items to navigation interface
        self.initNavigation()

    def connectSignalToSlot(self):
        signalBus.micaEnableChanged.connect(self.setMicaEffectEnabled)

    def initNavigation(self):
        # self.navigationInterface.setAcrylicEnabled(True)

        # TODO: add navigation items
        self.addSubInterface(self.dcclaunchInterface, FIF.APPLICATION, 'DCCLaunch')
        self.addSubInterface(self.timelogInterface, FIF.HISTORY, '工时提交')

        # self.switchTo(self.timelogInterface)

        # add custom widget to bottom
        self.addSubInterface(
            self.settingInterface, Icon.SETTINGS, '设置', NavigationItemPosition.BOTTOM)

        self.splashScreen.finish()

    def initWindow(self):
        self.resize(1024, 768)
        # self.setMinimumWidth(760)
        self.setWindowIcon(QIcon(':/app/images/logo.png'))
        self.setWindowTitle('JumblaTools')

        self.setCustomBackgroundColor(QColor(240, 244, 249), QColor(32, 32, 32))
        self.setMicaEffectEnabled(cfg.get(cfg.micaEnabled))

        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()

        desktop = QApplication.primaryScreen().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        self.show()
        QApplication.processEvents()

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if hasattr(self, 'splashScreen'):
            self.splashScreen.resize(self.size())