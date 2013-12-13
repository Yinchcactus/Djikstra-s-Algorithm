#!/usr/bin/python

import glob
import sys
import math
import copy
import string

## read in data files

#generate list of files
fileList = glob.glob("./input/*")

#will hold the maps
fileData = []

#will hold the number of vertices in each map
vertexCount = []

for file in fileList:
    #open file for reading
    data = open(file, "r").read()
    
    #split the files on their newlines and store the vertices in a separate list
    temp = data.splitlines()
    vertexCount.append(int(temp[0]))
    temp.pop(0)
    
    #append the temp list to fileData (deep copy to ensure we don't have references)
    fileData.append(copy.deepcopy(temp))

## for each read in data set, construct a graph

#each element of this list is another list containing the edge and its weight
edgesList = []

#create the graph for each data set
for data in fileData:
    temp = []
    for edge in data:
        #parse the string into its components
        start = edge[0]
        end = edge[2]
        
        #ugly way to account for 2 and 3 digit weights in text file
        if len(edge) == 7:
            weight = int(edge[4] + edge[5] + edge[6])
        elif len(edge) == 6:
                weight = int(edge[4] + edge[5])
        else:
            weight = int(edge[4])
        
        temp.append([start, end, weight])
    edgesList.append(temp)

## define dijkstra's algorithm

#define the maximum integer value
MAX_INT = 9999999999

def dijkstra(edges, start, end, n):
    
    #create the graph dictionary
    graph = {}
    
    #construct a dictionary with all the vertices of the graph (using the alphabet since our inputs are alphabetical).
    for letter in list(string.uppercase[:n]):
        graph[letter] = {}
    
    #for each vertex in the graph, go through the entire edges list and connect the vertices together along with their weights
    for vertex in graph:
        for edge in edges:
            if edge[0] == vertex:
                graph[vertex][edge[1]] = edge[2]
    
    #initialize predecessor, a dictionary that keeps track of the final path. the predecessor of the start vertex is initialized to zero so we know where to begin
    predecessor = {start: 0}
    
    #initialize distances, a dictionary that keeps track of the shortest path length to a certain vertex from the start vertex
    distances = {}
    
    #initialize all the distance values to the maximum int value
    for vertex in graph:
        distances[vertex] = MAX_INT
    
    #the starting vertex has an automatic distance of 0
    distances[start] = 0
    
    #initialize visited, a list that keeps track of all the visited vertices of the graph
    visited = [start]
    
    #run an infinite loop that begins with the starting vertex and works its way through the graph
    vertex = start
    while 1:
        if vertex == end:
            break
        else:
            #take current vertex's distance 
            currentVertexDistance = distances[vertex]
            
            #take all current vertex's adjacent neighbors
            neighbors = graph[vertex]
            
            for neighbor in neighbors:
                #check that the vertex is unvisited
                if not neighbor in visited:
                    #find the weight from the current vertex to the neighbor we are currently considering
                    tempWeight = neighbors[neighbor] + currentVertexDistance
                    
                    #if the newly calculated weight is less than the weight we have stored for that vertex, we've found a shorter path to that vertex and we can update it accordingly
                    if tempWeight < distances[neighbor]:
                        distances[neighbor] = tempWeight
                        #set the predecessor of the new low cost vertex to be the current vertex
                        predecessor[neighbor] = vertex
            
            #now that all the weights are updated, select the next unvisited vertex with the lowest weight to be the next vertex we visit    
            minValue = MAX_INT
            nextVertex = 0
            
            for distanceVertex, distanceValue in distances.iteritems():
                if not distanceVertex in visited:
                    if distanceValue < minValue:
                        minValue = distanceValue
                        nextVertex = distanceVertex
            
            #add the next vertex to the visited list
            visited.append(nextVertex)
            
            #set the next vertex to be considered as the vertex selected with the lowest weight
            vertex = nextVertex
            
    #create the final path from the adjacency list, starting from the last element
    currentVertex = end
    finalPath = [end]
    totalWeight = 0
    while 1:
        if currentVertex == start:
            break
        
        #progressively add edge weights to find the total weight of the path
        for edge in edges:
            if edge[0] == predecessor[currentVertex] and edge[1] == currentVertex:
                totalWeight += edge[2]
        
        #traverse the linked list backwards to find the predecessor of each vertex in the final path
        finalPath.insert(0, predecessor[currentVertex])
        currentVertex = predecessor[currentVertex]

    return {"path": finalPath, "weight": totalWeight}
    
## run dijkstra's algorithm for the data that was read in

i = 0
for edges in edgesList:
    start = "A"
    end = "B"
    
    print "\n"
    print "Vertices: ", vertexCount[i]
    print "Start: ", start
    print "End:   ", end
    
    output = dijkstra(edges, start, end, vertexCount[i])
    i += 1
    
    #output shortest path and weight in the required format
    pathString = ""
    for vertex in output["path"]:
        pathString += (vertex + " ")
    
    print "Final Weight: ", output["weight"]
    print "Final Path: ", pathString
    
    outputText = str(output["weight"]) + "\n" + pathString
    
    file = open("output/Solution" + str(i) + ".txt", "w")
    file.write(outputText)
    
    
