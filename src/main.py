# memuat pustaka Python yang dibutuhkan
import pandas as pd
import json
import sys
from os import walk, path

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
                list_project_site = []
                for ele in filenames:
                    df_kickstarter = pd.read_csv(dir_path_data + "\\" + ele)
                    list_project_site.extend(extract_project_url(df_kickstarter))
                
                # buka berkas luaran
                try:
                    with open(dir_path_output) as json_file:
                        data = json.load(json_file)
                        print("\nCheckpoint from", str(len(data)), "of", str(len(list_project_site)))
                        print("Project site:", data[str(len(data)-1)]["site"])
                        print("\nStarting to scrape...")
                except Exception as e:
                    data = {}
                    print("\nStarting to scrape...")

                if len(data) < 1:
                    for idx, val in enumerate(list_project_site):
                        dict_tmp = {}
                        if idx < 1:
                            print(str(idx+1), "of", str(len(list_project_site)), "| Scrape", val)
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
                            with open(dir_path_output, "r+") as file:
                                data = json.load(file)
                                print(str(idx+1), "of", str(len(list_project_site)), "| Scrape", val)
                                dict_tmp[idx] = {
                                    "site": val,
                                    "campaign": extract_campaign_content(val),
                                    "faq": extract_faq_content(val),
                                    "update": extract_update_content(val),
                                    "comment": extract_comment_content(val),
                                    "community": extract_community_content(val)
                                }
                                file.seek(0)
                                json.dump(dict_tmp, file)
                else:
                    for idx, val in enumerate(list_project_site):
                        if idx < (len(data)-1):
                            continue
                        elif idx == (len(data)-1):
                            data.popitem()
                            with open(dir_path_output, 'w') as f:
                                json.dump(data, f)
                            
                            with open(dir_path_output, "r+") as file:
                                dict_tmp = json.load(file)
                                print(str(idx+1), "of", str(len(list_project_site)), "| Scrape", val)
                                dict_tmp[idx] = {
                                    "site": val,
                                    "campaign": extract_campaign_content(val),
                                    "faq": extract_faq_content(val),
                                    "update": extract_update_content(val),
                                    "comment": extract_comment_content(val),
                                    "community": extract_community_content(val)
                                }
                                file.seek(0)
                                json.dump(dict_tmp, file)
                        else:
                            with open(dir_path_output, "r+") as file:
                                dict_tmp = json.load(file)
                                print(str(idx+1), "of", str(len(list_project_site)), "| Scrape", val)
                                dict_tmp[idx] = {
                                    "site": val,
                                    "campaign": extract_campaign_content(val),
                                    "faq": extract_faq_content(val),
                                    "update": extract_update_content(val),
                                    "comment": extract_comment_content(val),
                                    "community": extract_community_content(val)
                                }
                                file.seek(0)
                                json.dump(dict_tmp, file)
            else:
                print("Wrong output file extension. Use JSON extension.")
            print("*** End ***")
        
if __name__ == '__main__':
    main()