# memuat pustaka Python yang dibutuhkan
import pandas as pd
import json
import re
import time
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
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),\
        options=options)
    
    # tunggu maksimal 30 detik, 
    # jika elemen ada sebelum batas waktu tersebut, 
    # maka lanjutkan ke baris berikutnya.
    driver.implicitly_wait(30)
    driver.get(url+"/description")   

    content = driver.page_source

    # tunggu 5 detik
    time.sleep(5)

    # akhiri sesi Selenium browser
    driver.quit()

    soup = BeautifulSoup(content, "lxml")
   
    # ekstrak jumlah donasi
    try:
        money = soup.find("span", attrs={"class": "money"}).contents[0].strip()
    except:
        money = ""

    # ekstrak jumlah pendukung
    try:
        backer = soup.find_all("h3", attrs={"class": "mb0"})[1].getText().strip()
    except:
        backer = ""

    # ekstrak deskripsi proyek
    try:
        story = soup.find("div", attrs={"class": "rte__content"}).getText()
    except:
        story = ""

    # ekstrak resiko dan tantangan
    try:
        risks_and_challenges = soup.find("p", attrs={"class": "js-risks-text text-preline"}).getText()
    except:
        risks_and_challenges = ""
    
    # simpan konten ke dalam sebuah dictionary
    dict_res = {
        "money": money,
        "backer": backer,
        "story" : story,
        "risks_and_challenges": risks_and_challenges
    }
    
    return dict_res

# fungsi ekstraksi teks pada menu "FAQ"
def extract_faq_content(url):
    # inisialisasi chromedriver
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),\
        options=options)
    
    # tunggu maksimal 30 detik, 
    # jika elemen ada sebelum batas waktu tersebut, 
    # maka lanjutkan ke baris berikutnya.
    driver.implicitly_wait(30)
    driver.get(url+"/faqs")   

    content = driver.page_source

    # tunggu 5 detik
    time.sleep(5)
    
    # akhiri sesi Selenium browser
    driver.quit()

    soup = BeautifulSoup(content, "lxml")

    konten = [e for e in soup.body.find_all("li", attrs={"class": "js-faq bg-white border mb2 shadow-button radius2px hover-bg-grey-200"})]
    
    dict_res = {}
    for idx, val in enumerate(konten):
        pertanyaan = val.find("span", attrs={"class": "type-14 navy-700 medium"}).getText().strip()
        jawaban = val.find("div", attrs={"class": "type-14 navy-700 normal"}).getText().strip()
        tanggal = val.find("time")['datetime']
    
        dict_tmp = {
            "pertanyaan" : pertanyaan,
            "jawaban" : jawaban,
            "tanggal" : tanggal
        }
        dict_res[idx] = dict_tmp

    return dict_res
def extract_comments_content(url):
    # inisialisasi chromedriver
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),\
        options=options)
    
    # tunggu maksimal 30 detik, 
    # jika elemen ada sebelum batas waktu tersebut, 
    # maka lanjutkan ke baris berikutnya.
    driver.implicitly_wait(30)
    driver.get(url+"/comments")   

    content = driver.page_source

    # tunggu 5 detik
    time.sleep(5)
    
    # akhiri sesi Selenium browser
    driver.quit()

    soup = BeautifulSoup(content, "lxml")

    konten = [e for e in soup.body.find_all("ul", attrs={"class": "bg-grey-100 border border-grey-400 p2 mb3"})]
    dict_res = {}
    for idx, val in enumerate(konten):
        comment = val.find("p", attrs={"class": "type-14 mb0"}).getText().strip()
        name = val.find("span", attrs={"class":"mr2"}).getText().strip()
        dict_tmp = {
            "Nama"  : name,
            "Komentar" : comment
        }
        dict_res[idx] = dict_tmp

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
print(extract_campaign_content("https://www.kickstarter.com/projects/lgbb/cocktail-mixers-with-unduplicable-taste"))
print(extract_faq_content("https://www.kickstarter.com/projects/lgbb/cocktail-mixers-with-unduplicable-taste"))
print(extract_comments_content("https://www.kickstarter.com/projects/lgbb/cocktail-mixers-with-unduplicable-taste"))

#ToDo
# ekstraksi "FAQ"
# ekstraksi teks pada menu "Updates"
# ekstraksi teks pada menu "Comments"
# ekstraksi teks pada menu "Community"
