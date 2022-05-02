from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget
from PyQt6.uic  import  loadUi

class WinArc(QWidget):
    def CreateArc(self):
        print('YOLO')
        self.close()
        
    def Suicide(self):
        self.close()
        
    def  __init__ ( self , parent, mode='Create'):
        QWidget . __init__ ( self )

        loadUi ( "./UI_Files/New_Arc.ui" , self )
        
        self.parent = parent
        
        self.setParent(parent)
    
        self.setWindowFlags(Qt.WindowType.Window|Qt.WindowType.WindowStaysOnTopHint)
        
        match mode:
            case 'Edit':
                self.setWindowTitle("Edit Arc")
            case 'Delete':
                self.setWindowTitle("Delete Arc")
                self.tab_2.deleteLater()
        
        self.pushAccept.clicked.connect(self.CreateArc)
        
        self.pushCancel.clicked.connect(self.Suicide)
        
        
 
