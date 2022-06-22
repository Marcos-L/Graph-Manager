import pyphi as phi
import numpy as np

def CMatrix(nodes, arcs):
    '''
    A function which recieves the nodes and arcs of a graph and determines the Conectivity Matrix
    
    ...

    Parameters
    ----------
    nodes: dict
        The dictionary containing the nodes of the graph.
        Example: nodes = {  a:{'att':1},
                            b:{'att':2},
                            c:{'att':3}}
    arcs: list
        The list of arcs of the graph.
        Example: arcs = [   ['a','b'],
                            ['a','c'],
                            ['b','c'],
                            ['c','a']]
    
    ...

    Outputs
    ----------
    CM: np.array
        The Connectivity Matrix.
        Example: CM = [[0,1,1]
                       [0,0,1]
                       [1,0,0]]
    '''
    CM = np.zeros((len(nodes),len(nodes)))
    keys = list(nodes.keys())
    for j in range(len(keys)):
        for i in arcs:
            if i[0] == keys[j]:
                CM[j,keys.index(i[1])] = 1
    return CM