import json
from newsapi import NewsApiClient

News_API = NewsApiClient(api_key='c1c336393c7e462688300d3dff04c521')
all_articles = News_API.get_everything(q='Covid',
                                      language='en',
                                      page=1,
                                      sort_by='relevancy',
                                      page_size=100,
                                      )

with open('data.txt', 'w') as NewFile1:
    json.dump(all_articles, NewFile1)
