#!/bin/python


BASIS=3
DIM=BASIS * BASIS
HALFISH=(DIM-1)/2

def is_bold(val):
    return val % BASIS == 0

def draw_tee(tee, row, col):
    piece = ord(tee[0])
    if is_bold(row):
        piece = piece + 3
    if is_bold(col):
        piece = piece + 4
    print ("%c"%piece, end='')

cross_bars = ["┼","┿","╂","╋"]
    
def draw_cross(row, col):
    piece = 0
    if is_bold(row):
        piece = piece + 1
    if is_bold(col):
        piece = piece + 2
    print ("%c"%cross_bars[piece], end='')

FULL_SET="123456789"

def draw_set():
    print(FULL_SET, end='')

def draw_padding():
    print("         ", end='')

def pad_row():
    for col in range (DIM):
        if col % BASIS != 0  :
            print("│", end="")
        else:
            print("┃", end="")
        draw_padding()
    print("┃")

def remove_from_set(cell_set, val):
    if (val < 0) | (val > 9):
        assert("invalid value %s" %val)

def draw_cell_length(bold=False):
    for _ in range(9):
        if bold:
            print ("━", end='')
        else:
            print ("─", end='')
            
def draw_board(board):
     print ("┏",end="")
     for col in range (DIM):
         if col > 0:
             draw_tee('┬', 0, col)
         draw_cell_length(True)
     print("┓") 

     for row in range (DIM):

         if (row > 0):
             if is_bold(row) :
                 print("┣", end='')
             else:
                 print("┠", end='')
                 
             for col in range (DIM):
                 if col > 0:
                     draw_cross(row, col)
                 draw_cell_length(is_bold(row))
             if is_bold(row):                 
                 print("┫", end='')
             else:
                 print("┨", end='')
             print("") 

         pad_row()
                      
         for col in range (DIM):
             if col % BASIS != 0  :
                 print("│", end="")
             else:
                 print("┃", end="")
             print(board[row][col], end="")
         print("┃")
         pad_row()


     print("┗", end='')
     for col in range (DIM):
         if col > 0:
             draw_tee('┴', 0, col)
         draw_cell_length(True)     
     print("┛") 

board = []

for row in range(DIM):
    cur_row = []
    for col in range (DIM):
        cur_row.append(FULL_SET)
    board.append(cur_row)
     
draw_board(board)
     
