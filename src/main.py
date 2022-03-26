# memuat pustaka Python yang dibutuhkan
import pandas as pd
import json
import sys
import ast
import multiprocessing
from os import walk, path

from scraper import *

def main():
    # inisialisasi direktori data (berisi kumpulan berkas CSV)
    # data didapat dari https://webrobots.io/kickstarter-datasets/
    args = sys.argv[1:]

    if path.exists("chromedriver\chromedriver.exe") is False:
        print("put chromedriver.exe into chromedriver directory.")
    else:
        if path.exists("data\Kickstarter.csv") is False:
            print("put Kickstarter.csv into data directory.")
        else:
            if len(args) < 1:
                print("define the json filename.")
            elif args[0].find(".json")!=-1:
                dir_path_data = "data"
                dir_path_output = "out/" + args[0]

                filenames = next(walk(dir_path_data), (None, None, []))[2]

                # menjalankan fungsi extract_project_url() secara iteratif
                # sesuai dengan banyaknya berkas pada direktori data
                list_project_site = []
                for ele in filenames:
                    df_kickstarter = pd.read_csv(dir_path_data + "\\" + ele)
                    list_project_site.extend(extract_project_url(df_kickstarter))
                
                list_project_site = [[i, e] for i, e in enumerate(list_project_site)]
                
                # buka berkas luaran
                try:
                    f = open(dir_path_output, "r")
                    data = json.loads(f.read())
                    f.close()
                except:
                    data = {}

                list_processed = [e for e in list_project_site if e[1] \
                    not in [data[key]["site"] for key in data]]
                
                # processor = int(-1 * (multiprocessing.cpu_count()/3) // 1 * -1)
                processor = int(-1 * (multiprocessing.cpu_count()/8) // 1 * -1)
                pool = multiprocessing.Pool(processes=processor)

                print("*** start ***")

                for b in [list_processed[i:i + processor] for i in range(0, len(list_processed), processor)]:
                    dict_tmp = {}
                    list_bres = pool.map(scrapes, b)
                    
                    for i in list_bres:
                        dict_i = i
                        for elem in dict_i.values():
                            for k, v in elem.items():
                                if k is "update" and isinstance(v, str):
                                    elem[k] = ast.literal_eval(v)
                                if k is "community" and isinstance(v, str):
                                    elem[k] = ast.literal_eval(v)
                        dict_tmp.update(dict_i)

                    if len(data) < 1:
                        with open(dir_path_output, 'w') as file:
                            json.dump(dict_tmp, file, indent = 4)
                    else:
                        with open(dir_path_output, "r+") as file:
                            data = json.load(file)
                            data.update(dict_tmp)
                            file.seek(0)
                            json.dump(data, file, indent = 4)
                    print("scraped", str(b[-1][0]+1), "of", str(len(list_project_site)-1))
                    break
            else:
                print("wrong output file extension. use json extension.")
            print("*** end ***")
        
if __name__ == '__main__':
    main()