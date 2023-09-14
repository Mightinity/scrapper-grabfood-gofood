from bs4 import BeautifulSoup
import pandas as pd
import requests, re, random, json, os

def read_filter_keywords(filename):
    with open(filename, 'r') as file:
        keywords = file.readlines()
    return [keyword.strip() for keyword in keywords]

def read_useragents(filename):
    with open(filename, "r") as file:
        useragents = file.readlines()
    return [ua.strip() for ua in useragents]

def modify_menu_name(menu_name, modification_data):
    for keyword, replacement in modification_data.items():
        if keyword in menu_name:
            menu_name = menu_name.replace(keyword, replacement)
    return menu_name

with open('filter_menu.json', 'r') as json_file:
    filter_data = json.load(json_file)
filter_menu = filter_data.get("filter_menu", [])
    
with open('modified_names.json', 'r') as file:
    modification_data = json.load(file)

#
# JATIM 1 GRAB
#
urls_grab = {
    # "KAK ROSE 1 DINOYO": "https://food.grab.com/id/id/restaurant/geprek-kak-rose-lowokwaru-delivery/IDGFSTI000026kl", # LOWOKWARU
    # "KAK ROSE 2 SUMBERSARI": "https://food.grab.com/id/id/restaurant/geprek-kak-rose-sumbersari-delivery/IDGFSTI000026ko", 
    # "KAK ROSE 5 LANDUNGSARI": "https://food.grab.com/id/id/restaurant/geprek-kak-rose-tlogomas-delivery/IDGFSTI00003j09", # TLOGOMAS
    # "KAK ROSE 6 CENGKEH": "https://food.grab.com/id/id/restaurant/geprek-kak-rose-jatimulyo-delivery/IDGFSTI00003fld", # JATIMULYO
    # "KAK ROSE 8 SAWOJAJAR": "https://food.grab.com/id/id/restaurant/geprek-kak-rose-sawojajar-delivery/6-CYW2MBJANXADV2",
    # "KAK ROSE 11 SIGURA": "https://food.grab.com/id/id/restaurant/geprek-kak-rose-karangbesuki-delivery/6-CZAHEP3ZBEKAGN", # KARANGBESUKI
    # "KAK ROSE 12 SUHAT": "https://food.grab.com/id/en/restaurant/geprek-kak-rose-suhat-delivery/6-CY61RZCHACBDGA",
    # "KAK ROSE 13 SUKUN": "https://food.grab.com/id/id/restaurant/geprek-kak-rose-sukun-delivery/6-CZKZUFJTJAUGNN",

    # "SARUMPET 1 SIGURA": "https://food.grab.com/id/id/restaurant/sego-sambel-sarumpet-karang-besuki-delivery/6-C26JLTNTC8BHCJ", # KARANGBESUKI
    # "SARUMPET 3 CANDI PANGGUNG": "https://food.grab.com/id/en/restaurant/sego-sambel-sarumpet-candi-panggung-delivery/AWlIW2DOfYWaYaQC5dRK",
    # "SARUMPET 8 SAWOJAJAR": "https://food.grab.com/id/id/restaurant/sambal-sarumpet-lesanpuro-delivery/6-C3AYFGJTVX62TA", # LESANPURO
    # "SARUMPET 10 BATU": "https://food.grab.com/id/id/restaurant/sego-sambel-sarumpet-sisir-delivery/6-C3LXN7M1N4ADLJ", # SISIR

    # "TLOGOMAS": "https://food.grab.com/id/id/restaurant/ayam-goreng-nelongso-tlogomas-delivery/6-C23HDCK2CAVTL2",
    # "SUHAT NEW": "https://food.grab.com/id/id/restaurant/ayam-goreng-nelongso-soehat-new-delivery/AWhVcAOVZXYdMpch2OG0",
    # "UM": "https://food.grab.com/id/id/restaurant/ayam-goreng-nelongso-um-delivery/IDGFSTI000026l2",
    # "BLIMBING": "https://food.grab.com/id/id/restaurant/ayam-goreng-nelongso-blimbing-delivery/IDGFSTI000010xb",
    # "DIENG": "https://food.grab.com/id/id/restaurant/ayam-goreng-nelongso-dieng-delivery/IDGFSTI0000112q",
    # "SINGOSARI II": "https://food.grab.com/id/id/restaurant/ayam-goreng-nelongso-singosari-delivery/IDGFSTI000026kz",
    # "SAWOJAJAR II": "https://food.grab.com/id/id/restaurant/ayam-goreng-nelongso-sawojajar-delivery/AWhWblfp2bMmVZfr_Es1",
    # "BURING": "https://food.grab.com/id/id/restaurant/ayam-goreng-nelongso-buring-delivery/IDGFSTI00002sn6",
    # "LAWANG": "https://food.grab.com/id/id/restaurant/ayam-goreng-nelongso-kalirejo-delivery/6-C2MDSCJHMB3TLA",
    # "PAKIS": "https://food.grab.com/id/id/restaurant/ayam-goreng-nelongso-pakis-delivery/IDGFSTI000010x7",
    # "BULULAWANG": "https://food.grab.com/id/id/restaurant/ayam-goreng-nelongso-bululawang-delivery/IDGFSTI000026kx",
    # "TUREN": "https://food.grab.com/id/id/restaurant/ayam-goreng-nelongso-talok-delivery/6-CY43TVJAC7LKG6",
}
useragents = read_useragents('useragent.txt')

for name, url, in urls_grab.items():
    user_agent = random.choice(useragents)
    headers = {
        "User-Agent": user_agent
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        disabled_menu_items = soup.find_all(class_=re.compile(r"menuItem--disable___.*"))
        menu_names = []

        for item in disabled_menu_items:
            menu_title = item.find(class_=re.compile(r"itemNameTitle___.*"))
            if menu_title:
                modified_menu_names = modify_menu_name(menu_title.text.strip(), modification_data)
                contains_filter_keywords = any(keyword in modified_menu_names for keyword in filter_menu)
                if not contains_filter_keywords:
                    menu_names.append(modified_menu_names)

        if menu_names:
            print(f"Toko: {name}")
            for nama_menu in menu_names:
                print(f"\tMenu yang habis adalah: {nama_menu}")
        else:
            print(f"Toko: {name} [FULL]")







# data = []
# for name, url, in urls_grab.items():
#     user_agent = random.choice(useragents)
#     headers = {
#         "User-Agent": user_agent
#     }
#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')
#         disabled_menu_items = soup.find_all(class_=re.compile(r"menuItem--disable___.*"))
#         menu_names = []

#         for item in disabled_menu_items:
#             menu_title = item.find(class_=re.compile(r"itemNameTitle___.*"))
#             if menu_title:
#                 modified_menu_names = modify_menu_name(menu_title.text.strip(), modification_data)
#                 contains_filter_keywords = any(keyword in modified_menu_names for keyword in filter_menu)
#                 if not contains_filter_keywords:
#                     menu_names.append(modified_menu_names)

#         if menu_names:
#             data.extend([(name, menu_name, "GRAB") for menu_name in menu_names])
#         else:
#             data.append((name, "[FULL]", "GRAB"))

# df = pd.DataFrame(data, columns=["OUTLET", "MENU", "APLIKASI"])
# folder_path = "csv"

# file_name = "hasil.csv"
# counter = 1
# while os.path.exists(os.path.join(folder_path, file_name)):
#     file_name = f"hasil{counter}.csv"
#     counter += 1

# file_path = os.path.join(folder_path, file_name)
# df.to_csv(file_path, index=False)










        # for item in disabled_menu_item:
        #     nama_menu = item.find(class_="itemNameTitle___1sFBq")
        #     if nama_menu:
        #         print(f"Menu yang habis adalah: {nama_menu.text.strip()}")

        # if disabled_menu_item:
        #     nama_menu = disabled_menu_item.find(class_="itemNameTitle___1sFBq")
        #     if nama_menu:
        #         print(f"Menu yang habis adalah: {nama_menu.text.strip()}")
        # pretty = soup.prettify()
        # print("OK")

        # file_path = os.path.join("result", f"result_{name}.html")
        # with open(file_path, "w", encoding="utf-8") as file:
        #     file.write(pretty)