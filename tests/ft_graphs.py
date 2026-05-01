
# ============= ------------------------------------ ==================
# ============= EVERYTHING NEED TO KNOW ABOUT GRAPHS ==================
# ============= ------------------------------------ ==================
import math

"""Graph Data Structure represented using Adjacency Matrix"""
# def add_edge(mat, i, j):
#     # Add an edge between two vertices
#     mat[i][j] = 1
#     mat[j][i] = 1
    
# def display_matrix(mat):
#     # Display the adjacency matrix
#     for row in mat:
#         print(" ".join(map(str, row)))  
        
        
# if __name__ == "__main__":
#     V = 4  # Number of vertices
#     mat = [[0] * V for _ in range(V)]  

#     print("the matrix before:")
#     display_matrix(mat)

#     # Add edges to the graph
#     add_edge(mat, 0, 1)
#     add_edge(mat, 0, 2)
#     add_edge(mat, 1, 2)
#     add_edge(mat, 2, 3)

#     # Optionally, initialize matrix directly
#     """
#     mat = [
#         [0, 1, 0, 0],
#         [1, 0, 1, 0],
#         [0, 1, 0, 1],
#         [0, 0, 1, 0]
#     ]
#     """

#     # Display adjacency matrix
#     print("Adjacency Matrix:")
#     display_matrix(mat)
    
    
    
    
"""Graph Data Structure represented using Adjacency List"""

# first initializing an array of lists (vertices/nodes)
# adding edges to each node by indexing to it like adj[0].append(1)
# the previous line means that the 1st node is connected to the seconde one 
# this is a case which the edge goes in only one direction.

def add_edge(adj, i, j):
    adj[i].append(j)
    # adj[j].append(i)  # Undirected

def display_adj_list(adj):
    for i in range(len(adj)):
        label = chr(ord("A") + i)
        print(f"Node {label}:", end="")
        for j in adj[i]:
            print(f" -> {j}", end=" ")
        print()

# Create a graph with 4 vertices and no edges
V = 3
adj = [[] for _ in range(V)]
print("Graph with 4 nodes -> before adding edges/connections")
display_adj_list(adj)

print(chr(10))
# Now add edges one by one
add_edge(adj, 1, 0)
add_edge(adj, 1, 2)
add_edge(adj, 2, 0)
# add_edge(adj, 2, 3)

print("Adjacency List Representation:")
display_adj_list(adj)


#other tests
# malanihaya = float('inf')

# print(malanihaya + 1)

# add_always_8 = lambda x: x+8
# print(add_always_8(7))