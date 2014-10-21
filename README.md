# Dijkstra's Algorithm

Python implementation of Dijkstra's Algorithm to find the minimum spanning tree of a directed weighted graph.

----------------------------------

## How to format input files

The graph builder expects a certain format for input files. It will understand the input file as long as it follows these rules:

1. The first line of the file is an integer with the number of vertices the graph.

2. The starting point for each graph is labeled `A`, and the ending point is labeled `B`. The first line of each input file represents the number of vertices in the graph.

3. Letters must be used in alphabetical order. For instance, if your graph has 5 vertices you can only use the letters A, B, C, D, E.

4. Each line (after the first line) is in the form START END WEIGHT, delimited by spaces.

Sample input files are included in the `input` directory. Without modification, the script will automatically read in all files in the input directory.

Obviously you can change the code to suit your needs, but it's important to understand how it's currently set up.

####E.g.
In the example input snippet below, there are 10 vertices in the graph (A...J)

```
10
A J 18
A H 79
A I 81
J G 24
J F 76
G F 2
G H 50
F E 4
E D 2
D H 20
H C 50
I D 6
I C 97
I J 27
C B 22
```