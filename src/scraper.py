# memuat pustaka Python yang dibutuhkan
import json
import re
import time

from selenium import webdriver, common
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

# fungsi untuk membersihkan string
def cleaning_string(txt):
    txt = re.sub(r'[^\x00-\x7F]+',' ', txt)
    txt = re.sub(r'["]', '', txt)
    txt = re.sub(r'["\n"]', ' ', txt)
    txt = re.sub(r'["\r"]', ' ', txt)
    txt = re.sub(r'\.+', ".", txt)
    txt = re.sub(r'(?<=[?])(?=[^\s])', r' ', txt)
    txt = re.sub(r'([,.:?0-9]+(\.[,.:?0-9]+)?)', r' \1 ', txt)
    txt = re.sub(r' ?(\d+) ?', r' \1 ', txt).strip()
    txt = re.sub(' +', ' ', txt)
    return txt

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
    s = Service(r"chromedriver/chromedriver.exe")
    driver = webdriver.Chrome(service=s, options=options)
    
    # tunggu maksimal 10 detik, 
    # jika elemen ada sebelum batas waktu tersebut, 
    # maka lanjutkan ke baris berikutnya.
    driver.implicitly_wait(10)
    driver.get(url+"/description")

    # tunggu 5 detik
    time.sleep(5)    

    content = driver.page_source

    # akhiri sesi Selenium browser
    driver.quit()

    soup = BeautifulSoup(content, "lxml")
   
    # ekstrak jumlah donasi
    money = try_or(lambda: soup.find("span", \
        class_="money").contents[0].strip(), "<n/a>")

    # ekstrak jumlah pendukung
    backer = try_or(lambda: soup.find_all("h3", \
        class_="mb0")[1].getText().strip(), "<n/a>")

    # ekstrak deskripsi proyek
    story = try_or(lambda: soup.find("div", \
        class_="rte__content").getText(), "<n/a>")

    # ekstrak resiko dan tantangan
    risks_and_challenges = try_or(lambda: soup.find("p", \
        class_="js-risks-text text-preline").getText(), "<n/a>")
    
    # simpan konten ke dalam sebuah dictionary
    dict_res = {
        "money": money,
        "backer": backer,
        "story" : cleaning_string(story),
        "risks_and_challenges": cleaning_string(risks_and_challenges)
    }
    
    return dict_res

# fungsi ekstraksi teks pada menu "FAQ"
def extract_faq_content(url):
    # inisialisasi chromedriver
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    s = Service(r"chromedriver/chromedriver.exe")
    driver = webdriver.Chrome(service=s, options=options)
    
    # tunggu maksimal 10 detik, 
    # jika elemen ada sebelum batas waktu tersebut, 
    # maka lanjutkan ke baris berikutnya.
    driver.implicitly_wait(10)
    driver.get(url+"/faqs")

    # tunggu 5 detik
    time.sleep(5)

    content = driver.page_source
    
    # akhiri sesi Selenium browser
    driver.quit()

    soup = BeautifulSoup(content, "lxml")

    konten = [e for e in soup.body.find_all("li", \
        class_="js-faq bg-white border mb2 shadow-button radius2px hover-bg-grey-200")]
    
    dict_res = {}
    if not konten:
        dict_res = "<n/a>"
    else:
        for idx, val in enumerate(konten):
            pertanyaan = try_or(lambda: val.find("span", \
                class_="type-14 navy-700 medium").getText().strip(), "<n/a>")
            jawaban = try_or(lambda: val.find("div", \
                class_="type-14 navy-700 normal").getText().strip(), "<n/a>")
            tanggal = try_or(lambda: val.find("time")['datetime'], "<n/a>")
        
            dict_tmp = {
                "pertanyaan" : pertanyaan,
                "jawaban" : jawaban,
                "tanggal" : tanggal
            }
            dict_res[idx] = dict_tmp

    return dict_res

# fungsi ekstraksi teks pada menu "Updates"
def extract_update_content(url):
    # inisialisasi chromedriver
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--disable-extensions")
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    s = Service(r"chromedriver/chromedriver.exe")
    driver = webdriver.Chrome(service=s, options=options)
    
    # tunggu maksimal 10 detik, 
    # jika elemen ada sebelum batas waktu tersebut, 
    # maka lanjutkan ke baris berikutnya.
    driver.implicitly_wait(10)
    driver.get(url+"/posts")

    # tunggu 5 detik
    time.sleep(5)

    # klik tombol load more
    while True:
        try:
            driver.find_element(By.CLASS_NAME, 'flex w100p').click()
            time.sleep(5)
        except common.exceptions.NoSuchElementException:
            break
    
    # tunggu 5 detik
    time.sleep(5)

    # mengambil halaman HTML dari url yang diberikan pada driver.get(url)
    content = driver.page_source
    
    # akhiri sesi Selenium browser
    driver.quit()

    soup = BeautifulSoup(content, "lxml")

    list_of_updates = [e for e in soup.find_all("div", \
        class_="grid-col-12 grid-col-8-md grid-col-offset-2-md mb6 relative")]

    dict_res = {}
    if not list_of_updates:
        dict_res = "<n/a>"
    else:
        for idx, val in enumerate(list_of_updates):
            title = try_or(lambda: val.find("h2", \
                class_="mb3").getText(), "<n/a>")
            date = try_or(lambda: val.find("span", \
                class_="type-13 soft-black_50 block-md").getText(), "<n/a>")
            author = try_or(lambda: val.find("div", \
                class_="pl2").find("div").contents[0], "<n/a>")
            content_link = try_or(lambda: val.find("a", \
                class_="truncated-post soft-black block border border-grey-500 hover-border-dark-grey-400")["href"], "<n/a>")
            dict_res[idx] = {
                'title': title,
                'date': date,
                'author': author,
                'content_link': content_link
            }
    
    return dict_res

# fungsi ekstraksi teks pada menu "Comment"
def extract_comment_content(url):
    # inisialisasi chromedriver
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--disable-extensions")
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    s = Service(r"chromedriver/chromedriver.exe")
    driver = webdriver.Chrome(service=s, options=options)
    
    # tunggu maksimal 10 detik, 
    # jika elemen ada sebelum batas waktu tersebut, 
    # maka lanjutkan ke baris berikutnya.
    driver.implicitly_wait(10)
    driver.get(url+"/comments")

    # tunggu 5 detik
    time.sleep(5)

    # klik tombol load for more replies dan load more 
    while True:
        try:
            driver.find_element(By.CLASS_NAME, 'bttn-secondary').click()
            time.sleep(5)
        except common.exceptions.NoSuchElementException:
            break
    
    # tunggu 5 detik
    time.sleep(5)

    content = driver.page_source
    
    # akhiri sesi Selenium browser
    driver.quit()

    soup = BeautifulSoup(content, "lxml")

    list_of_comments = [e for e in soup.find_all("li", class_="mb2")]

    dict_res = {}
    if not list_of_comments:
        dict_res = "<n/a>"
    else:
        for idx, val in enumerate(list_of_comments):
            post_name = try_or(lambda: val.find("div").find("span", \
                class_='mr2').getText(), "<n/a>")
            post_comment = try_or(lambda: val.find("div").find("p").getText(), "<n/a>")
            post_datetime = try_or(lambda: val.find("div").find("time")['title'], "<n/a>")

            list_of_replies = [e for e in val.find_all("li", class_="mb2")]
            dict_replies = {}
            if not list_of_replies:
                dict_replies = "<n/a>"
            else:
                for sidx, sval in enumerate(list_of_replies):
                    reply_name = try_or(lambda: sval.find("div").find("span", \
                        class_='mr2').getText(), "<n/a>")
                    reply_comment = try_or(lambda: sval.find("div").find("p").getText(), "<n/a>")
                    reply_datetime = try_or(lambda: sval.find("div").find("time")['title'], "<n/a>")

                    dict_replies[sidx] = {
                        "reply_name" : reply_name,
                        "reply_comment" : cleaning_string(reply_comment),
                        "reply_datetime" : reply_datetime
                    }

            if post_name is not "<n/a>":
                dict_res[idx] = {
                    "post_name" : post_name,
                    "post_comment" : cleaning_string(post_comment),
                    "post_datetime" : post_datetime,
                    "post_replies" : dict_replies
            }
    
    return dict_res

# fungsi untuk mendapatkan data top negara yang mengambil bagian pada project
def extract_countries(div_input): 
    country = try_or(lambda: div_input.find("div", \
        class_="primary-text js-location-primary-text").find("a").contents[0], "<n/a>")
    backer = try_or(lambda: div_input.find("div", \
        class_="tertiary-text js-location-tertiary-text").contents[0].getText().split()[0], "<n/a>")
    
    dict_output = {
        "country" : country,
        "backer" : backer
    }
    return dict_output

# fungsi untuk mendapatkan data top negara yang mengambil bagian pada project
def extract_cities(div_input):
    city = try_or(lambda: div_input.find("div", \
        class_="primary-text js-location-primary-text").find("a").contents[0], "<n/a>")
    country = try_or(lambda: div_input.find("div", \
        class_="secondary-text js-location-secondary-text").find("a").contents[0], "<n/a>")
    backer = try_or(lambda: div_input.find("div", \
        class_="tertiary-text js-location-tertiary-text").contents[0].getText().split()[0], "<n/a>")
    
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
    s = Service(r"chromedriver/chromedriver.exe")
    driver = webdriver.Chrome(service=s, options=options)
    
    # tunggu maksimal 10 detik, 
    # jika elemen ada sebelum batas waktu tersebut, 
    # maka lanjutkan ke baris berikutnya.
    driver.implicitly_wait(10)
    driver.get(url+"/community")

    # tunggu 5 detik
    time.sleep(5)

    content = driver.page_source
    soup = BeautifulSoup(content, "lxml")
    
    # akhiri sesi Selenium browser
    driver.quit()
    
    dict_top_cities = {}
    dict_top_country = {}

    section_cities = soup.find_all("div", \
        class_="community-section__locations_cities")
    section_country = soup.find_all("div", \
        class_="community-section__locations_countries")

    section_total_backers = soup.find("div", \
        class_="community-section__hero")
    total_backers= try_or(lambda: section_total_backers.find("div", \
        class_="title").contents[0].getText().split()[0], "<n/a>")

    section_total_new_backers = soup.find("div", class_="new-backers")
    total_new_backers = try_or(lambda: section_total_new_backers.find("div", \
        class_="count").contents[0].getText().strip(), "<n/a>")

    section_total_existing_backers = soup.find("div", class_="existing-backers")
    total_existing_backers = try_or(lambda: section_total_existing_backers.find("div", \
        class_="count").contents[0].getText().strip(), "<n/a>")

    if section_cities:
        section_cities_new = section_cities[0].find_all("div", \
            class_="location-list__item js-location-item")
        for idx, val in enumerate(section_cities_new):
            dict_top_cities[idx] = extract_cities(val)
    else:
        dict_top_cities = "<n/a>"
    
    if section_country:
        section_country_new = section_country[0].find_all("div", \
            class_="location-list js-locations-countries")
        for idx, val in enumerate(section_country_new):
            dict_top_country[idx] = extract_countries(val)
    else:
        dict_top_country = "<n/a>"

    dict_temp = {
            "Total Backer": total_backers,
            "Total New Backer": total_new_backers,
            "Total Existing Backer": total_existing_backers,
            "Top Cities": dict_top_cities,
            "Top Country": dict_top_country
    }

    return dict_temp