from PyQt6.QtCore import Qt, QEventLoop
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt6.QtGui import QActionGroup
from PyQt6.uic  import  loadUi

from  matplotlib.backends.backend_qtagg  import  ( NavigationToolbar2QT  as  NavigationToolbar )

from Widgets.subWin import WinArc, WinNode, WinGraph

import os
import json
import PGraph as pgraph
import webbrowser
import  numpy  as  np 

class  Main ( QMainWindow ):
    def  __init__ ( self ):
        """ 
        Loads the .ui file and associates certain widgets with specific functions 
        """
    
        QMainWindow . __init__ ( self )

        loadUi ( "./UI_Files/MainWindow.ui" , self )
        
        self . AppGroup =  QActionGroup(self)
        
        self . AppGroup.addAction(self.actionApp_1)
        self . AppGroup.addAction(self.actionApp_2)
        
        self . AppGroup.setExclusive(True)
        
        self . addToolBar ( NavigationToolbar ( self . MplWidget . canvas ,  self ))
        
        self . FileName = None
        
        self . FileDir = None
        
        self . actionPersonalizado . triggered . connect(self.NewGraph)
        
        self . actionAleatorio . triggered . connect(self.NewRand)
        
        self . actionAbrir . triggered . connect(self.OpenFile)
        
        self . actionImportar_Datos . triggered . connect(self.OpenFile)
        
        self . actionGuardar . triggered . connect(self.SaveFile)

        self . actionGuardar_Como . triggered . connect(self.SaveFileAs)    
        
        self . actionExcel . triggered . connect(lambda: self.Export(0))
        
        self . actionImagen . triggered . connect(lambda: self.Export(1))
        
        self . actionPDF . triggered . connect(lambda: self.Export(2))
        
        self . actionA_1 . triggered . connect(lambda: print('Algorithm1'))
        
        self . actionImprimir . triggered . connect(self.PrintPDF)
        
        self . actionCerrar . triggered . connect(self.close)
        
        self . actionEjecucion . triggered . connect(self.AppRun)
        
        self . actionAgregar . triggered . connect(lambda: self.Node('Create'))
        
        self . actionEditar . triggered . connect(lambda: self.Node('Edit'))
        
        self . actionEliminar . triggered . connect(lambda: self.Node('Delete'))
        
        self . actionAgregar_2 . triggered . connect(lambda: self.Arc('Create'))
        
        self . actionEditar_2 . triggered . connect(lambda: self.Arc('Edit'))
        
        self . actionEliminar_2 . triggered . connect(lambda: self.Arc('Delete'))
        
        self . actionCerrar . triggered . connect(self.close)
        
        self . actionAyuda . triggered . connect(lambda: webbrowser.open(
            'https://www.youtube.com/watch?v=dQw4w9WgXcQ', new=2))
        
        self . actionAcerca_de_Grafos . triggered . connect(lambda: webbrowser.open(
            'https://github.com/Marcos-L/Graph-Manager', new=2))
        
    def OpenFile(self):
        file = QFileDialog.getOpenFileName(
            filter='JavaScript Object Notation(*.json);;Extensible Markup Language (*.XML)')
        if file[0]:
            self.FileName = file[0]
            self.FileDir = file[1][34:]
            self.type = 1
            f = json.loads(open(file[1][34:]+file[0], 'r').read())
            self.nodes = f['Nodes']
            self.arcs = f['Arcs']
            self.updateGraph()
            
    def SaveFile(self):
        if self.FileName:
            Graph = {'Nodes': self.nodes,
                     'Arcs': self.arcs}
            json_object = json.dumps(Graph, indent = 4)
  
            with open(self.FileDir+self.FileName+'.json', "w") as outfile:
                outfile.write(json_object)
        else:
            self.SaveFileAs()
            
    def SaveFileAs(self):
        file = QFileDialog.getSaveFileName(filter='Extensible Markup Language (*.XML);;JavaScript Object Notation(*.json)')
        if file[0]:
            self.FileName = file[0]
            self.FileDir = file[1][34:]
            Graph = {'Nodes': self.nodes,
                     'Arcs': self.arcs}
            json_object = json.dumps(Graph, indent = 4)
  
            with open(self.FileDir+self.FileName+'.json', "w") as outfile:
                outfile.write(json_object)
        
    def Export(self, FileType):
        match FileType:
            case 0:
                print('Excel')
            case 1:
                file = QFileDialog.getSaveFileName()
                if file[0]:
                    self.MplWidget.canvas.figure.savefig(file[1][13:]+file[0]+'.png',dpi=150)
            case 2:
                file = QFileDialog.getSaveFileName()
                if file[0]:
                    self.MplWidget.canvas.figure.savefig(file[1][13:]+file[0]+'.pdf',dpi=150)
                
    def PrintPDF(self):
        print(os.name)
                
    def NewGraph(self):
        self.nodes = {}
        self.arcs = []
        if (hasattr(self,'subWinGraph')):
            msg = "Graph maker already open."
            q = QMessageBox()
            q.setText(msg)
            q.exec()
        else:
            self.subWinGraph = WinGraph(self)
            self.subWinGraph.show()
            
    def NewRand(self):
        self.nodes = {}
        self.arcs = []
        self.AttNum = 0
        j = np.random.randint(2,20)
        for i in range(j):
            self.nodes['N'+str(i)] = {'coordinates':
                                       {'x':np.random.randint(0,100),
                                        'y':np.random.randint(0,100)},
                                      'type':'Object'
                                       }
        for i in range(j):
            for h in range(np.random.randint(0,j-1)):
                if h != i:
                    self.arcs += [['N'+str(i),'N'+str(h),10]]
        self.updateGraph()
    
    def AppRun(self):
        print(self.AppGroup.checkedAction().text())
        
    def Arc(self, mode):
        if not hasattr(self,'subWinNode'):
            self.subWinArc = WinArc(self, mode)
            self.subWinArc.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
            self.subWinArc.show()
            loop = QEventLoop()
            self.subWinArc.destroyed.connect(loop.quit)
            loop.exec()
            delattr(self,'subWinArc')
        else:
            msg = "Arc Manager already open."
            q = QMessageBox()
            q.setText(msg)
            q.exec()
        
    def Node(self, mode):
        if not hasattr(self,'subWinNode'):
            self.subWinNode = WinNode(self, mode, self.AttNum)
            self.subWinNode.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
            self.subWinNode.show()
            loop = QEventLoop()
            self.subWinNode.destroyed.connect(loop.quit)
            loop.exec()
            delattr(self,'subWinNode')
        else:
            msg = "Node Manager already open."
            q = QMessageBox()
            q.setText(msg)
            q.exec()
        
    def updateGraph(self):
        g = pgraph.UGraph()
        
        for name, info in self.nodes.items():
            g.add_vertex(name=name, coord=(info['coordinates']['x'],info['coordinates']['y']))
        
        for route in self.arcs:
            g.add_edge(route[0], route[1], cost=route[2])
        
        self . MplWidget . canvas . figure . clear()
        
        a = self . MplWidget . canvas . figure . add_subplot (111)
        g.plot(block=False, subplot=a)

        self . MplWidget . canvas . figure . tight_layout ()
        self . MplWidget . canvas . draw ()
        
app  =  QApplication ([]) 
window  =  Main () 
window . show () 

app . exec ()
