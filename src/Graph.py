from collections import defaultdict
# This class represents a directed graph using

class Node:
    def __init__(self, id, value, type):
        self.id = id
        self.value = value
        self.type = type
        # self.lrange = lrange
        # self.hrange = hrange

class Edge:
    def __init__(self, src, sink, type):
        self.src = src
        self.sink = sink
        self.type = type


# adjacency list representation
class Graph:
    # Constructor
    def __init__(self):
        # default dictionary to store graph
        self.graph = defaultdict(list)
    # function to add an edge to graph
    def addEdge(self, u_id, v_id):
        self.graph[u_id].append(v_id)
    # A function used by DFS
    def DFSUtil(self, v, visited):
        # Mark the current node as visited
        # and print it
        visited.add(v)
        # print(v, end=' ')
        # Recur for all the vertices
        # adjacent to this vertex
        for neighbour in self.graph[v]:
            if neighbour not in visited:
                self.DFSUtil(neighbour, visited)
    # The function to do DFS traversal. It uses
    # recursive DFSUtil()
    def DFS(self, v):
        # Create a set to store visited vertices
        visited = set()
        # Call the recursive helper function
        # to print DFS traversal
        self.DFSUtil(v, visited)