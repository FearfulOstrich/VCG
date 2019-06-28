from graphviz import Digraph, render
import pandas as pd
from tqdm import tqdm

def readEdgeList(fname):

	f = open(fname, 'r')
	f.readline()
	edges = pd.DataFrame(columns=['source', 'target'])

	print('Reading edge list.')
	for l in tqdm(f.readlines()):
		_list = l.rstrip('\n').split('\t')
		edges = edges.append({k: int(_list[i]) for i, k in enumerate(edges.columns)}, ignore_index=True)

	return edges


def readFile(fname):

	f = open(fname, 'r')

	colors = []
	print('Reading colors.')
	for l in tqdm(f.readlines()):
		colors.append(int(l))

	color_set = list(set(colors))
	print('color_set : {}'.format(color_set))
	color_reset_dict = {color_set[i]: i for i in range(len(color_set))}
	print('color_reset_dict : {}'.format(color_reset_dict))
	return {j+1: color_reset_dict[colors[j]] for j in range(len(colors))}


def cluster(color_dict, edges):

	edges['source_c'] = edges.source.replace(color_dict)
	edges['target_c'] = edges.target.replace(color_dict)

	color_bool = (edges.source_c == edges.target_c)
	print('Number of edges left: {}'.format(color_bool.sum()))
	edges = edges[color_bool]

	return edges

def visualize(edges):

	print('Visualizing all colours.')
	f = open('graphs/n.txt', 'w')
	for c in tqdm(edges.source_c.unique()):
		tmp_df = edges[edges.source_c == c]
		if not tmp_df.empty:

			f.write('{}\n'.format(c))

			writeCluster(tmp_df, c)
			g = Digraph()
			for ix in tmp_df.index:
				g.edge(str(tmp_df.loc[ix, 'source']), str(tmp_df.loc[ix, 'target']))

		#	g.render(filename='clusters/LGN/viz/cluster{}'.format(c))

	f.close()


def writeCluster(edges, c):

	f = open('graphs/color{}.txt'.format(c), 'w+')
	for ix in edges.index:
		f.write('{}\t{}\n'.format(edges.loc[ix, 'source'], edges.loc[ix, 'target']))
	f.close()


if __name__ == '__main__':

	fname = 'colors.txt'
	fname2 = '../../datasets/email_4.txt'
	color_dict = readFile(fname)
	# print('color dict: {}'.format(color_dict))
	edges = readEdgeList(fname2)

	edges = cluster(color_dict, edges)

	visualize(edges)
