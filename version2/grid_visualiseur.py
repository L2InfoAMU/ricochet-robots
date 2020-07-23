import sys
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QMainWindow, QWidget, QAction, QFileDialog

from robot import Board

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.label = QtWidgets.QLabel()
        self.create_menu()


    def create_menu(self) :
        menuBar = self.menuBar()
        file_menu = menuBar.addMenu("&Fichier")

        openAction = QAction(QIcon('open.png'),'&Open',self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('charger une grille')
        openAction.triggered.connect(self.open_grid)

        file_menu.addAction(openAction)


    def open_grid(self) :
        filename, filter = QFileDialog.getOpenFileName(self , 'selectionner un fichier contenant une grille','./grids','*.json')
        print(filename)
        board, = Board.load_from_json(filename) 
        canvas = self.draw_Board ( board)
        
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)

    def draw_Board(self,board):
        canvas = QtGui.QPixmap(800, 800)
        canvas.fill(Qt.white)
        painter = MyPainter( 50 , canvas )
        # painter.scale(25, 25)
        names=["Empty","N","E","EN","S","NS","ES","ENS","W","NW","EW","ENW","SW","NSW","ESW","ENSW"]
        images = [QtGui.QPixmap("./images/"+name+".bmp", format="bmp")  for name in names]

        grid = board.grid
        height , width = board.height,board.width

        for i in range(height) :
            for j in range (width) :
                cell = int(grid[i][j].walls)
                painter.drawPixmap(j,i, images[cell])                              
        painter.end()
        return canvas
        
class MyPainter(QtGui.QPainter) :
	
	def __init__(self,scale , *args ,**kwargs) :
	    super().__init__(*args , **kwargs)
	    self.scale = scale
	def drawPixmap(self, x,y, image) :
	    
	    super().drawPixmap(QtCore.QPoint(self.scale*x,self.scale*y) , image)
  
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
