# memuat pustaka Python yang dibutuhkan
import pandas as pd
import json
import re
import time
import sys
from os import walk, path
from datetime import datetime

from selenium import webdriver, common
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

from scraper import *

def main():
    # inisialisasi direktori data (berisi kumpulan berkas CSV)
    # data didapat dari https://webrobots.io/kickstarter-datasets/
    args = sys.argv[1:]

    if path.exists("chromedriver\chromedriver.exe") is False:
        print("Put chromedriver.exe into chromedriver directory.")
    else:
        if path.exists("data\Kickstarter.csv") is False:
            print("Put Kickstarter.csv into data directory.")
        else:
            if len(args) < 1:
                print("Define the json filename.")
            elif args[0].find(".json")!=-1:
                dir_path_data = "data"
                dir_path_output = "out\\" + args[0]

                filenames = next(walk(dir_path_data), (None, None, []))[2]

                # menjalankan fungsi extract_project_url() secara iteratif
                # sesuai dengan banyaknya berkas pada direktori data
                list_project_site = ["https://www.kickstarter.com/projects/theclaw/the-claw-a-documentary-about-baron-von-raschke"]
                # for ele in filenames:
                #     df_kickstarter = pd.read_csv(dir_path_data + "\\" + ele)
                #     list_project_site.extend(extract_project_url(df_kickstarter))

                for idx, val in enumerate(list_project_site):
                    dict_tmp = {}
                    if idx < 1:                
                        dict_tmp[idx] = {
                            "site": val,
                            "campaign": extract_campaign_content(val),
                            "faq": extract_faq_content(val),
                            "update": extract_update_content(val),
                            "comment": extract_comment_content(val),
                            "community": extract_community_content(val)
                        }

                        with open(dir_path_output, 'w') as f:
                            json.dump(dict_tmp, f)
                    else:
                        dict_tmp[idx] = {
                            "site": val,
                            "campaign": extract_campaign_content(val),
                            "faq": extract_faq_content(val),
                            "update": extract_update_content(val),
                            "comment": extract_comment_content(val),
                            "community": extract_community_content(val)
                        }
                        with open(dir_path_output, "r+") as file:
                            data = json.load(file)
                            data[idx] = {
                                "site": val,
                                "campaign": extract_campaign_content(val),
                                "faq": extract_faq_content(val),
                                "update": extract_update_content(val),
                                "comment": extract_comment_content(val),
                                "community": extract_community_content(val)
                            }
                            file.seek(0)
                            json.dump(data, file)
            else:
                print("Wrong output file extension. Use JSON extension.")
        
if __name__ == '__main__':
    main()