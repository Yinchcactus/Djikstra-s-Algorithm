#!/usr/bin/env python

import glob
import sys
import math
import copy
import string

# constants
START = 'A'
END = 'B'
MAX_INT = 9999999999

"""
    Read in the data file specified by file_path.
    
    Parameters
    ----------
    file_path: string
        Path to the file we want to parse.
        
    Returns
    -------
    dictionary
"""
def read_datafile(file_path):
    data = open(file_path, 'r').read()
    
    # parse then pop the first line, which contains the vertex count
    file_lines = data.splitlines()
    vertex_count = int(file_lines[0])
    file_lines.pop(0)
    
    # return the vertex count and the list of edges (deep copy edges to ensure we don't have references)
    return { 'vertex_count': vertex_count, 'edges': copy.deepcopy(file_lines) }

"""
    Build a graph out of the list of edge strings.
    
    Parameters
    ----------
    raw_edges: list
        List of strings in the form: 'A B 20' representing START END WEIGHT.
        
    Returns
    -------
    list 
"""
def build_graph(raw_edges):
    # each element of this list is a dictionary that represents an edge and its weight.
    edge_list = []
    
    # parse each of the edge strings
    for edge in raw_edges:
        edge_data = edge.split()
        edge_list.append({ 'start': edge_data[0], 'end': edge_data[1], 'weight': int(edge_data[2]) })
    
    return edge_list

"""
    Dijkstra's Algorithm
    
    Parameters
    ----------
    edges: list
        List of dicts where each dict is an edge. Eg. { 'start': 'A', 'end': 'B', 'weight': 20 }
    start: string
        A-Z letter representing the start node.
    end: string
        A-Z letter representing the end node.
    n: int
        The number of vertices in the graph.
    
    Returns
    -------
    dictionary
"""
def dijkstra(edges, start, end, n):
    graph = {}
    
    # build dict with all the vertices of the graph (using the alphabet since our inputs are alphabetical).
    for letter in list(string.uppercase[:n]):
        graph[letter] = {}
    
    # for each vertex in the graph, go through the entire edges list and connect the vertices together along with their weights
    for vertex in graph:
        for edge in edges:
            if edge['start'] == vertex:
                graph[vertex][edge['end']] = edge['weight']
    
    # keeps track of the final path. the predecessor of the start vertex is initialized to zero so we know where to begin
    predecessor = { start: 0 }
    
    # keeps track of the shortest path length to a certain vertex from the start vertex
    distances = {}
    
    # initialize all the distance values to the maximum int value
    for vertex in graph:
        distances[vertex] = MAX_INT
    
    # the starting vertex has an automatic distance of 0
    distances[start] = 0
    
    # initialize visited, a list that keeps track of all the visited vertices of the graph
    visited = [start]
    
    # run an infinite loop that begins with the starting vertex and works its way through the graph
    vertex = start
    while 1:
        if vertex == end:
            break
        else:
            # take current vertex's distance 
            current_vertex_distance = distances[vertex]
            
            # take all current vertex's adjacent neighbors
            neighbors = graph[vertex]
            
            for neighbor in neighbors:
                # check that the vertex is unvisited
                if not neighbor in visited:
                    # find the weight from the current vertex to the neighbor we are currently considering
                    temp_weight = neighbors[neighbor] + current_vertex_distance
                    
                    # if the newly calculated weight is less than the weight we have stored for that vertex, we've found a shorter path to that vertex and we can update it accordingly
                    if temp_weight < distances[neighbor]:
                        distances[neighbor] = temp_weight
                        
                        # set the predecessor of the new low cost vertex to be the current vertex
                        predecessor[neighbor] = vertex
            
            # now that all the weights are updated, select the next unvisited vertex with the lowest weight to be the next vertex we visit    
            min_value = MAX_INT
            next_vertex = 0
            
            for distance_vertex, distance_value in distances.iteritems():
                if not distance_vertex in visited:
                    if distance_value < min_value:
                        min_value = distance_value
                        next_vertex = distance_vertex
            
            # add the next vertex to the visited list
            visited.append(next_vertex)
            
            # set the next vertex to be considered as the vertex selected with the lowest weight
            vertex = next_vertex
            
    # create the final path from the adjacency list, starting from the last element
    current_vertex = end
    final_path = [end]
    total_weight = 0
    
    while 1:
        if current_vertex == start:
            break
        
        # progressively add edge weights to find the total weight of the path
        for edge in edges:
            if edge['start'] == predecessor[current_vertex] and edge['end'] == current_vertex:
                total_weight += edge['weight']
        
        # traverse the linked list backwards to find the predecessor of each vertex in the final path
        final_path.insert(0, predecessor[current_vertex])
        current_vertex = predecessor[current_vertex]

    return { 'path': final_path, 'weight': total_weight }

"""
    Driver function that gets all the files in the input/ directory, runs dijkstra's algorithm, and prints the output.
"""
def main():
    # get list of available input files
    input_files = glob.glob('./input/*')
    
    # parse each data file, build the graph, and run dijkstra's algorithm on the graph
    for input_file in input_files:
        parsed_data = read_datafile(input_file)
        edge_list = build_graph(parsed_data['edges'])

        print '\n********************************************************'
        print 'Vertices: {}'.format(parsed_data['vertex_count'])
        print 'Start: {}'.format(START)
        print 'End: {}'.format(END)
        
        output = dijkstra(edge_list, START, END, parsed_data['vertex_count'])
        
        print 'Final Weight: {}'.format(output['weight'])
        print 'Final Path: {}'.format(' '.join(output['path']))
        print ''

if __name__ == '__main__':
    main()
            