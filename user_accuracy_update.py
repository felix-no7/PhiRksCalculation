import time
import pandas as pd
import numpy as np
import json
from bs4 import BeautifulSoup
import requests

'''
RKS = pd.read_excel(r"songs_rks(version3.4.2).xlsx")
del RKS["Unnamed: 0"]
RKS = RKS.set_index("name")
'''
html = BeautifulSoup(requests.get(r"https://phigros.fandom.com/wiki/Phigros_Wiki").text,features="html.parser")
PHIGROS_VERSION = html.find_all("div",attrs={"class":"mbox__content__header"})[0].string.split(" ")[-1]
with open(f"songs_rks(version{PHIGROS_VERSION}).json","r+") as f:
    RKS = json.load(f)

data = pd.read_excel(r"data\songs_accuracy.xlsx")
#del data["Unnamed: 0"]
data = data.set_index("name")

flag = True
while flag:
    recommend = []
    name = input("song name?: ")
    for i in RKS:
        if name.upper() in i.upper():
            recommend.append(i)
        if name==i:
            flag = False
            break
    else:
        print("You may want to find:", recommend,"\n")

flag = True
while flag:
    recommend = []
    level = input(f"level?{data.columns.values}: ")
    for i in data.columns.values:
        if level.upper() in i.upper():
            recommend.append(i)
        if level==i:
            if RKS[name][level] is None:
                print(f"\"{name}\" do not have {level} level! Retry\n")
                break
            else:
                flag = False
                break
    else:
        print("You may want to find:", recommend,"\n")

while True:
    if name in data[level]:
        print(f"\nOriginal acc: {data.loc[name,level]}%")
        new_acc = input(f"New acc: ")
        if 0.00<=float(new_acc)<=100.00:
            print(20*"-")
            print(f"Original acc: {data.loc[name,level]}%")
            print(f"New acc: {new_acc}%")
            print(20*"-")
            if input("Overwrite old records?(Y/n): ")=="Y":
                data.loc[name,level] = round(float(new_acc),2)
                break
    else:
        print(f"\nOriginal acc: 00.00%")
        new_acc = input(f"New acc: ")
        if 0.00<=float(new_acc)<=100.00:
            print(20*"-")
            print(f"Original acc: 00.00%")
            print(f"New acc: {new_acc}%")
            print(20*"-")
            if input("Overwrite old records?(Y/n): ")=="Y":
                data.loc[name,level] = round(float(new_acc),2)
                break
        

now = time.strftime("%Y%m%d%H%M%S",time.localtime())
data.to_excel(f"data\songs_accuracy.xlsx")