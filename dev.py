from bs4 import BeautifulSoup
import pandas as pd
import requests, re, random, json, os

urls = {
    "UM": "https://gofood.co.id/malang/restaurant/ayam-goreng-nelongso-um-d7f461e5-2ca8-42ca-b3ec-4858343f9571",
    "TUREN": "https://gofood.co.id/malang/restaurant/ayam-goreng-nelongso-turen-462c1e32-dbfd-478f-a69d-467d75bd892e",
    "TLOGOMAS": "https://gofood.co.id/malang/restaurant/ayam-goreng-nelongso-tlogomas-369ca55d-29a7-472e-8c1c-ba9d7a7aa272"
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
        tutup = soup.find_all(class_="mr-2 rounded-full bg-gf-support-danger-default w-2.5 h-2.5")
        for item in tutup:
            print(item)
            tes123 = item.find_parent()
            # print(tes123.text.strip())
            if "Tutup" in tes123.text.strip():
                print(f"Toko {name} TUTUP")