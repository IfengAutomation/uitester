# @Time    : 2016/8/25 15:33
# @Author  : lixintong
class Style:
    def setStyle(self):
        # QPushButton
        # {border - image: url(: / images / icon_search_normal); background:transparent;} \
        #         QPushButton:hover
        # {border - image: url(: / images / icon_search_hover)} \
        #         QPushButton:pressed
        # {border - image: url(: / images / icon_search_press)}
        search_button='''
            QPushButton{

            }
        '''
        label = '''
            QLabel{
                border-radius: 4px;
                background-color: #CCCCCC;
                }
            QLabel:Hover{
                border: 2px solid #DDDDDD;
                }
        '''
        edit = '''
            QTextEdit{
                border-top-left-radius: 4px;
                border-bottom-left-radius: 4px;
                background-color: #CCCCCC;
                selection-color: #CCCCCC;
                selection-background-color: #222222;
                color: black;
                }
        '''
        btn = '''
           QPushButton{
                color: #003300;
                border-top-right-radius: 4px;
                border-bottom-right-radius: 4px;
                background-color: #CCCC99;
                font-size: 15px;
                font-family: '';
                }
            QPushButton:Hover{
                background-color: #009966;
                color: white;
                }
        '''
