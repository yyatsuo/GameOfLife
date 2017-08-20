#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import Qt, QBasicTimer
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QApplication, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen

class Board(QWidget):

    def __init__(self, width=9, height=9, offset=0, size=10):
        super().__init__()
        self.width = width
        self.height = height
        self.offset = offset
        self.size   = size
        self.cells  = []
        self.pressEventEnabled = True

        for y in range(self.height):
            for x in range(self.width):
                self.cells.append(0)

        widgetSize = self.offset*2 + self.width*self.size
        self.setMinimumSize(widgetSize, widgetSize)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawBoard(qp)
        qp.end()

    def drawBoard(self, qp):
        
        cellIndex = 0
        for y in range(self.height):
            for x in range(self.width):
                qp.setPen(QPen(Qt.gray, 1, Qt.SolidLine))
                if(self.cells[cellIndex] == 0):
                    qp.setBrush(QColor(255,250,250))
                else:
                    qp.setBrush(QColor(0,0,0))

                qp.drawRect(
                        self.offset + x*self.size,
                        self.offset + y*self.size,
                        self.size, self.size)     

                cellIndex += 1

    def clearCells(self):
        for i in range(len(self.cells)):
            self.cells[i] = 0
        self.update()

    def setCell(self, x, y, status):
        self.cells[(self.width*y) + x] = status
        self.update()

    def getCell(self, x, y):
        if x < 0 or y < 0 or x > self.width-1 or y > self.width-1:
            return 0
        else:
            return self.cells[(self.width*y) + x]

    def setCells(self, cells):
        self.cells=cells
        self.update()

    def invertCell(self, x, y):
        if self.cells[(self.width*y) + x] == 0:
            self.cells[(self.width*y) + x] = 1
        elif self.cells[(self.width*y) + x] == 1:
            self.cells[(self.width*y) + x] = 0

        self.update()

    def drawRectangles(self, qp):
        pen = QPen(Qt.gray, 1, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawRect(1,1,10,10)

        col = QColor(0,0,0)
        col.setNamedColor('#d4d4d4')
        qp.setPen(col)

        qp.setBrush(QColor(200, 0,0))
        qp.drawRect(10,15,90,60)

        qp.setBrush(QColor(25, 0, 90, 200))
        qp.drawRect(130,15,90,60)

        qp.setBrush(QColor(25, 80, 90, 200))
        qp.drawRect(250,15,90,60)

    def mousePressEvent(self, e):
        if(self.pressEventEnabled):
            x = (e.x() - self.offset)/self.size
            y = (e.y() - self.offset)/self.size
    
            if x<0 or y<0 or x>self.width or y>self.height:
                return
    
            self.invertCell(int(x), int(y))

    def enablePressEvent(self):
        self.pressEventEnabled = True

    def disablePressEvent(self):
        self.pressEventEnabled = False
        
    def nextGeneration(self):
        newCells = []
        for y in range(self.height):
            for x in range(self.width):
                neighbours = 0
                neighbours += self.getCell(x-1, y-1)
                neighbours += self.getCell(x, y-1)
                neighbours += self.getCell(x+1, y-1)
                neighbours += self.getCell(x-1, y)
                neighbours += self.getCell(x+1, y)
                neighbours += self.getCell(x-1, y+1)
                neighbours += self.getCell(x, y+1)
                neighbours += self.getCell(x+1, y+1)

                if self.getCell(x, y) == 1:
                    if neighbours < 2:
                        newCells.append(0)
                    elif neighbours == 2 or neighbours == 3:
                        newCells.append(1)
                    else:
                        newCells.append(0)
                else:
                    if neighbours == 3:
                        newCells.append(1)
                    else:
                        newCells.append(0)

        self.setCells(newCells)


class GuiMain(QWidget):

    Speed = 300

    def __init__(self, width=9, height=9, offset=0, size=10):
        super().__init__()

        self.timer = QBasicTimer()

        self.board = Board(width, height, offset, size)

        self.stepForwardBtn = QPushButton('>')
        self.stepForwardBtn.clicked.connect(self.stepForward)

        self.moveForwardBtn = QPushButton('>>')
        self.moveForwardBtn.clicked.connect(self.moveForward)

        self.pauseBtn = QPushButton('Pause')
        self.pauseBtn.clicked.connect(self.pause)
        self.pauseBtn.setEnabled(False)

        self.clearBtn = QPushButton('Clear')
        self.clearBtn.clicked.connect(self.clear)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.stepForwardBtn)
        hbox.addWidget(self.moveForwardBtn)
        hbox.addWidget(self.pauseBtn)
        hbox.addWidget(self.clearBtn)

        vbox = QVBoxLayout()
        vbox.addWidget(self.board)
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setWindowTitle('Game of Life')

        self.setLayout(vbox)
        self.show()

    def stepForward(self):
        self.board.nextGeneration()

    def moveForward(self):
        self.stepForwardBtn.setEnabled(False)
        self.pauseBtn.setEnabled(True)
        self.clearBtn.setEnabled(False)
        self.moveForwardBtn.setEnabled(False)
        self.board.disablePressEvent()
        self.timer.start(GuiMain.Speed, self)

    def clear(self):
        self.board.clearCells()

    def pause(self):
        self.stepForwardBtn.setEnabled(True)
        self.pauseBtn.setEnabled(False)
        self.clearBtn.setEnabled(True)
        self.moveForwardBtn.setEnabled(True)
        self.board.enablePressEvent()
        self.timer.stop()

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.stepForward()
        else:
            super(GuiMain, self).timerEvent(event)

if __name__=='__main__':
    app = QApplication(sys.argv)
    myGui = GuiMain(50, 50, 10, 10)
    sys.exit(app.exec_())

