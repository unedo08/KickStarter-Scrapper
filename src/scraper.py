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

# fungsi untuk mengembalikan nilai "N/A"
def try_or(fn, default):
    try:
        return fn()
    except:
        return default

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
    money = try_or(lambda: soup.find("span", \
        class_="money").contents[0].strip(), '<n/a>')

    # ekstrak jumlah pendukung
    backer = try_or(lambda: soup.find_all("h3", \
        class_="mb0")[1].getText().strip(), '<n/a>')

    # ekstrak deskripsi proyek
    story = try_or(lambda: soup.find("div", \
        class_="rte__content").getText(), '<n/a>')

    # ekstrak resiko dan tantangan
    risks_and_challenges = try_or(lambda: soup.find("p", \
        class_="js-risks-text text-preline").getText(), '<n/a>')
    
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

    konten = [e for e in soup.body.find_all("li", \
        class_="js-faq bg-white border mb2 shadow-button radius2px hover-bg-grey-200")]
    
    dict_res = {}
    if not konten:
        dict_res = '<n/a>'
    else:
        for idx, val in enumerate(konten):
            pertanyaan = try_or(lambda: val.find("span", \
                class_="type-14 navy-700 medium").getText().strip(), '<n/a>')
            jawaban = try_or(lambda: val.find("div", \
                class_="type-14 navy-700 normal").getText().strip(), '<n/a>')
            tanggal = try_or(lambda: val.find("time")['datetime'], '<n/a>')
        
            dict_tmp = {
                "pertanyaan" : pertanyaan,
                "jawaban" : jawaban,
                "tanggal" : tanggal
            }
            dict_res[idx] = dict_tmp

    return dict_res

# fungsi untuk mendapatkan data top negara yang mengambil bagian pada project
def extract_countries(div_input): 
    country = try_or(lambda: div_input.find("div", \
        class_="primary-text js-location-primary-text").find("a").contents[0], '<n/a>')
    backer = try_or(lambda: div_input.find("div", \
        class_="tertiary-text js-location-tertiary-text").contents[0].getText().split()[0], '<n/a>')
    
    dict_output = {
        "country" : country,
        "backer" : backer
    }
    return dict_output

# fungsi untuk mendapatkan data top negara yang mengambil bagian pada project
def extract_cities(div_input):
    city = try_or(lambda: div_input.find("div", \
        class_="primary-text js-location-primary-text").find("a").contents[0], '<n/a>')
    country = try_or(lambda: div_input.find("div", \
        class_="secondary-text js-location-secondary-text").find("a").contents[0], '<n/a>')
    backer = try_or(lambda: div_input.find("div", \
        class_="tertiary-text js-location-tertiary-text").contents[0].getText().split()[0], '<n/a>')
    
    dict_output = {
        "city" : city,
        "country" : country,
        "backer" : backer
    }
    return dict_output

# fungsi ekstraksi teks pada menu "Community"
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

    section_cities = try_or(soup.find("div", \
        class_="location-list js-locations-cities"), '<n/a>')
    section_country = try_or(soup.find("div", \
        class_="location-list js-locations-countries"), '<n/a>')

    section_total_backers = soup.find("div", \
        class_="community-section__hero")
    total_backers= try_or(lambda: section_total_backers.find("div", \
        class_="title").contents[0].getText().split()[0], '<n/a>')

    section_total_new_backers = soup.find("div", class_="new-backers")
    total_new_backers = try_or(lambda: section_total_new_backers.find("div", \
        class_="count").contents[0].getText().strip(), '<n/a>')

    section_total_existing_backers = soup.find("div", class_="existing-backers")
    total_existing_backers = try_or(lambda: section_total_existing_backers.find("div", \
        class_="count").contents[0].getText().strip(), '<n/a>')

    if section_country is not '<n/a>':
        for idx, val in enumerate(section_cities.find_all("div", \
            class_="location-list__item js-location-item")):
            dict_top_cities[idx] = extract_cities(val)
    else:
        dict_top_cities = '<n/a>'
    
    if section_cities is not '<n/a>':
        for idx, val in enumerate(section_country.findAll("div", \
            class_="location-list__item js-location-item")):
            dict_top_country[idx] = extract_countries(val)
    else:
        dict_top_country = '<n/a>'

    dict_temp = {
            "Total Backer" : total_backers,
            "Total New Backer": total_new_backers,
            "Total Existing Backer": total_existing_backers,
            "Top Cities" : dict_top_cities,
            "Top Country": dict_top_country
    }

    return dict_temp  

# fungsi ekstraksi teks pada menu "Updates"
def extract_info(url): ## untuk mendapatkan data top negara yang mengambil bagian pada project
        # inisialisasi chromedriver
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    # tunggu maksimal 30 detik, 
    # jika elemen ada sebelum batas waktu tersebut, 
    # maka lanjutkan ke baris berikutnya.
    driver.implicitly_wait(30)
    driver.get(url+"/posts")   

    content = driver.page_source

    # tunggu 5 detik
    time.sleep(5)
    
    # akhiri sesi Selenium browser
    driver.quit()

    soup = BeautifulSoup(content, "html")
    dict_res = []
    for i in range(int(soup.find("span", class_="count").text)):
        title = try_or(lambda: soup.find_all("h2", \
            class_="mb3")[:i], '<n/a>')
        date = try_or(lambda: soup.find_all("span", \
            class_="type-13 soft-black_50 block-md")[:i], '<n/a>')
        author= try_or(lambda: soup.find_all("div", \
            class_="pl2")[:i], '<n/a>')
        content= try_or(lambda: soup.find_all("div", \
            class_="rte__content")[:i], '<n/a>')
        for value in title:
            titles = value.text
        for value in date:
            dates = value.text
        for value in author:
            authors = value.text
            dict_res.append({
                'title': titles,
                'dates': dates,
                'authors': authors,
                'content': content
                })
            
    return dict_res
  
# fungsi ekstraksi teks pada menu "Comment"
def extract_comment_content(url):
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

    section_comments = soup.find("ul", class_="bg-grey-100 border border-grey-400 p2 mb3")
    list_of_comments = section_comments.find_all("li", class_="mb2")
    for val in list_of_comments:
        name_elemen = val.find("div").find("span", class_='mr2')
        name = name_elemen.get_text() if name_elemen else "No Name"
        komentar_elemen = val.find("div").find("p")
        komentar = komentar_elemen.getText() if komentar_elemen else "No Comment"
        times = val.find("div").find("time")['title']
        
        dict_output ={
            "name" : name,
            "time" : times,
            "text" : komentar,
            }
        print(dict_output)

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
print(extract_comment_content("https://www.kickstarter.com/projects/lgbb/cocktail-mixers-with-unduplicable-taste"))
print(extract_community_content("https://www.kickstarter.com/projects/lgbb/cocktail-mixers-with-unduplicable-taste"))
print(extract_info("https://www.kickstarter.com/projects/melissaaxel/it-takes-a-village-to-release-a-debut-album-0"))

#ToDo
# menggabungkan semua fungsi ekstraksi dalam fungsi main