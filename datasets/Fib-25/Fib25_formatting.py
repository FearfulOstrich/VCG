import numpy as np
import pandas as pd
from graphviz import Digraph, render
import os

def readFile(f):
    '''Function to read the file and obtain edge list as well as number of nodes and edges.
    ARGS:
        - f : opened file.
    RETURNS:
        - dot : networkx graph.
        - edges : list of all edges in the graph.
        - n_nodes : number of nodes in the graph.
        - n_edges : number of edges in the graph.
    '''

    #create edge_list
    edges = []
    n_nodes = int(f.readline())
    n_edges = int(f.readline())
    assert(n_edges>0)
    assert(n_nodes>0)

    dot = Digraph()

    for x in f:
        l = x.split(',')
        edges.append(map(int, l))
        dot.edge(l[1], l[0])

    assert(n_edges==len(edges))

    return dot, edges, n_nodes, n_edges


def pruneGraph(df, n):
    '''Function to prune the edge list, and only keep n edges from the graph.
    ARGS:
        - df : pandas DataFrame containing the edge list.
        - n : integer number of edges to keep.
    RETURNS:
        - pandas DataFrame containing the pruned list of edges.
    '''

    if n>df.shape[0]:
        return df.sort_values(by=['pre_id','post_id'], axis=0)

    sub_df = df.sort_values(by=['pre_id','post_id'], axis=0)
    return sub_df.iloc[:n]

def writeKavoshFile(fname, df, n_nodes, threshold=0):
    '''Function to write the edge list in a txt file in such format as it is readable for Kavosh algorithm.
    ARGS :
        - fname : filename to save the data in.
        - df : pandas DataFrame containing the edge list and optionally the weights.
        - n_nodes : Number of nodes in the graph.
        - threshold : weight threshold to consider an edge as existing, if weight is lower or equal the edge is discarded.
    '''

    ## There seems to be self looped edges.
    # print(df[df.pre_id==df.post_id])
    ## Remove self looped edges.
    df = df[df.pre_id!=df.post_id]

    ## Some neurons do not have edges. We need to remove their IDs and reset the IDs.
    unique_list = list(set(df.pre_id.unique()).union(set(df.post_id.unique()) - set(df.pre_id.unique())))
    new_ID = dict(zip(unique_list, [i for i in range(1,len(unique_list)+1)]))
    df.pre_id = df.pre_id.map(new_ID)
    df.post_id = df.post_id.map(new_ID)

    ## sort nodes
    df = df.sort_values(by=['pre_id','post_id'], axis=0)

    ## apply threshold for weights
    if threshold>0:
        df = df.where(df.n_edge>threshold)

    ## check if file exists
    if os.path.isfile('../../Kavosh/networks/'+fname):
        os.system('rm ../../Kavosh/networks/'+fname)

    ## write to file
    f = open('../../Kavosh/networks/'+fname, 'wb')
    f.write(str(len(unique_list))+'\n')
    for ix in df.index:
        f.write(str(df.loc[ix, 'pre_id'])+' '+str(df.loc[ix, 'post_id'])+'\n')

    ## close file
    f.close()

def main(visualize=False, sub_graph_viz_size=100, threshold=0):
    '''Main function of this module. Module is used to format and visualize the Fib-25 graph dataset.
    ARGS:
        - visualize : Boolean. If true, will save a png of the dataset.
        - sub_graph_viz_size : Size of the rendered subgraph. if 0, the full graph will be rendered.'''

    cwd = os.getcwd()
    l = cwd.split('/')[-3:]
    target_cwd = 'PART1/datasets/Fib-25'
    if '/'.join(l) != target_cwd:
        print('/'.join(l))
        raise IOError('Please go to \'{}\'. You\'re current working directory is \'{}\'.'.format(target_cwd, cwd))

    ## open the raw file.
    f = open('Fib25.txt', 'rb')

    dot, edge_list, n_nodes, n_edges = readFile(f)

    ## close raw file.
    f.close()

    ## Format the edges to a dataframe.
    df_edges = pd.DataFrame(edge_list, columns=['post_id', 'pre_id', 'n_edge'])
    ## Save as a pickle file.
    df_edges.to_pickle('Fib-25.p')

    ## render the graphs
    if visualize:
        if sub_graph_viz_size==0 and n_edges<250:
            dot.render(filename='../../visualization/'+l[-1])
        elif sub_graph_viz_size==0 and n_edges>=250:
            print('Graph too big for rendering.')
        else:
            sub_df = pruneGraph(df_edges, sub_graph_viz_size)
            sub_dot = Digraph()
            for x in sub_df.values:
                sub_dot.edge(str(x['pre_id']), str(x['post_id']))
            sub_dot.render(filename='../../visualization/'+l[-1]+'_sub_'+str(sub_graph_viz_size))

    ## Format for Kavosh
    writeKavoshFile(l[-1], df_edges, n_nodes)


if __name__=="__main__":
    print('Formatting Fib-25 dataset.')
    main(visualize=False, sub_graph_viz_size=100, threshold=0)
    print('Done formatting.')
