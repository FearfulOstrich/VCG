import json
import pandas as pd
import numpy as np
from graphviz import Digraph, render


## Run this file from datasets/Janelia/ directory

def writeFiles(df):
    '''Write the dataset to text file for different algorithms.'''

    ## Write Kavosh
    f = open('../../Kavosh/networks/Janelia.txt', 'w')
    f2 = open('../../gtrieScanner/datasets/Janelia.txt', 'w')
    f3 = open('Janelia.txt', 'w')
    f4 = open('Janelia_weighted.txt', 'w')

    f.write('{}\n'.format(max(df['pre_id'].max(), df['post_id'].max())))
    for ix in df.index:
        f.write('{}\t{}\n'.format(df.loc[ix, 'pre_id'], df.loc[ix, 'post_id']))
        f2.write('{}\t{}\n'.format(df.loc[ix, 'pre_id'], df.loc[ix, 'post_id']))
        f3.write('{}\t{}\n'.format(df.loc[ix, 'pre_id'], df.loc[ix, 'post_id']))
        f4.write('{}\t{}\t{}\n'.format(df.loc[ix, 'pre_id'], df.loc[ix, 'post_id'], df.loc[ix, 'weights']))
    f.close()
    f2.close()
    f3.close()
    f4.close()


def processDataFrame(df, threshold=0):
    '''Remove unecessary nodes, add weights and reindex nodes.'''

    ## Get the weights for each connexion
    df['tmp'] = 1
    df['weights'] = df.groupby(['pre_id', 'post_id']).transform(np.sum)

    ## Drop unecessary rows
    df = df.drop_duplicates()

    ## Remove self looped edges
    df = df.loc[df.index[df.pre_id!=df.post_id]]

    ## apply threshold for weights
    if threshold>0:
        df = df[df.weights>threshold]

    ## Some neurons do not have edges. We need to remove their IDs and reset the IDs.
    unique_list = list(set(df.pre_id.unique()).union(set(df.post_id.unique()) - set(df.pre_id.unique())))
    new_ID = dict(zip(unique_list, [i for i in range(1,len(unique_list)+1)]))
    df.pre_id = df.pre_id.map(new_ID)
    df.post_id = df.post_id.map(new_ID)
    print('Number of nodes : {}'.format(len(unique_list)))
    print('Number of edges : {}'.format(len(df)))
    print('Max weight in edges : {}\nAverage weight : {}'.format(df.weights.max(), df.weights.mean()))

    ## sort nodes
    df = df.sort_values(by=['pre_id','post_id'], axis=0)

    return df

def getDataFrame(data):
    '''Get a dataframe of all edges in the dictionnary'''

    list = data['data']
    df = pd.DataFrame(columns=['pre_id', 'post_id'])

    for l in list:
        if not l['T-bar']['body ID'] == 0:
            for p in l['partners']:
                if not p['body ID'] == 0:
                    df = df.append({'pre_id': l['T-bar']['body ID'], 'post_id': p['body ID']}, ignore_index=True)

    return df

def plotGraph(df, sub_graph_viz_size):

    dot = Digraph()
    if sub_graph_viz_size==0 and len(df)<1000:
        for ix in df.index:
            dot.edge(str(df.loc[ix,'pre_id']), str(df.loc[ix,'post_id']))
        dot.render(filename='../../visualization/Janelia/Janelia.pdf')
    elif sub_graph_viz_size==0 and len(df)>=1000:
        print('Graph too big for rendering.')
    else:
        sub_df = pruneGraph(df, sub_graph_viz_size)
        for ix in sub_df.index:
            dot.edge(str(sub_df.loc[ix,'pre_id']), str(sub_df.loc[ix,'post_id']))
        dot.render(filename='../../visualization/Janelia/Janelia_'+str(sub_graph_viz_size)+'.pdf')

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

    sub_df = df.sort_values(by=['weights'], axis=0)
    return sub_df.iloc[:n]

def readFile():
    '''Read the json file and return a dict.'''

    return json.load(open("Janelia.json", 'r'))


'+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+='

if __name__ == "__main__":

    # print('Starting processing of Janelia dataset.')
    # data = readFile()
    # print('Reading file.')
    # df = getDataFrame(data)
    # df.to_pickle('Janelia.p')
    df = pd.read_pickle('Janelia.p')
    print('total number of edges before weights : {}'.format(len(df)))
    print('Processing data.')
    df = processDataFrame(df, 5)
    # print('Rendering graph')
    # plotGraph(df, 400)
    print('Writing to files.')
    writeFiles(df)
    print('Finished formating.')
