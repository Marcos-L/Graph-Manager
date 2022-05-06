from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget
from PyQt6.uic  import  loadUi

import numpy as np

class WinArc(QWidget):
    def closeEvent(self, event):
        delattr(self.parent,'subWinArc')
            
    def CreateArc(self):
        if self.comboOrigin.currentText() != self.comboDst.currentText():
            self.parent.arcs += [[self.comboOrigin.currentText(),
                                  self.comboDst.currentText(),
                                  10]]
            self.parent.updateGraph()
        self.close()
        
    def DestroyArc(self):
        for i in range(len(self.parent.arcs)):
            if (self.parent.arcs[i][0] == self.comboOrigin.currentText() 
            and self.parent.arcs[i][1] == self.comboDst.currentText()):
                self.parent.arcs.pop(i)
                self.parent.updateGraph()
                self.close()
                break;
                
    def UpdateDst(self, text):
        Dst = []
        self.comboDst.clear()
        
        for node in self.parent.arcs:
            if node[0] == text:
                Dst += [node[1]]
                
        self.comboDst.addItems(np.unique(Dst))
              
    def  __init__ ( self , parent, mode='Create'):
        QWidget . __init__ ( self )

        loadUi ( "./UI_Files/New_Arc.ui" , self )
        
        self.parent = parent
        
        self.setParent(parent)
    
        self.setWindowFlags(Qt.WindowType.Window|Qt.WindowType.WindowStaysOnTopHint)
        
        match mode:
            case 'Create':
                self.comboOrigin.addItems(self.parent.nodes.keys())                
                self.comboDst.addItems(self.parent.nodes.keys())
                
                self.pushAccept.clicked.connect(self.CreateArc)
                
            case 'Edit':
                Origins = []
                Dst = []
                self.setWindowTitle("Edit Arc")
                
                for node in self.parent.arcs:
                    Origins += [node[0]]
                    if node[0] == Origins[0]:
                        Dst += [node[1]]
                self.comboOrigin.addItems(np.unique(Origins))
                self.comboDst.addItems(np.unique(Dst))
                
                self.comboOrigin.textActivated.connect(self.UpdateDst)
                
                #self.pushAccept.clicked.connect(self.UpdateArc)
            case 'Delete':
                Origins = []
                Dst = []
                self.setWindowTitle("Delete Arc")
                self.tab_2.deleteLater()
                
                for node in self.parent.arcs:
                    Origins += [node[0]]
                    if node[0] == Origins[0]:
                        Dst += [node[1]]
                self.comboOrigin.addItems(np.unique(Origins))
                self.comboDst.addItems(np.unique(Dst))
                
                self.comboOrigin.textActivated.connect(self.UpdateDst)
                
                self.pushAccept.clicked.connect(self.DestroyArc)
                
        self.pushCancel.clicked.connect(lambda: self.close())
        
        
 
