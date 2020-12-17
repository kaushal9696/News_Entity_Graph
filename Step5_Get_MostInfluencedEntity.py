import networkx as nx
import pandas as pd
import seaborn as sns

df = pd.read_csv('Articles_News.csv')
IamLinks = pd.read_csv('LinkOneTOone.csv')

List_1 = []
List_2 = []

IamLinks = IamLinks.groupby(['from', 'to']).size().reset_index()
IamLinks.rename(columns={0: 'weight'}, inplace=True)
IamLinks = IamLinks[IamLinks['from'] != IamLinks['to']]
IamLinks.reset_index(inplace=True, drop=True)
IamLinks['inverse_weight'] = IamLinks['weight'].map(lambda x: 1 / x)

G = nx.Graph()

for link in IamLinks.index:
    G.add_edge(IamLinks.iloc[link]['from'],
               IamLinks.iloc[link]['to'],
               weight=IamLinks.iloc[link]['weight'],
               inverse_weight=IamLinks.iloc[link]['inverse_weight'])

ec_dict = nx.eigenvector_centrality(G, max_iter=1000, weight='weight')

for node in G.nodes():
    List_1.append(node)
    List_2.append(ec_dict[node])

DataFrame_Cent = pd.DataFrame(data={'Entity': List_1,
                                     'Vector': List_2})

Top_Most_Inf = DataFrame_Cent.sort_values('Vector', ascending=False).head(20)
Top_Most_Inf.reset_index(inplace=True, drop=True)

Plot_BAR_Graph = sns.barplot(data=Top_Most_Inf,
                             x='Vector',
                             y='Entity',
                             dodge=False,
                             orient='h',
                             hue='Vector',
                             palette='viridis')

Plot_BAR_Graph.set_yticks([])
Plot_BAR_Graph.set_ylabel('')
Plot_BAR_Graph.set_xlabel('Eigenvector centrality')
Plot_BAR_Graph.set_xlim(0, max(Top_Most_Inf['Vector']) + 0.1)
Plot_BAR_Graph.legend_.remove()
Plot_BAR_Graph.tick_params(labelsize=5)
Plot_BAR_Graph.set_title('TOP MOST INFLUENCED ENTITIES')

for i in Top_Most_Inf.index:
    Plot_BAR_Graph.text(Top_Most_Inf.iloc[i]['Vector'] + 0.005, i + 0.25, Top_Most_Inf.iloc[i]['Entity'])

sns.despine()
Plot_BAR_Graph.get_figure().savefig('Most_Influence.png', dpi=1000)
