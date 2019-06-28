import json
import pandas as pd
import numpy as np

## Run this file from datasets/mushroombody/ directory

def writeFiles(df):
    '''Write the dataset to text file for different algorithms.'''

    ## Write Kavosh
    f = open('../../Kavosh/networks/MB.txt', 'w')
    f2 = open('../../gtrieScanner/datasets/MB.txt', 'w')
    f3 = open('MB.txt', 'w')

    f.write('{}\n'.format(max(df['pre_id'].max(), df['post_id'].max())))
    for ix in df.index:
        f.write('{}\t{}\n'.format(df.loc[ix, 'pre_id'], df.loc[ix, 'post_id']))
        f2.write('{}\t{}\n'.format(df.loc[ix, 'pre_id'], df.loc[ix, 'post_id']))
        f3.write('{}\t{}\n'.format(df.loc[ix, 'pre_id'], df.loc[ix, 'post_id']))
    f.close()
    f2.close()
    f3.close()


def processDataFrame(df, threshold=0):
    '''Remove unecessary nodes, add weights and reindex nodes.'''

    ## Get the weights for each connexion
    df['tmp'] = 1
    df['weights'] = df.groupby(['pre_id', 'post_id']).transform(np.sum)

    ## Drop unecessary rows
    df = df.drop_duplicates()

    ## Remove self looped edges
    df = df.loc[df.index[df.pre_id!=df.post_id]]

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

    ## apply threshold for weights
    if threshold>0:
        df = df.where(df.n_edge>threshold)

    return df

def getDataFrame(data, roi):
    '''Get a dataframe of all edges in the dictionnary'''

    roi = np.asarray(roi)
    body_id = roi[:,0]
    pos = np.core.defchararray.add(roi[:,1].astype(str),np.core.defchararray.add(roi[:,2].astype(str),\
     roi[:,3].astype(str)))
    body_dict = {a: b for (a,b) in zip(pos, body_id)}

    df = pd.DataFrame(columns=['pre_id', 'post_id'])

    for x in data:
        if (x['Tags'] is not None) and (x['Tags']):




        if not l['T-bar']['body ID'] == 0:
            for p in l['partners']:
                if not p['body ID'] == 0:
                    df = df.append({'pre_id': l['T-bar']['body ID'], 'post_id': p['body ID']}, ignore_index=True)

    return df


def readFile():
    '''Read the json file and return a dict.'''

    return json.load(open("MB.json", 'r')), json.load(open("datasets/mushroombody/roi.json", 'r'))


'+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+='

if __name__ == "__main__":

    print('Starting processing of Janelia dataset.')
    data, roi = readFile()
    print('Reading file.')
    df = getDataFrame(data, roi)
    df.to_pickle('MB.p')
    df = pd.read_pickle('MB.p')
    print('total number of edges before weights : {}'.format(len(df)))
    print('Processing data.')
    df = processDataFrame(df)
    print('Writing to files.')
    writeFiles(df)
    print('Finished formating.')



l = json.load(open("datasets/mushroombody/MB.json", 'r'))
ids = []
for x in l:
    if (x['Tags'] is not None) and (x['Tags']):
        id = x['Tags'][0]
        if (id not in ids):
            ids.append(id)


len(ids)
len(l)
x
l[0].keys()
l[0]

[a for a in range(100)]
