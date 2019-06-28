import pandas as pd

def writeFile():

    dat = pd.read_csv('LGN.txt', sep='\t', names=['pre_id', 'post_id', 'weights'])
    # dat = dat[['pre_id', 'post_id']]
    print("Number of nodes: {}".format(len(list(set(dat.pre_id.unique()).union(set(dat.post_id.unique()) - set(dat.pre_id.unique()))))))
    print("Number of edges: {}".format(dat.weights.sum()))
    print("Number of unique edges: {}".format(len(dat)))

    f = open('../../Kavosh/networks/LGN.txt', 'w')
    f2 = open('LGN_weighted.txt', 'w')
    f.write(str(max(dat.pre_id.max(), dat.post_id.max()))+'\n')
    for ix in dat.index:
        f.write('{}\t{}\n'.format(dat.loc[ix, 'pre_id'], dat.loc[ix, 'post_id']))
        f2.write('{}\t{}\t{}\n'.format(dat.loc[ix, 'pre_id'], dat.loc[ix, 'post_id'], dat.loc[ix, 'weights']))
    f.close()
    f2.close()

if __name__=="__main__":
    writeFile()
