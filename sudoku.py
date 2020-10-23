#!/bin/python


BASIS=3
DIM=BASIS * BASIS
HALFISH=(DIM-1)/2





def draw_set():
    print("123456789", end='')


def draw_cell_length(bold=False):
    for _ in range(9):
        if bold:
            print ("━", end='')
        else:
            print ("─", end='')

    
def draw_board():
     print("┏", end='') 
     for col in range (DIM - 1):
         draw_cell_length(True)
         if col % BASIS == BASIS -1:
             print("┳", end="")
         else:
             print ("┯", end='')
     draw_cell_length(True)
     print("┓") 

     for row in range (DIM):
         for col in range (DIM):
             if col % BASIS != 0  :
                 print("│", end="")
             else:
                 print("┃", end="")
             draw_set()
         print("┃")

         if (row < 8):
             print("┠", end='') 
             for col in range (DIM-1):
                 draw_cell_length()
                 print ("┼", end='')
             draw_cell_length()
             print("┤") 

     print("┗", end='') 
     for col in range (DIM-1):
         draw_cell_length(True)
         print ("┷", end='')
     draw_cell_length(True)
     print("┛") 

draw_board()
     
