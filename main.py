from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt6.QtGui import QActionGroup
from PyQt6.uic  import  loadUi

from  matplotlib.backends.backend_qtagg  import  ( NavigationToolbar2QT  as  NavigationToolbar )

from Widgets.subWin import WinArc

import os
import json
import pgraph
import webbrowser
#import  numpy  as  np 

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
        
        self . actionAbrir . triggered . connect(self.OpenFile)
        
        self . actionGuardar . triggered . connect(self.SaveFile)

        self . actionGuardar_Como . triggered . connect(self.SaveFileAs)    
        
        self . actionExcel . triggered . connect(lambda: self.Export(0))
        
        self . actionImagen . triggered . connect(lambda: self.Export(1))
        
        self . actionPDF . triggered . connect(lambda: self.Export(2))
        
        self . actionA_1 . triggered . connect(lambda: print('Algorithm1'))
        
        self . actionImprimir . triggered . connect(self.PrintPDF)
        
        self . actionCerrar . triggered . connect(self.close)
        
        self . actionEjecucion . triggered . connect(self.AppRun)
        
        self . actionAgregar_2 . triggered . connect(lambda: self.Arc('Create'))
        
        self . actionEditar_2 . triggered . connect(lambda: self.Arc('Edit'))
        
        self . actionEliminar_2 . triggered . connect(lambda: self.Arc('Delete'))
        
        self . actionAyuda . triggered . connect(lambda: webbrowser.open(
            'https://www.youtube.com/watch?v=dQw4w9WgXcQ', new=2))
        
        self . actionAcerca_de_Grafos . triggered . connect(lambda: webbrowser.open(
            'https://github.com/Marcos-L/Graph-Manager', new=2))
        
    def OpenFile(self):
        file = QFileDialog.getOpenFileName(
            filter='Extensible Markup Language (*.XML);;JavaScript Object Notation (*.json)')
        if file[0]:
            self.FileName = file[0]
            self.FileDir = file[1]
            f = json.loads(open(file[1][35:]+file[0], 'r').read())
            self.nodes = f['Nodes']
            self.arcs = f['Arcs']
            self.updateGraph()
            
    def SaveFile(self):
        if self.FileName:
            print('Saved')
        else:
            self.SaveFileAs()
            
    def SaveFileAs(self):
        file = QFileDialog.getSaveFileName(filter='Extensible Markup Language (*.XML);;JavaScript Object Notation (*.json)')
        if file[0]:
            print('Saved')
            self.FileName = file[0]
            self.FileDir = file[1]
        
    def Export(self, FileType):
        match FileType:
            case 0:
                print('Excel')
            case 1:
                print('Imagen')
            case 2:
                print('PDF')
                
    def PrintPDF(self):
        print(os.name)
                
    def AppRun(self):
        print(self.AppGroup.checkedAction().text())
        
    def Arc(self, mode):
        self.subWinArc = WinArc(self, mode)
        
        self.subWinArc.show()
        
    def updateGraph(self):
        g = pgraph.UGraph()
        
        for name, info in self.nodes.items():
            g.add_vertex(name=name, coord=info["utm"])
        
        for route in self.arcs:
            g.add_edge(route[0], route[1], cost=route[2])
        
        p = g.path_Astar('Hughenden', 'Brisbane')
        self . MplWidget . canvas . figure . clear()
        
        a = self . MplWidget . canvas . figure . add_subplot (111)
        g.plot(block=False, subplot=a) # plot it
        g.highlight_path(p,subplot=a)  # overlay the path

        self . MplWidget . canvas . figure . tight_layout ()
        self . MplWidget . canvas . draw ()
        
app  =  QApplication ([]) 
window  =  Main () 
window . show () 

app . exec ()
