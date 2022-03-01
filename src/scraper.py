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

def extract_countries(div_input): ## untuk mendapatkan data top negara yang mengambil bagian pada project
    country = div_input.find("div", class_="primary-text js-location-primary-text").find("a").contents[0]
    backer = div_input.find("div", class_="tertiary-text js-location-tertiary-text").contents[0].getText().split()[0]
    
    dict_output = {
        "country" : country,
        "backer" : backer
    }
    return dict_output

def extract_cities(div_input): ## untuk mendapatkan data top negara yang mengambil bagian pada project
    city = div_input.find("div", class_="primary-text js-location-primary-text").find("a").contents[0]
    country  = div_input.find("div", class_="secondary-text js-location-secondary-text").find("a").contents[0]
    backer = div_input.find("div", class_="tertiary-text js-location-tertiary-text").contents[0].getText().split()[0]
    
    dict_output = {
        "city" : city,
        "country" : country,
        "backer" : backer
    }
    return dict_output

def extract_community_content(url):
    # inisialisasi chromedriver
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),\
        options=options)
    
    # tunggu maksimal 30 detik, 
    # jika elemen ada sebelum batas waktu tersebut, 
    # maka lanjutkan ke baris berikutnya.
    driver.implicitly_wait(30)
    driver.get(url+"/community")   

    content = driver.page_source
    soup = BeautifulSoup(content, "lxml")
    # tunggu 5 detik
    time.sleep(5)
    
    # akhiri sesi Selenium browser
    driver.quit()

    dict_top_cities = {}
    dict_top_country = {}

    section_cities = soup.find("div", class_="location-list js-locations-cities")
    section_country = soup.find("div", class_="location-list js-locations-countries")

    section_total_backers = soup.find("div", class_="community-section__hero")
    total_backers= section_total_backers.find("div", class_="title").contents[0].getText().split()[0]

    section_total_new_backers = soup.find("div", class_="new-backers")
    total_new_backers = section_total_new_backers.find("div", class_="count").contents[0].getText().strip()

    section_total_existing_backers = soup.find("div", class_="existing-backers")
    total_existing_backers = section_total_existing_backers.find("div", class_="count").contents[0].getText().strip()

    for idx, val in enumerate(section_cities.find_all("div", class_="location-list__item js-location-item")):
        dict_top_cities[idx] = extract_cities(val)
    for idx, val in enumerate(section_country.findAll("div", class_="location-list__item js-location-item")):
        dict_top_country[idx] = extract_countries(val)


    dict_temp = {
            "Total Backer" : total_backers,
            "Total New Backer": total_new_backers,
            "Total Existing Backer": total_existing_backers,
            "Top Cities" : dict_top_cities,
            "Top Country": dict_top_country
    }

    return dict_temp

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
print(extract_community_content("https://www.kickstarter.com/projects/lgbb/cocktail-mixers-with-unduplicable-taste"))

#ToDo
# ekstraksi "FAQ"
# ekstraksi teks pada menu "Updates"
# ekstraksi teks pada menu "Comments"
# ekstraksi teks pada menu "Community"
