import csv
import json

csv1 = open('Articles_News.csv', 'w', newline='', encoding='utf-8')
fieldnames = ['url', 'title', 'content']
writer = csv.DictWriter(csv1, fieldnames=fieldnames)
writer.writeheader()

with open('data.txt') as outfile:
    data = json.load(outfile)
    for me in data['articles']:
        writer.writerow({'url': me['url'], 'title': me['title'], 'content': me['content']})

csv1.close()
