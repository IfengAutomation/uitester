# @Time    : 2016/8/25 19:12
# @Author  : lixintong
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit,QPushButton,QHBoxLayout


class TestEdit():
    def __init__(self):
        m_pSearchLineEdit = QLineEdit()
        pSearchButton = QPushButton()
        pSearchButton.setCursor(Qt.PointingHandCursor)
        pSearchButton.setFixedSize(22, 22)
        pSearchButton.setToolTip("搜索")
        pSearchButton.setStyleSheet("QPushButton{border-image:url(:/images/icon_search_normal) background:transparent} \
                                             QPushButton:hover{border-image:url(:/images/icon_search_hover)} \
                                             QPushButton:pressed{border-image:url(:/images/icon_search_press)}")

        # // 防止文本框输入内容位于按钮之下

        margins = m_pSearchLineEdit.textMargins()
        m_pSearchLineEdit.setTextMargins(margins.left(), margins.top(), pSearchButton.width(), margins.bottom())
        m_pSearchLineEdit.setPlaceholderText("请输入搜索内容")

        pSearchLayout = QHBoxLayout()
        pSearchLayout.addStretch()
        pSearchLayout.addWidget(pSearchButton)
        pSearchLayout.setSpacing(0)
        pSearchLayout.setContentsMargins(0, 0, 0, 0)
        m_pSearchLineEdit.setLayout(pSearchLayout)

if __name__ == '__main__':
    m_pSearchLineEdit = QLineEdit()
    pSearchButton = QPushButton()
    pSearchButton.setCursor(Qt.PointingHandCursor)
    pSearchButton.setFixedSize(22, 22)
    pSearchButton.setToolTip("搜索")
    pSearchButton.setStyleSheet("QPushButton{border-image:url(:/images/icon_search_normal) background:transparent} \
                                             QPushButton:hover{border-image:url(:/images/icon_search_hover)} \
                                             QPushButton:pressed{border-image:url(:/images/icon_search_press)}")

    # // 防止文本框输入内容位于按钮之下
    margins = m_pSearchLineEdit.textMargins()
    print(margins.left(), margins.top(), pSearchButton.width(), margins.bottom())
    m_pSearchLineEdit.setTextMargins(margins.left(), margins.top(), pSearchButton.width(), margins.bottom())
    m_pSearchLineEdit.setPlaceholderText("请输入搜索内容")

    pSearchLayout = QHBoxLayout()
    pSearchLayout.addStretch()
    pSearchLayout.addWidget(pSearchButton)
    pSearchLayout.setSpacing(0)
    pSearchLayout.setContentsMargins(0, 0, 0, 0)
    m_pSearchLineEdit.setLayout(pSearchLayout)