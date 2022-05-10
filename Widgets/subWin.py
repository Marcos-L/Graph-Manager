from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QComboBox, QLineEdit, QPushButton, QLabel, QDoubleSpinBox
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
        
class WinNode(QWidget):
    def closeEvent(self, event):
        delattr(self.parent,'subWinNode')
    
    def addAtt(self):
        Num = self.AttNum
        row = self.gridLayout.rowCount()
        DTypes = ['Int', 'Float32', 'String']
        self.Att += [[QLineEdit("Attribute Name"),
                     QComboBox(),
                     QLineEdit(),
                     QPushButton('Delete')]]
        self.Att[-1][1].addItems(DTypes)
        for i,j in zip(self.Att[-1],range(4)):
            self.gridLayout.addWidget(i,row,j)
            
        self.Att[-1][3].row = Num
        self.Att[-1][3].clicked.connect(self.delAtt)
        
        self.AttNum += 1
        
    def delAtt(self):
        self.AttNum -= 1
        Num = self.sender().row
        for i in range(4):
            self.gridLayout.removeWidget(self.Att[Num][i])
        self.Att.pop(Num)
        for i in range(Num,self.AttNum):
            self.Att[i][3].row -= 1
        
        
    def  __init__ ( self , parent, mode='Create'):
        QWidget . __init__ ( self )

        loadUi ( "./UI_Files/New_Node.ui" , self )
        
        self.Att = []
        
        self.AttNum = 0
        
        self.parent = parent
        
        self.setParent(parent)
    
        self.setWindowFlags(Qt.WindowType.Window|Qt.WindowType.WindowStaysOnTopHint)
        
        match mode:
            case 'Create':
                self.gridLayout.addWidget(QLabel("X Coordinate"),
                                          0,0)
                self.gridLayout.addWidget(QLabel("Y Coordinate"),
                                          1,0)
                self.gridLayout.addWidget(QDoubleSpinBox(),
                                          0,1,1,3)
                self.gridLayout.addWidget(QDoubleSpinBox(),
                                          1,1,1,3)
                self.gridLayout.setColumnStretch(2,15)
            case 'Edit':
                print('Golo')
                
            case 'Delete':
                print('Showlo')
                
        self.pushAdd.clicked.connect(self.addAtt)
        
        self.pushAccept.clicked.connect(lambda: print(self.gridLayout.rowCount()))
        
        self.pushCancel.clicked.connect(lambda: self.close())
        
        
 
     
 
