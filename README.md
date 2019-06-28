# VCG
This repository contains codes and literature from my internship at Harvard's Visual Computing Group (VCG).
The goal of the internship is to use and develop motif discovery algorithms to discover and analyze brain wiring diagram from different sources. 

## datasets
Contains the different datasets I have used as wiring diagrams.
Subfolders usually contain formatting python files to pre-process the data.
- Fib-25 is a dataset acquired by Janelia research campus (HHMI). It features raw EM data for the 7 medulla columns FIB-SEM reconstruction. The data can be found @[Janelia data](https://www.janelia.org/project-team/flyem/tools-and-data-release).
- yeast is a small dataset from the Kavosh algorithm repo. 
- Janelia is the Janelia 2015 Hackathon dataset. Not used in my study (probably the largest available but not most reliable).
- LGN is the extraction from Josh Morgan. @[LGN website](https://software.rc.fas.harvard.edu/lichtman/LGN/) Tree like connectome, also contains weights.
- mushroombody is also a HHMI Janelia dataset. However, we need more information to extract the edge list. 
- email is a clusterable dataset with 1005 nodes from 42 different departments with 25571 unique directed edges.


## Literature
Features the different relevant literature that I have based myself on, from algorithms to related works.

## Kavosh
Contains the source code as found @[S. Mohammadi github](https://github.com/shmohammadi86/Kavosh). This is an exact motif counting algorithm as seen in this [paper](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-10-318). In addition, it contains a wrapper.py file containing the commands to execute the algorithm and finally show the discovered motifs (analyzeZScore.py and printGraphs.py).

## visualization
Contains visualization of the graphs, using python libraries (networkx) and graphviz (dot) as rendenring tools.
