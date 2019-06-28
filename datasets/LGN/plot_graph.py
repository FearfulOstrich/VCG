from graphviz import Digraph, render

def main(filename):

    f = open('{}.txt'.format(filename), 'r')
    dot = Digraph()

    for x in f:
        l = x.split('\t')
        if int(l[2])>2:
            dot.edge(l[0], l[1])

    dot.render('{}_full.png'.format(filename))

if __name__ == "__main__":
    main('LGN')
