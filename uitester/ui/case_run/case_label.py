from PyQt5.QtWidgets import QLabel


class CaseLabel(QLabel):
    def __init__(self, case, parent=None):
        super(QLabel, self).__init__(parent)
        self.setText(case.name)
        self.status = None
        self.id = case.id

