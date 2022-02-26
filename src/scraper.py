# memuat pustaka Python yang dibutuhkan
import pandas as pd
import json
import re
from os import walk

# fungsi ekstraksi url dari dataframe masukan
def extract_project_url(df_input):
	list_url = []
	for ele in df_input["urls"]:
		dict_tmp = json.loads(ele)
		str_tmp = dict_tmp["web"]["project"]
		list_url.append(re.split('\?', str_tmp)[0])
	return list_url

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

#ToDo
# ekstraksi teks pada menu "Campaign"
# ekstraksi "FAQ"
# ekstraksi teks pada menu "Updates"
# ekstraksi teks pada menu "Comments"
# ekstraksi teks pada menu "Community"