from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QPushButton

from uitester.config import Config


class ChooseButton(QPushButton):
    def __init__(self, *args):
        super().__init__(*args)
        self.setToolTip("add case tag")
        search_icon = QIcon()
        config = Config()
        search_icon.addPixmap(QPixmap(config.images + '/add.png'), QIcon.Normal, QIcon.Off)
        self.setIcon(search_icon)
        self.setText("Add Tags")
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedSize(90, 22)
        self.setStyleSheet(
            "QPushButton{border-width:0px; background:transparent;} ")