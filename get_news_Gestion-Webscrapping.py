#!/usr/bin/env python
# coding: utf-8

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import json


url_head = 'https://gestion.pe'
tags = ['economia','mundo','tecnologia','peru']


## Extrayendo artículos con sus urls

records = []

for tag in tags:
    r = requests.get(url_head + '/' + tag)
    soup = BeautifulSoup(r.text, 'html.parser')
    content = soup.find('div', attrs={'class': "content-sidebar flex mt-20 mb-20"} )
    content2 = content.find_all('div', attrs={'class': "story-item__information-box w-full"})
    dates = content.find_all('p', class_="story-item__date font-thin ml-5 text-xs text-gray-300 md:mt-5 md:ml-0")

    for idx, result in enumerate(content2):

        title = result.find('a').text
        descr = result.find('p').text
        url = result.find('a')['href']
        date = dates[idx].text
        
        try:
            rx = requests.get(url_head + url)
            soupx = BeautifulSoup(rx.text, 'html.parser')
            data = json.loads(soupx.find_all('script', type='application/ld+json')[1].string)
            text = data['articleBody']

            records.append((date, title, descr, url, text))
        except:
            print("Erro: ", tag, idx)


df = pd.DataFrame(records, columns=['date', 'title', 'description', 'url', 'text'])
print("numero de noticias: ", df.shape[0])

df = df.drop_duplicates()
print("numero de noticias no duplicadas: ", df.shape[0])


# get main topic
routes = df.iloc[:,3]
targets = []
for idx, route in enumerate(routes):
    target = route.split('/')[1]
    targets.append(target)
df['topic'] = targets
print(df.topic.value_counts())


df.to_csv('data/2021-02-13-news.csv', index=False)