import pandas as pd
from graphviz import Digraph, render
import numpy as np

def visualize_clusters(df, c1, c2):

    df1 = df[(df.pre_label==c1)&(df.post_label==c1)]
    df2 = df[(df.pre_label==c2)&(df.post_label==c2)]
    df12 = df[((df.pre_label==c2)&(df.post_label==c1))|((df.pre_label==c1)&(df.post_label==c2))]
    print('Number of edges between clusters: {}'.format(len(df12)))

    g = Digraph('email')
    # print('Intra cluster {} edges'.format(c1))
    with g.subgraph(name='cluster_{}'.format(c1)) as c:
        c.attr(style='filled', color='white')
        c.node_attr.update(style='filled', color='lightgrey')
        for ix in df1.index:
            # print('Adding edge between node {} and {}, cluster {} to {}'.format(df1.loc[ix, 'pre_id'], df1.loc[ix, 'post_id'], df1.loc[ix, 'pre_label'], df1.loc[ix, 'post_label']))
            c.edge(str(df1.loc[ix, 'pre_id']), str(df1.loc[ix, 'post_id']))
        c.attr(label='cluster {}'.format(c1))

    # print('\nIntra cluster {} edges'.format(c2))
    with g.subgraph(name='cluster_{}'.format(c2)) as c:
        c.attr(style='filled', color='white')
        c.node_attr.update(style='filled', color='lightblue2')
        for ix in df2.index:
            # print('Adding edge between node {} and {}, cluster {} to {}'.format(df2.loc[ix, 'pre_id'], df2.loc[ix, 'post_id'], df2.loc[ix, 'pre_label'], df2.loc[ix, 'post_label']))
            c.edge(str(df2.loc[ix, 'pre_id']), str(df2.loc[ix, 'post_id']))
        c.attr(label='cluster {}'.format(c2))
        c.node('298')

    # print('\nInter cluster edges')
    for ix in df12.index:
        # print('Adding edge between node {} and {}, cluster {} to {}'.format(df12.loc[ix, 'pre_id'], df12.loc[ix, 'post_id'], df12.loc[ix, 'pre_label'], df12.loc[ix, 'post_label']))
        g.edge(str(df12.loc[ix, 'pre_id']), str(df12.loc[ix, 'post_id']))

    g.render(filename='email_4')

if __name__ == "__main__":

    # f = open('email.txt', 'r')
    # df = pd.DataFrame(columns=['pre_id', 'post_id'])
    # for l in f.readlines():
    #     _list = l.rstrip('\n').split(' ')
    #     df = df.append({'pre_id':int(_list[0]), 'post_id':int(_list[1])}, ignore_index=True)
    # f.close()
    #
    # copydf = df.copy()
    # df = copydf.copy()
    # # print(df.head())
    # df.to_csv('email.csv', index=False)
    df = pd.read_csv('email.csv')

    fc = open('email_labels.txt', 'r')
    label_dict = {}
    for l in fc.readlines():
        _list = l.rstrip('\n').split(' ')
        label_dict[int(_list[0])] = int(_list[1])
    fc.close()

    # print(label_dict)
    # print('self loops: {}'.format(len(df[df.post_id==df.pre_id])))
    df = df[df.post_id!=df.pre_id]

    df['pre_label'] = df.pre_id.replace(label_dict)
    df['post_label'] = df.post_id.replace(label_dict)

    # print('Number of nodes: {}'.format(len(unique_list)))
    # print('Number of edges: {}'.format(len(df)))
    # print('Number of unique edges: {}'.format(len(df)-len(df[df.duplicated(keep=False)])+len(df[df.duplicated(keep='first')])))

    # df[['pre_id', 'post_id']] = df[['pre_id', 'post_id']]+1
    # df = df.sort_values(by=['pre_id','post_id'], axis=0)
    # print(df.pre_label)
    # df[(df.pre_id==201)&(df.post_id==298)]

    # len(df[df.pre_label==df.post_label])

    n={j:0 for j in range(43)}
    for i in range(43):
        print('Number of edges in cluster {}: {}'.format(i, len(df[(df.pre_label==i) & (df.post_label==i)])))
        for k in label_dict.keys():
            if label_dict[k]==i:
                n[i]+=1

        print('Number of nodes in cluster {}: {}\n'.format(i, n[i]))


    # keep only 15 first labels

    lab_bool = ((df.pre_label.isin([8,9,13])) & (df.post_label.isin([8,9,13])))
    df = df[lab_bool]
    len(df)

    unique_list = sorted(list(set(df.pre_id.unique()).union(set(df.post_id.unique()) - set(df.pre_id.unique()))))
    new_ID = dict(zip(unique_list, [i for i in range(1,len(unique_list)+1)]))
    df.pre_id = df.pre_id.map(new_ID)
    df.post_id = df.post_id.map(new_ID)
    df = df.sort_values(by=['pre_id','post_id'], axis=0)

    node_list = [(n,label_dict[n]) for n in label_dict.keys() if (label_dict[n] in [8,9,13])]
    node_array = np.asarray(node_list)
    df_label = pd.DataFrame(data=node_array[:,1], index=node_array[:,0], columns=['labels'], dtype=None, copy=False)
    df_label.reset_index(inplace=True)
    df_label['index'] = df_label['index'].map(new_ID)
    df_label = df_label.dropna().astype(int)

    df_label.to_csv('../../../../email_labels4.txt', header=False, index=False)
    
    len(df[df.pre_label!=df.post_label])
    # df[(df.post_id==153) & (df.pre_id==5)]
    # df[(df.pre_id==153) & (df.post_id==5)]

    df[['pre_id', 'post_id']].to_csv('email_reduced.csv', index=False)
    df.to_csv('email4.csv', index=False)
    print('new number of nodes: {}'.format(len(unique_list)))
    print('new number of edges: {}'.format(len(df)))
    fw = open('../../../../email_4.txt', 'w')
    fw.write('{}\n'.format(len(unique_list)))
    for id in df.index:
        fw.write('{}\t{}\n'.format(df.loc[id, 'pre_id'], df.loc[id, 'post_id']))

    fw.close()

    visualize_clusters(df, 2, 3)
