import json
from newsapi import NewsApiClient

News_API = NewsApiClient(api_key='YOUR_API_KEY')
all_articles = News_API.get_everything(q='Covid',
                                      language='en',
                                      sort_by='relevancy',
                                      page_size=10000,
                                      )

with open('data.txt', 'w') as NewFile1:
    json.dump(all_articles, NewFile1)
