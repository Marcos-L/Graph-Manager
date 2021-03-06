# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 09:18:19 2020

@author: Marco
"""
from  PyQt6.QtWidgets  import QWidget, QVBoxLayout

from  matplotlib.backends.backend_qtagg  import  FigureCanvas

from  matplotlib.figure  import  Figure

    
class  MplWidget ( QWidget ):
    
    def  __init__ ( self ,  parent  =  None ):

        QWidget . __init__ ( self ,  parent )
        
        self . canvas  =  FigureCanvas ( Figure ())
        
        vertical_layout  =  QVBoxLayout () 
        vertical_layout . addWidget ( self . canvas )
        
        self . canvas . axes  =  self . canvas . figure . add_subplot ( 111 ) 
        self . setLayout ( vertical_layout )