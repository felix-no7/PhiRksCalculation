import pandas as pd
import numpy as np
import json
from bs4 import BeautifulSoup
import requests

html = BeautifulSoup(requests.get(r"https://phigros.fandom.com/wiki/Phigros_Wiki").text,features="html.parser")
PHIGROS_VERSION = html.find_all("div",attrs={"class":"mbox__content__header"})[0].string.split(" ")[-1]


'''
RKS = pd.read_excel(f"songs_rks(version{PHIGROS_VERSION}).xlsx")
del RKS["Unnamed: 0"]
RKS = RKS.set_index("name")

data = pd.read_excel(r"data\songs_accuracy(20240130210300).xlsx")
del data["Unnamed: 0"]
data = data.set_index("name")
'''

with open(f"songs_rks(version{PHIGROS_VERSION}).json","r+",encoding='utf-8') as f:
    RKS = json.load(f)

data = pd.read_excel(r"data\songs_accuracy.xlsx")
#del data["Unnamed: 0"]
data = data.set_index("name")

best19 = []
phi1 = 0

score = []

def get_rks(levelDif,acc)->float:
    if levelDif is None:
        return None
    if acc<70.00:
        return 0
    else:
        return ((acc-55)/45)**2*levelDif

for level in data.columns.values:
    for song in data.index.values:
        rks = get_rks(RKS[song][level],data.loc[song,level])
        if rks is not None:
            score.append(rks)
        if data.loc[song,level]==100.00 and rks>phi1:
            phi1 = rks

score = sorted(list(pd.Series(score).dropna()),reverse=True)
best19 = score[0:19]

print(sum(best19),phi1)
Ranking_Score = (sum(best19)+phi1)/20

print(35*"-")
print(f"accurate rks: {Ranking_Score}")
print(f"display rks: {round(Ranking_Score,2)}")
print(35*"-")