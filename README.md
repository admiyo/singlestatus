# singlestatus

A partial implementation of a Sudoku solver using heuristics

thus far it implements:

* reducing cells where there is a known solved value in row/column/block
* solving cells where there is a single viable value in that row/column/block
* reducing by matched pairs

With just these three rules it solves NYT problems marked as easy or medium.