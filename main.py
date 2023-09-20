from bs4 import BeautifulSoup
import pandas as pd
import requests, re, random, json, os, time

def read_filter_keywords(filename):
    with open(filename, 'r') as file:
        keywords = file.readlines()
    return [keyword.strip() for keyword in keywords]

def read_useragents(filename):
    with open(filename, "r") as file:
        useragents = file.readlines()
    return [ua.strip() for ua in useragents]

def read_proxies(filename):
    with open(filename, "r") as file:
        proxies = file.readlines()
    return [proxy.strip() for proxy in proxies]

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

maxRetries = 5

#
# JATIM 1 GOJEK
#

urls_gojek_jatim_one = {
    "GKR CENGKEH II": "https://gofood.co.id/malang/restaurant/geprek-kak-rose-bunga-cengkeh-11dcb458-3b82-4602-bf5c-2446f569b59d", # BUNGA CENGKEH
    "GKR DINOYO": "https://gofood.co.id/malang/restaurant/geprek-kak-rose-lowokwaru-fc883e75-f5c3-4ac6-b8db-b621cfaf9177", # LOWOKWARU
    "GKR LANDUNGSARI": "https://gofood.co.id/malang/restaurant/geprek-kak-rose-tlogomas-a2568178-5052-4b94-b8b4-52d48ae03a1f", # TLOGOMAS
    "GKR SAWOJAJAR": "https://gofood.co.id/malang/restaurant/geprek-kak-rose-sawojajar-8a1c1aa1-ec8a-4b42-9924-a96362e2be80",
    "GKR SIGURA": "https://gofood.co.id/malang/restaurant/geprek-kak-rose-sigura-gura-f5cf38e9-f195-4903-bfde-3a7fe61f14cb", # SIGURA GURA
    "GKR SUHAT": "https://gofood.co.id/malang/restaurant/geprek-kak-rose-soekarno-hatta-f5492f10-159a-4ba6-b2c0-90d5b403de28",
    "GKR SUKUN": "https://gofood.co.id/malang/restaurant/geprek-kak-rose-sukun-fdee1fc0-6904-4688-8df1-582aef2494d3",
    "GKR SUMBERSARI": "https://gofood.co.id/malang/restaurant/geprek-kak-rose-sumbersari-2cab085a-324f-4f82-a031-ccb0654c48ac", 

    "AGN BATU II": "https://gofood.co.id/malang/restaurant/ayam-goreng-nelongso-batu-9486ebff-bc2b-46f3-b3aa-bfa0d5d5a579",
    "AGN BLIMBING II": "https://gofood.co.id/malang/restaurant/ayam-goreng-nelongso-blimbing-54a7b458-d141-49bd-9c78-313edfdde842",
    "AGN BULULAWANG": "https://gofood.co.id/malang/restaurant/ayam-goreng-nelongso-bululawang-fde4932c-4001-4795-a0d6-87c0dec6ad5b",
    "AGN BURING": "https://gofood.co.id/malang/restaurant/ayam-goreng-nelongso-buring-5c1f4977-04af-4733-9a38-7679fad01ad3",
    "AGN DIENG": "https://gofood.co.id/malang/restaurant/ayam-goreng-nelongso-dieng-bd8b162e-ed72-4edf-8ba3-2f0b3e37685a",
    "AGN LAWANG": "https://gofood.co.id/malang/restaurant/ayam-goreng-nelongso-lawang-e2e86082-dd6e-459f-bfcf-63bf27844720",
    "AGN PAKIS": "https://gofood.co.id/malang/restaurant/ayam-goreng-nelongso-pakis-dc95a738-3a61-4348-8e35-d528662c4d50",
    "AGN SAWOJAJAR II": "https://gofood.co.id/malang/restaurant/ayam-goreng-nelongso-sawojajar-421794a1-a9c8-4b5b-9e49-f517340e55a7",
    "AGN SINGOSARI II": "https://gofood.co.id/malang/restaurant/ayam-goreng-nelongso-singosari-2f40eaf3-9b1f-413e-b859-cb791ef4cf3e",
    "AGN SUHAT NEW": "https://gofood.co.id/malang/restaurant/ayam-goreng-nelongso-suhat-8f2e5e4a-53eb-4d77-96a4-8cacb5082ae6",
    "AGN SUKUN II": "https://gofood.co.id/malang/restaurant/ayam-goreng-nelongso-sukun-28e68ca3-d89b-4ba6-8386-f0fe4c2fc488",
    "AGN TLOGOMAS": "https://gofood.co.id/malang/restaurant/ayam-goreng-nelongso-tlogomas-369ca55d-29a7-472e-8c1c-ba9d7a7aa272",
    "AGN UM": "https://gofood.co.id/malang/restaurant/ayam-goreng-nelongso-um-d7f461e5-2ca8-42ca-b3ec-4858343f9571",
    "AGN TUREN": "https://gofood.co.id/malang/restaurant/ayam-goreng-nelongso-turen-462c1e32-dbfd-478f-a69d-467d75bd892e",

    "SMB BATU": "https://gofood.co.id/en/malang/restaurant/sego-meduro-bang-sad-ngaglik-b0b97458-f450-40de-b25a-7f18c61aa484",
    "SMB KEPANJEN": "https://gofood.co.id/malang/restaurant/sego-maduro-bang-sad-kepanjen-32989237-0550-4464-9430-64d25e3da424",
    "SMB SUHAT II": "https://gofood.co.id/malang/restaurant/sego-maduro-bang-sad-suhat-63b39c4f-8bf1-4df3-86e6-0edf6bb0d98d",

    "SS CANDI PANGGUNG": "https://gofood.co.id/malang/restaurant/sego-sambel-sarumpet-candi-panggung-f886246f-d9ce-421e-a332-1906d89cc8a5",
    "SS BATU": "https://gofood.co.id/malang/restaurant/sambel-sarumpet-batu-745f5c93-14d2-474a-992b-bf42f5a639cb",
    "SS SAWOJAJAR": "https://gofood.co.id/malang/restaurant/sambal-sarumpet-sawojajar-180ae2b2-3986-4d43-8785-178b8a70a41e",
    "SS SIGURA": "https://gofood.co.id/malang/restaurant/sambal-sarumpet-sigura-97d61e9d-83d8-4a7e-9cca-67eda632afc7",
}
useragents = read_useragents('useragent.txt')
proxies = read_proxies('proxy.txt')
data_list_jatim1_gojek = []

for name, url, in urls_gojek_jatim_one.items():
    user_agent = random.choice(useragents)
    proxy = random.choice(proxies)
    headers = {
        "User-Agent": user_agent
    }
    proxy_dict = {
        "http": proxy,
        "https": proxy,
    }
    errorVar = True
    retries = 0
    while (errorVar):
        if retries < maxRetries:
            try:
                menu_names_outlet = []
                errorVar = False
                # response = requests.get(url, headers=headers, proxies=proxy_dict, timeout=10)
                response = requests.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    close_resto = soup.find_all(class_="mr-2 rounded-full bg-gf-support-danger-default w-2.5 h-2.5")
                    food_habis = soup.find_all('span', class_="min-w-[50%] text-gf-background-fill-brand gf-label-m")
                    menu_names = []
                    close_resto_var = False
                    for item in close_resto:
                        close_resto_parent = item.find_parent()
                        if "Tutup" in close_resto_parent.text.strip():
                            print(f"Outlet {name}: \t[BERHASIL (TUTUP)]")
                            data_list_jatim1_gojek.append([name, "OUTLET TUTUP", "GOJEK"])
                            close_resto_var = True
                            break

                    if not close_resto_var:
                        for item2 in food_habis:
                            food_name_parent = item2.find_parent().find_parent()
                            food_name = food_name_parent.find('h3', class_="text-gf-content-primary line-clamp-2 gf-label-m")
                            if food_name_parent:
                                modified_menu_names = modify_menu_name(food_name.text.strip(), modification_data)
                                contains_filter_keywords = any(keyword in modified_menu_names for keyword in filter_menu)
                                if not contains_filter_keywords:
                                    menu_names.append(modified_menu_names)
                        if menu_names:
                            data_list_jatim1_gojek.extend([(name, menu_name, "GOJEK") for menu_name in menu_names])
                            print(f"Outlet {name}: \t[BERHASIL]")
                            # print(f"Outlet: {name}")
                            # for nama_menu in menu_names:
                            #     print(f"\tMenu yang habis adalah: {nama_menu}")
                        else:
                            print(f"Outlet {name}: \t[BERHASIL (FULL)]")
                            data_list_jatim1_gojek.append([name, "TIDAK ADA YANG HABIS", "GOJEK"])
            except requests.exceptions.RequestException as e:
                retries =+ 1
                errorVar = True
                print(f"Outlet {name}: \t[GAGAL ({retries})]")
                time.sleep(5)
                # print(f"Gagal mengambil data pada {name}. Trying on 5 seconds ({retries})")
                # print(f"Request to {url} failed with error: {str(e)}")

df = pd.DataFrame(data_list_jatim1_gojek, columns=["OUTLET", "MENU", "APLIKASI"])
folder_path = "csv"
file_name = "hasil_jatim1.csv"
counter = 1
while os.path.exists(os.path.join(folder_path, file_name)):
    file_name = f"hasil_jatim1_{counter}.csv"
    counter += 1
file_path = os.path.join(folder_path, file_name)
df.to_csv(file_path, index=False)


#
# JATIM 1 GRAB
#

# urls_grab_jatim_one = {
#     # "AGN TLOGOMAS": "https://food.grab.com/id/id/restaurant/ayam-goreng-nelongso-tlogomas-delivery/6-C23HDCK2CAVTL2",
#     # "AGN SUHAT NEW": "https://food.grab.com/id/id/restaurant/ayam-goreng-nelongso-soehat-new-delivery/AWhVcAOVZXYdMpch2OG0",
#     # "AGN BLIMBING II": "https://food.grab.com/id/id/restaurant/ayam-goreng-nelongso-blimbing-delivery/IDGFSTI000010xb",
#     # "AGN UM": "https://food.grab.com/id/id/restaurant/ayam-goreng-nelongso-um-delivery/IDGFSTI000026l2",
#     # "AGN DIENG": "https://food.grab.com/id/id/restaurant/ayam-goreng-nelongso-dieng-delivery/IDGFSTI0000112q",
#     # "AGN SINGOSARI II": "https://food.grab.com/id/id/restaurant/ayam-goreng-nelongso-singosari-delivery/IDGFSTI000026kz",
#     # "AGN SUKUN II": "https://food.grab.com/id/en/restaurant/ayam-goreng-nelongso-sukun-delivery/IDGFSTI000011z3",
#     # "AGN SAWOJAJAR II": "https://food.grab.com/id/id/restaurant/ayam-goreng-nelongso-sawojajar-delivery/AWhWblfp2bMmVZfr_Es1",
#     # "AGN BATU": "https://food.grab.com/id/id/restaurant/ayam-goreng-nelongso-batu-delivery/IDGFSTI000026kq",
#     # "AGN BURING": "https://food.grab.com/id/id/restaurant/ayam-goreng-nelongso-buring-delivery/IDGFSTI00002sn6",
#     # "AGN PAKIS": "https://food.grab.com/id/id/restaurant/ayam-goreng-nelongso-pakis-delivery/IDGFSTI000010x7",
#     # "AGN LAWANG": "https://food.grab.com/id/id/restaurant/ayam-goreng-nelongso-kalirejo-delivery/6-C2MDSCJHMB3TLA",
#     # "AGN BULULAWANG": "https://food.grab.com/id/id/restaurant/ayam-goreng-nelongso-bululawang-delivery/IDGFSTI000026kx",
#     # "AGN TUREN": "https://food.grab.com/id/id/restaurant/ayam-goreng-nelongso-talok-delivery/6-CY43TVJAC7LKG6",

#     # "GKR DINOYO": "https://food.grab.com/id/id/restaurant/geprek-kak-rose-lowokwaru-delivery/IDGFSTI000026kl", # LOWOKWARU
#     # "GKR SUMBERSARI": "https://food.grab.com/id/id/restaurant/geprek-kak-rose-sumbersari-delivery/IDGFSTI000026ko", 
#     # "GKR LANDUNGSARI": "https://food.grab.com/id/id/restaurant/geprek-kak-rose-tlogomas-delivery/IDGFSTI00003j09", # TLOGOMAS
#     # "GKR CENGKEH": "https://food.grab.com/id/id/restaurant/geprek-kak-rose-jatimulyo-delivery/IDGFSTI00003fld", # JATIMULYO
#     # "GKR SAWOJAJAR": "https://food.grab.com/id/id/restaurant/geprek-kak-rose-sawojajar-delivery/6-CYW2MBJANXADV2",
#     # "GKR SIGURA": "https://food.grab.com/id/id/restaurant/geprek-kak-rose-karangbesuki-delivery/6-CZAHEP3ZBEKAGN", # KARANGBESUKI
#     # "GKR SUHAT": "https://food.grab.com/id/en/restaurant/geprek-kak-rose-suhat-delivery/6-CY61RZCHACBDGA",
#     # "GKR SUKUN": "https://food.grab.com/id/id/restaurant/geprek-kak-rose-sukun-delivery/6-CZKZUFJTJAUGNN",

#     "SS SIGURA": "https://food.grab.com/id/id/restaurant/sego-sambel-sarumpet-karang-besuki-delivery/6-C26JLTNTC8BHCJ", # KARANGBESUKI
#     "SS SARUMPET 3 CANDI PANGGUNG": "https://food.grab.com/id/en/restaurant/sego-sambel-sarumpet-candi-panggung-delivery/AWlIW2DOfYWaYaQC5dRK",
#     "SS SARUMPET 8 SAWOJAJAR": "https://food.grab.com/id/id/restaurant/sambal-sarumpet-lesanpuro-delivery/6-C3AYFGJTVX62TA", # LESANPURO
#     "SS SARUMPET 10 BATU": "https://food.grab.com/id/id/restaurant/sego-sambel-sarumpet-sisir-delivery/6-C3LXN7M1N4ADLJ", # SISIR
# }

# useragents = read_useragents('useragent.txt')

# for name, url, in urls_grab_jatim_one.items():
#     user_agent = random.choice(useragents)
#     headers = {
#         "User-Agent": user_agent
#     }
#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')
#         disabled_menu_items = soup.find_all(class_=re.compile(r"menuItem--disable___.*"))
#         close_resto = soup.find_all(class_="closed___22AOe")
#         menu_names = []
#         close_resto_var = False
#         for item in close_resto:
#             if "Tutup" or "Closed" in close_resto.text.strip():
#                 print(f"Outlet: {name} [OUTLET TUTUP]")
#                 close_resto_var = True
#                 break
        
#         if not close_resto_var:
#             for item in disabled_menu_items:
#                 menu_title = item.find(class_=re.compile(r"itemNameTitle___.*"))
#                 if menu_title:
#                     modified_menu_names = modify_menu_name(menu_title.text.strip(), modification_data)
#                     contains_filter_keywords = any(keyword in modified_menu_names for keyword in filter_menu)
#                     if not contains_filter_keywords:
#                         menu_names.append(modified_menu_names)

#             if menu_names:
#                 print(f"Toko: {name}")
#                 for nama_menu in menu_names:
#                     print(f"\tMenu yang habis adalah: {nama_menu}")
#             else:
#                 print(f"Toko: {name} [FULL]")
























# data = []
# for name, url, in urls_grab_jatim_one.items():
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