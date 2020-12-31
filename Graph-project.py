import networkx as nx
import matplotlib 
import matplotlib.pyplot as plt
import sys
from math import sqrt

def degree_sum(lst):
    return sum(lst)

def num_edges(lst):
    return int(degree_sum(lst)/2)

def is_graph(lst):
    lst.sort(reverse=True)
    vertex = lst[0]
    if len(lst) == 1 and vertex == 1:
        return True
    if sum(lst) % 2:
        return False
    # if vertex being remmoved has more edges than vertices in list, 
    # cannot be representable and caught by IndexError
    try:
        new_lst = [lst[i]-1 for i in range(vertex+1)]
    except:
        return False
    lst2 = new_lst[1:] + lst[vertex+1:] 
    if any(v<0 for v in lst2):
        return False
    elif all(i==0 for i in lst2):
        return True
    else:
        return is_graph(lst2)

def printMat(degseq, n): 
    G=nx.Graph()
    degseq.sort(reverse=True)
    # n is number of vertices  
    mat = [[0] * n for i in range(n)] 
  
    for i in range(n): 
        G.add_node(str(i))
        for j in range(i + 1, n): 
            if str(j) not in G.nodes():
                G.add_node(str(j))
            # For each pair of vertex decrement  
            # the degree of both vertex.  
            if (degseq[i] > 0 and degseq[j] > 0): 
                degseq[i] -= 1
                degseq[j] -= 1
                mat[i][j] = 1
                mat[j][i] = 1
                G.add_edge(str(i),str(j))

    # Print the result in specified form 
    print("      ", end = " ") 
    for i in range(n): 
        print(" ", "(", i, ")", end = "")  
    print() 
    print() 
    for i in range(n): 
        print(" ", "(", i, ")", end = "") 
        for j in range(n): 
            print("     ", mat[i][j], end = "")  
        print() 
    return G
        
def get_input():
    lst = []
    try:
        lst = [ int(x) for x in input("\nEnter the vertex degrees : ").strip().split()]
    except:
        print("Must input a list of numbers, try again\n")
        return get_input()
    if lst and not(lst == []):
        if (is_graph(lst)):
            print(f"Graph is Representable with {num_edges(lst)} edge{'' if num_edges(lst)==1 else 's'}!")
            print(f"It has degree sum {degree_sum(lst)}")
            print("Here is a possible representation of this graph:")
            return printMat(lst, len(lst))
        else:
            print("Graph is Not Representable!")
            quit()
            return
    else:
        print("Must input vertex degrees, try again\n")
        return get_input()

def eigen_centrality_vector(G, max_iter=100, tol=1.0e-6, decimals=None):
    x = dict([(n,1.0/len(G)) for n in G]) 
    nnodes = G.number_of_nodes()
    for i in range(max_iter):
        lastx = x
        x = dict.fromkeys(lastx, 0)
        for n in x:
            for nbr in G[n]:
                x[nbr] += lastx[n] #could add weighted edges here
        try: 
            s = 1.0/sqrt(sum(v**2 for v in x.values())) 
        except ZeroDivisionError: 
            s = 1.0
        for n in x: 
            x[n] *= s 
        err = sum([abs(x[n]-lastx[n]) for n in x]) 
        if err < nnodes*tol: 
            if decimals is not None:
              return {k:round(v,decimals) for (k,v) in x.items()}
            return x 
    raise nx.NetworkXError("""eigenvector_centrality(): power iteration failed to converge in %d iterations."%(i+1))""") 


def main():
  graph = get_input()
  print("Here are the Eigen Vector Centrality Values:")
  evcv = eigen_centrality_vector(graph, tol=1.0e-3, decimals=3)
  print(evcv)
  if graph is not None:
    print("Nodes of graph: ")
    print(graph.nodes())
    print("Edges of graph: ")
    print(graph.edges())

    nx.draw(graph)
    plt.savefig("simple_graph.png") # save as png
    plt.show() # display
    sys.exit()

if __name__== "__main__":
  main()

# G.add_node("a")
# G.add_nodes_from(["b","c"])

# G.add_edge(1,2)
# edge = ("d", "e")
# G.add_edge(*edge)
# edge = ("a", "b")
# G.add_edge(*edge)

