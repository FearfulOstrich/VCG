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


    for x in f:
        l = x.split(sep=',')
        edges.append(map(int, l))

    assert(n_edges==len(edges))

    return edges, n_nodes, n_edges


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

def writeFiles(df):
    '''Write the dataset to text file for different algorithms.'''

    ## Write Kavosh
    f = open('../../Kavosh/networks/Fib-25.txt', 'w')
    f2 = open('../../gtrieScanner/datasets/Fib-25.txt', 'w')
    f3 = open('Fib-25.txt', 'w')
    f4 = open('Fib-25_weighted.txt', 'w')

    f.write('{}\n'.format(max(df['pre_id'].max(), df['post_id'].max())))
    for ix in df.index:
        f.write('{}\t{}\n'.format(df.loc[ix, 'pre_id'], df.loc[ix, 'post_id']))
        f2.write('{}\t{}\n'.format(df.loc[ix, 'pre_id'], df.loc[ix, 'post_id']))
        f3.write('{}\t{}\n'.format(df.loc[ix, 'pre_id'], df.loc[ix, 'post_id']))
        f4.write('{}\t{}\t{}\n'.format(df.loc[ix, 'pre_id'], df.loc[ix, 'post_id'], df.loc[ix, 'n_edge']))
    f.close()
    f2.close()
    f3.close()
    f4.close()


def processDataFrame(df, threshold=0):
    '''Remove unecessary nodes, add weights and reindex nodes.'''

    ## Remove self looped edges
    df = df[df.pre_id!=df.post_id]

    ## apply threshold for weights
    if threshold>0:
        df = df[df.n_edge>threshold]

    ## Some neurons do not have edges. We need to remove their IDs and reset the IDs.
    unique_list = list(set(df.pre_id.unique()).union(set(df.post_id.unique()) - set(df.pre_id.unique())))
    new_ID = dict(zip(unique_list, [i for i in range(1,len(unique_list)+1)]))
    df.pre_id = df.pre_id.map(new_ID)
    df.post_id = df.post_id.map(new_ID)
    print('Number of nodes : {}'.format(len(unique_list)))
    print('Number of unique edges : {}'.format(len(df)))
    print('Total number of edges : {}'.format(df.n_edge.sum()))
    print('Max weight in edges : {}\nAverage weight : {}'.format(df.n_edge.max(), df.n_edge.mean()))

    ## sort nodes
    df = df.sort_values(by=['pre_id','post_id'], axis=0)

    return df

def plotGraph(df, sub_graph_viz_size):

    dot = Digraph()
    if sub_graph_viz_size==0 and len(df)<500:
        for ix in df.index:
            dot.edge(str(df.loc[ix,'pre_id']), str(df.loc[ix,'post_id']))
        dot.render(filename='../../visualization/Fib-25/Fib-25.pdf')
    elif sub_graph_viz_size==0 and len(df)>=500:
        print('Graph too big for rendering.')
    else:
        sub_df = pruneGraph(df, sub_graph_viz_size)
        for ix in sub_df.index:
            dot.edge(str(sub_df.loc[ix,'pre_id']), str(sub_df.loc[ix,'post_id']))
        dot.render(filename='../../visualization/Fib-25/Fib-25_sub_'+str(sub_graph_viz_size)+'.pdf')

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
    f = open('Fib25.txt', 'r')

    edge_list, n_nodes, n_edges = readFile(f)

    print('Number of segments initially: {}'.format(n_nodes))

    ## close raw file.
    f.close()

    ## Format the edges to a dataframe.
    df_edges = pd.DataFrame(edge_list, columns=['post_id', 'pre_id', 'n_edge'])
    ## Save as a pickle file.
    df_edges.to_pickle('Fib-25.p')

    print('Total number of edges: {}'.format(df_edges.n_edge.sum()))
    print('Total number of unique edges: {}'.format(len(df_edges)))
    print('\n')

    ## Format for Kavosh
    df = processDataFrame(df_edges, threshold)

    ## Render the graph
    if visualize:
        plotGraph(df, sub_graph_viz_size)

    ## Format for GtrieScanner
    writeFiles(df)

if __name__=="__main__":
    print('Formatting Fib-25 dataset.')
    main(visualize=True, sub_graph_viz_size=0, threshold=10)
    print('Done formatting.')
