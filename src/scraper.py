# memuat pustaka Python yang dibutuhkan
import pandas as pd
import json
import re
from os import walk

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# fungsi ekstraksi url dari dataframe masukan
def extract_project_url(df_input):
    list_url = []
    for ele in df_input["urls"]:
        dict_tmp = json.loads(ele)
        str_tmp = dict_tmp["web"]["project"]
        list_url.append(re.split('\?', str_tmp)[0])
    return list_url

# fungsi ekstraksi teks pada menu "Campaign"
def extract_campaign_content(url):
    # inisialisasi chromedriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    # tunggu 5 detik sebelum melakukan pengikisan
    driver.implicitly_wait(5)
    driver.get(url)

    content = driver.page_source
    soup = BeautifulSoup(content, 'lxml')
   
	# ekstrak jumlah donasi
    try:
        money = soup.body.find('span', attrs={'class': 'money'}).contents[0].strip()
    except:
        money = ""

	# ekstrak jumlah pendukung
    try:
        backer = soup.body.find_all('h3', attrs={'class': 'mb0'})[1].contents[0].strip()
    except:
        backer = ""

	# ekstrak deskripsi proyek
    try:
        story = soup.body.find('div', attrs={'class': 'rte__content'}).contents[0]
    except:
        story = ""

	# ekstrak resiko dan tantangan
    try:
        risks_and_challenges = soup.body.find('p', attrs={'class': 'js-risks-text text-preline'}).contents[0]
    except:
        risks_and_challenges = ""

    # for span in mb0.span.find_all('span', recursive=False):
        # print(span.attrs['money'])

    # akhiri sesi Selenium browser
    driver.quit()
    
	# simpan konten ke dalam sebuah dictionary
    dict_res = {
        "money": money,
        "backer": backer,
        "story" : story,
        "risks_and_challenges": risks_and_challenges
    }
    
    return dict_res
    
# inisialisasi direktori data (berisi kumpulan berkas CSV)
# data didapat dari https://webrobots.io/kickstarter-datasets/
dir_path = ".\data"
filenames = next(walk(dir_path), (None, None, []))[2]

# menjalankan fungsi extract_project_url() secara iteratif
# sesuai dengan banyaknya berkas pada direktori data
list_project_site = []
for ele in filenames:
    df_kickstarter = pd.read_csv(dir_path + "\\" + ele)
    list_project_site.extend(extract_project_url(df_kickstarter))

# uji coba cetak hasil ekstraksi untuk satu url
print(extract_campaign_content(list_project_site[0]))

#ToDo
# ekstraksi "FAQ"
# ekstraksi teks pada menu "Updates"
# ekstraksi teks pada menu "Comments"
# ekstraksi teks pada menu "Community"