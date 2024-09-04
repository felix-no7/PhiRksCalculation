import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

def _replace_invalid_url(url:str):
    if url=="ρars/ey":
        return "Parsley"
    if url=="Cipher: /2&//<|0":
        return "Cipher"
    if url=="[PRAW]":
        return "PRAW"
    return url


html = BeautifulSoup(requests.get(r"https://phigros.fandom.com/wiki/Phigros_Wiki").text,features="html.parser")
PHIGROS_VERSION = html.find_all("div",attrs={"class":"mbox__content__header"})[0].string.split(" ")[-1]

PHIGROS_SONGS = []
SONGS_RKS = {}

html = BeautifulSoup(requests.get(r"https://phigros.fandom.com/wiki/Songs").text,features="html.parser")

for i in html.find_all("table",attrs={"class":"wikitable no-fixed-header"}):
    for j in i.tbody.find_all("tr"):
        if j.a is not None:
            PHIGROS_SONGS.append(j.a.string)

print("Calculation Start")
for index,song in enumerate(PHIGROS_SONGS):
    
    html = BeautifulSoup(requests.get(r"https://phigros.fandom.com/wiki/"+_replace_invalid_url(song)).text)
    _rks = html.find("table",attrs={"class":"wikitable centre-text"}).tbody.find_all("tr")[4].find_all("td")

    # exception
    if song in ["MARENOL"]:
        _rks = html.find("table",attrs={"class":"wikitable centre-text"}).tbody.find_all("tr")[3].find_all("td")
    # is it a hidden song?
    if len(_rks)<3 or song in ["Destination","Anomaly","テリトリーバトル"]:
        continue
    # have legacy difficulty?
    if _rks[2].string is None:
        _rks[2] = _rks[2].div.div

    __rks = []
    for i in range(len(_rks)):
        __rks.append(round(float(_rks[i].string.strip()),1))
    for i in range(4-len(_rks)):
        __rks.append(None)
    SONGS_RKS[song] = {k:v for k,v in zip(["EZ","HD","IN","AT"],__rks)}

    print("\r|"+"▮"*(round((index/len(PHIGROS_SONGS))*100/5))+" "*(20-round((index/len(PHIGROS_SONGS))*100/5))+"|",f"{round((index/len(PHIGROS_SONGS))*100,2)}%",end="")

print("\n\nCalculation Over")


save_path_json = f"songs_rks(version{PHIGROS_VERSION}).json"
save_path_xlsx = f"songs_rks(version{PHIGROS_VERSION}).xlsx"

with open(save_path_json,"w+",encoding='utf-8') as f:
    json.dump(SONGS_RKS,f)

print(f"Saved in \"{save_path_json}\" successfully")

pd.read_json(save_path_json).T.to_excel(f"songs_rks(version{PHIGROS_VERSION}).xlsx")
print(f"Saved in \"{save_path_xlsx}\" successfully")

input("\n")
