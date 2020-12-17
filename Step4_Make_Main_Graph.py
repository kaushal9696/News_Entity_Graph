import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

df = pd.read_csv('Articles_News.csv')
IamLinks = pd.read_csv('LinkOneTOone.csv')

G_plot = nx.Graph()
Nodes_Here = G_plot.nodes()
Figure, axes = plt.subplots(1, 1, figsize=(105, 105))

IamLinks = IamLinks.groupby(['from', 'to']).size().reset_index()
IamLinks.rename(columns={0: 'weight'}, inplace=True)
IamLinks = IamLinks[IamLinks['from'] != IamLinks['to']]
IamLinks.reset_index(inplace=True, drop=True)

for link in IamLinks.index:
    G_plot.add_edge(IamLinks.iloc[link]['from'],
                    IamLinks.iloc[link]['to'],
                    weight=IamLinks.iloc[link]['weight'])

Position = nx.kamada_kawai_layout(G_plot)
Edges1 = nx.draw_networkx_edges(G_plot, Position, alpha=0.1, ax=axes)
Nodes1 = nx.draw_networkx_nodes(G_plot, Position, nodelist=Nodes_Here, node_size=50, ax=axes)
Labels1 = nx.draw_networkx_labels(G_plot, Position, font_size=10)
Figure.savefig('MainGraph.png', dpi=200)