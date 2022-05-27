from PyQt6.QtCore import Qt, QEventLoop
from PyQt6.QtWidgets import QWidget, QComboBox, QLineEdit, QPushButton, QLabel, QDoubleSpinBox
from PyQt6.uic  import  loadUi

import numpy as np

class WinArc(QWidget):           
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
    def Construction(self, AttNum):
        self.gridLayout.addWidget(QLabel("X Coordinate"),
                                  0,0)
        self.gridLayout.addWidget(QLabel("Y Coordinate"),
                                  1,0)
        self.gridLayout.addWidget(QDoubleSpinBox(),
                                  0,1,1,3)
        self.gridLayout.addWidget(QDoubleSpinBox(),
                                  1,1,1,3)
        self.gridLayout.setColumnStretch(2,15)
        
        for i in range(AttNum):
            self.addAtt()
        
    def addAtt(self):
      row = self.gridLayout.rowCount()
      DTypes = ['Int', 'Float32', 'String']
      self.Att += [[QLineEdit("Attribute Name_"+str(row-1)),
                   QComboBox(),
                   QLineEdit(),]]
      self.Att[-1][1].addItems(DTypes)
      for i,j in zip(self.Att[-1],range(3)):
          self.gridLayout.addWidget(i,row,j)
          
    def addNode(self, name):
        self.parent.nodes[name] = {'coordinates':
                                           {'x':self.gridLayout.itemAtPosition(0,1).widget().value(),
                                            'y':self.gridLayout.itemAtPosition(1,1).widget().value()},
                                          'type':'Object'
                                           }
        for i in self.Att:
            match i[1].currentText():
                case 'String':
                    self.parent.nodes[self.lineEdit.text()][i[0].text()] = i[2].text() 
                case 'Int':
                    try:
                        self.parent.nodes[self.lineEdit.text()][i[0].text()] = int(i[2].text())
                    except:
                        pass
                case 'Float32':
                    try:
                        self.parent.nodes[self.lineEdit.text()][i[0].text()] = float(i[2].text())
                    except:
                        pass
                    
        self.parent.updateGraph()
        self.close()
        
    def delNode(self,name):
        for i in range(len(self.parent.arcs)-1,0,-1):
            if (self.parent.arcs[i][0] == name 
            or self.parent.arcs[i][1] == name):
                self.parent.arcs.pop(i)
                
        self.parent.nodes.pop(name)
        self.parent.updateGraph()
        self.close()
        
    def updateAtt(self):
        node = self.horizontalLayout_3.itemAt(1).widget().currentText()
        node = self.parent.nodes[node]
        self.gridLayout.itemAtPosition(0,1).widget().setValue(node['coordinates']['x']) 
        self.gridLayout.itemAtPosition(1,1).widget().setValue(node['coordinates']['y'])
        
        for i in range(2,self.gridLayout.rowCount()):
            for j in range(self.gridLayout.columnCount()):
                match j:
                    case 0:
                        self.gridLayout.itemAtPosition(i,j).widget().setText(list(node.keys())[i])
                    case 1:
                        if type(node[list(node.keys())[i-1]]) == int:
                            self.gridLayout.itemAtPosition(i,j).widget().setCurrentIndex(0)
                        elif type(node[list(node.keys())[i-1]]) == float:
                            self.gridLayout.itemAtPosition(i,j).widget().setCurrentIndex(1)
                        elif type(node[list(node.keys())[i-1]]) == str:
                            self.gridLayout.itemAtPosition(i,j).widget().setCurrentIndex(2)
                    case 2:
                        self.gridLayout.itemAtPosition(i,j).widget().setText(str(node[list(node.keys())[i]]))
        
    def  __init__ ( self , parent, mode='Create', AttNum = 0):
        QWidget . __init__ ( self )

        loadUi ( "./UI_Files/New_Node.ui" , self )
        
        self.Att = []
        
        self.parent = parent
        
        self.setParent(parent)
    
        self.setWindowFlags(Qt.WindowType.Window|Qt.WindowType.WindowStaysOnTopHint)
        
        match mode:
            case 'Create':
                self.Construction(AttNum)
                self.pushAccept.clicked.connect(lambda: self.addNode(self.lineEdit.text()))
            case 'Edit':
                self.Construction(AttNum)
                self.horizontalLayout_3.removeWidget(self.lineEdit)
                self.lineEdit.close()
                self.horizontalLayout_3.addWidget(QComboBox(), 3)
                self.horizontalLayout_3.itemAt(1).widget().addItems(self.parent.nodes.keys())
                
                self.updateAtt()
                self.horizontalLayout_3.itemAt(1).widget().textActivated.connect(self.updateAtt)
                
                self.pushAccept.clicked.connect(
                    lambda: self.addNode(self.horizontalLayout_3.itemAt(1).widget().currentText()))
                
            case 'Delete':
                self.horizontalLayout_3.removeWidget(self.lineEdit)
                self.lineEdit.close()
                self.horizontalLayout_3.addWidget(QComboBox(), 3)
                self.horizontalLayout_3.itemAt(1).widget().addItems(self.parent.nodes.keys())
                
                self.pushAccept.clicked.connect(
                    lambda: self.delNode(self.horizontalLayout_3.itemAt(1).widget().currentText()))
        

        
        self.pushCancel.clicked.connect(lambda: self.close())
        
        
class WinGraph(QWidget):    
    def CreateGraph(self):
        AttNum = self.AttNumBox.value()
        NodeNum = self.NodeNumBox.value()
        ArcNum = self.ArcsNumBox.value()
        
        self.parent.AttNum = AttNum
        
        for i in range(NodeNum):
            self.subWinNode = WinNode(self.parent, 'Create', AttNum)
            self.subWinNode.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
            self.subWinNode.show()
            loop = QEventLoop()
            self.subWinNode.destroyed.connect(loop.quit)
            loop.exec()
            delattr(self,'subWinNode')
        
        for i in range(ArcNum):
            self.subWinArc = WinArc(self.parent, 'Create')
            self.subWinArc.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
            self.subWinArc.show()
            loop = QEventLoop()
            self.subWinArc.destroyed.connect(loop.quit)
            loop.exec()
            delattr(self,'subWinArc')
        
        self.close()
    def  __init__ ( self , parent):
        QWidget . __init__ ( self )

        loadUi ( "./UI_Files/New_Graph.ui" , self )
        
        self.parent = parent
        
        self.setParent(parent)
    
        self.setWindowFlags(Qt.WindowType.Window|Qt.WindowType.WindowStaysOnTopHint)
                
        self.OkButton.clicked.connect(self.CreateGraph)
        
        self.CancelButton.clicked.connect(lambda: self.close())        
 
     
 
