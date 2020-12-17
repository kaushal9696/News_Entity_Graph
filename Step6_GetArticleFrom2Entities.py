import networkx as nx
import pandas as pd

df = pd.read_csv('Articles_News.csv')
IamLinks = pd.read_csv('LinkOneTOone.csv')


def Get_Article_From_Title(Person1, Person2):
    DataFrame_1 = df[(df['content'].str.contains(Person1)) & (df['content'].str.contains(Person2))]
    return DataFrame_1.iloc[0]['content']


IamLinks = IamLinks.groupby(['from', 'to']).size().reset_index()
IamLinks.rename(columns={0: 'weight'}, inplace=True)
IamLinks = IamLinks[IamLinks['from'] != IamLinks['to']]
IamLinks.reset_index(inplace=True, drop=True)
IamLinks['inverse_weight'] = IamLinks['weight'].map(lambda x: 1 / x)

G_Plot = nx.Graph()

for link in IamLinks.index:
    G_Plot.add_edge(IamLinks.iloc[link]['from'],
                    IamLinks.iloc[link]['to'],
                    weight=IamLinks.iloc[link]['weight'],
                    inverse_weight=IamLinks.iloc[link]['inverse_weight'])

Shortest_Path0 = nx.shortest_path(G_Plot,
                                  source='Donald Trump',
                                  target='Joe Biden',
                                  weight='inverse_weight')

print(Shortest_Path0)
print("-" * 25)

DataFrame_Contnt = pd.DataFrame([(Shortest_Path0[i - 1], Shortest_Path0[i]) for i in range(1, len(Shortest_Path0))],
                       columns=['Person1', 'Person2'])
DataFrame_Contnt['content'] = DataFrame_Contnt.apply(lambda x: Get_Article_From_Title(x.Person1, x.Person2), axis=1)

for Article1 in DataFrame_Contnt['content']:
    print(Article1)
    print("-" * 25)
