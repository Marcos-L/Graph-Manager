from  PyQt6.QtWidgets  import QApplication, QMainWindow
from  PyQt6.uic  import  loadUi

from  matplotlib.backends.backend_qtagg  import  ( NavigationToolbar2QT  as  NavigationToolbar )

import  numpy  as  np 

class  Main ( QMainWindow ):
    def  __init__ ( self ):
        """ 
        Loads the .ui file and associates certain widgets with specific functions 
        """
    
        QMainWindow . __init__ ( self )

        loadUi ( "./UI_Files/MainWindow.ui" , self )
        
        self . actionPersonalizado . triggered . connect(self.Test)

        self . addToolBar ( NavigationToolbar ( self . MplWidget . canvas ,  self ))
        
    def Test(self):
        self . MplWidget . canvas . figure . clear()
        
        x = np.linspace(0,2*np.pi,100)
        a = self . MplWidget . canvas . figure . add_subplot (111)
        a . plot(x,np.sin(x))
        
        self . MplWidget . canvas . draw ()
        
app  =  QApplication ([]) 
window  =  Main () 
window . show () 
app . exec ()
