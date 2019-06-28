import networkx as nx
import random

def randomGraphFromEdges(in_degree_sequence, out_degree_sequence):

    G = nx.DiGraph()

    in_list = in_degree_sequence.copy()
    out_list = out_degree_sequence.copy()

    # shuffle stublists and assign pairs by removing 2 elements at a time
    random.shuffle(in_list)
    random.shuffle(out_list)

    edge_list = []

    assert(len(in_list)==len(out_list))

    while in_list:

        # in_id = random.randint(0, n_tmp-1)
        # out_id= random.randint(0, n_tmp-1)
        random.shuffle(in_list)
        random.shuffle(out_list)
        # No multi edges or self loops.
        i = 0
        while (G.has_edge(out_list[0], in_list[0])) or\
         (out_list[0]==in_list[0]):
            # in_id = random.randint(0, n_tmp-1)
            # out_id = random.randint(0, n_tmp-1)
            random.shuffle(in_list)
            random.shuffle(out_list)
            i+=1
            if i>5:
                # print('\t\texit')
                return edge_list

        source = out_list.pop()
        target = in_list.pop()
        G.add_edge(source, target)
        edge_list.append((source, target))

    return edge_list

def main():

    for n in ['email']:#['Fib-25', 'Janelia', 'LGN']:

        f = open('../datasets/{}.txt'.format(n), 'r')

        n_nodes = int(f.readline())

        out_degree = []
        in_degree = []

        for l in f:

            [source, target] = l.split("\t")
            out_degree.append(source)
            in_degree.append(target)

        f.close()
        # print('No of edges in initial graph: {}'.format(len(in_degree)))
        for j in range(1000):
            # print('Random graph {}'.format(j))
            f = open('{}/graph{}.txt'.format(n, j), 'w')
            f.write('{}\n'.format(n_nodes))
            g = []
            while len(g)!=len(in_degree):
                g = randomGraphFromEdges(in_degree, out_degree)
                # print('\tNo of edges in random graph: {}.'.format(len(g)))
            for e in g:
                if e[0]==1:
                    print('{}\t{}'.format(e[0], e[1]))
                f.write('{}\t{}'.format(e[0], e[1]))
            f.close()

if __name__=="__main__":
    main()
