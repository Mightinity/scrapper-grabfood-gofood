from bs4 import BeautifulSoup
import pandas as pd
import requests, re, random, json, os

urls = {
    "UM": "https://food.grab.com/id/en/restaurant/sambal-sarumpet-lesanpuro-delivery/6-C3AYFGJTVX62TA",
}

def read_useragents(filename):
    with open(filename, "r") as file:
        useragents = file.readlines()
    return [ua.strip() for ua in useragents]

useragents = read_useragents('useragent.txt')

for name, url, in urls.items():
    # response = requests.get(url, headers=headers, proxies=proxy_dict, timeout=10)
    user_agent = random.choice(useragents)
    headers = {
        "User-Agent": user_agent
    }
    response = requests.get(url, headers=headers, timeout=10)
    # print(response)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        close_resto = soup.find(class_="closed___22AOe")
        print(close_resto.text.strip())
        # for item in tutup:
        #     print(item)
        #     tes123 = item.find_parent()
        #     # print(tes123.text.strip())
        #     if "Tutup" in tes123.text.strip():
        #         print(f"Toko {name} TUTUP")