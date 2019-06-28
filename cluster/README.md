# cluster
Work on our proposed algorithm.

## datasets 
contains the different processed datasets to be used by gtrieScanner. (Fib-25, LGN, email_4).

## randomGraphs
Used to create random Graphs using the file *randomGraphCreator.py*. This routine shuffles the edge list so as to create a new random one without self loops.
Directly takes original datasets from '../datasets/' and stores the random graphs in folders on the same level.

## gtrieScanner
contains source file for the gtrieScanner algorithm as well as different python files for our proposal pipeline. 
- enumOriginal.py: Enumerates size k subgraph occurrences on the original graph given a dataset. Saves the result file in 'results/[dataset]/[motifSize]/'. Make sure the folder exist. 
- enumRandom.py: Looks at random graphs in '../randomGraphs/[dataset]/' and enumerate size k subgraph occurrences and save result files in 'results/[dataset]/[motifSize]/'.
- enumFullOriginal.py: Enumerates size k subgraphs occurrences on the original graph and compute motif statistics based on automatically generated random graphs.
- results/getZScores.py: Looks at the results in 'results/[dataset]/[motifSize]/' and compute ZScores for each motif and saves them in a dictionnary.
- getOccurences.py: Takes the ZScores dictionnary and identifies the occurrences of certain selected motifs in the original graph, saving the occurences (node IDs) in 'results/[dataset]/[motifSize]/'.
- getZScoreLarge.py: Computes ZScores for all subgraphs in a given graph. Combines enumOriginal.py and enumRandom.py.
- enumCluster.py: Takes clusters edge lists from '../clustered/graphs/' and compute ZScores using gtrieScanner for each of them.

## clustered
This folder contains trials (different cut from different dataset). For each trial, we need a 'colors.txt' that contains the color assigned to each node in the graph after the multi-cut. 
*createEdgeLists.py* takes the 'colors.txt' file and from the original edge list in '../datasets/' creates the edge list for each color. Can also visualize the clusters using 'dot' and 'graphviz'.
graphs folder contains the edge lists and the results of the motif discovery. 
