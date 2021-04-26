# -*- coding: utf-8 -*-
# extraction_nb_entries.py - Camille Rey
# extraction du nombre d'entrées/requêtes de dictionnaires pour 2 plateformes : Ntealan et Leo dict

import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import csv
from collections import Counter
import argparse
import os
from dotenv import load_dotenv

# récupération des informations du .env
load_dotenv()
driver_path = os.getenv("DRIVER_PATH")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

# parser d'arguments en ligne de commande
parser = argparse.ArgumentParser()
parser.add_argument('-w', help = "executes selenium by opening a window")
args = parser.parse_args()

#création des headers pour les requests
headers = {"User-Agent":"Mozilla/5.0"}

def count_entries_ntealan():
    '''
    compte le nombre d'entrées pour chaque dictionnaire opérationnel de la plateforme Ntealan
    return : entries_count - list of dict, les infos de nb entrées pour chaque dictionnaire
    '''

    dictionnaire_ope = {'dl_fr_2018' : 'duala-français', 'ŋk̀ù_fr_2020' : 'ŋk̀ùnàbémbé-français', 'ok-en-2021' : 'oku-english', 'et-fr-2021' : 'Eton-français',
    'nu_fr_2020' : 'feefee-français', 'yb_fr_3031' : 'yemba-français', 'so_fr_2020' : 'soninké-français-anglais', 'ful_fr_2020' : 'fulfulde-français',
    'nd_fr_2020' : 'ndemli-français', 'bs_fr_2019' : 'bassa-français', 'bm_fr_11487' : 'bambara-français', 'med_fr_2020' : 'medʉmba-francais',
    'ŋg-fr-2021' : 'ŋgəmba-français', 'gho_fr_2020' : 'ghomala-français', 'ma_fr_2020' : 'mafa-francais', 'yang_fr_2020' : 'yangben-français', 'eja_fr_2020' : 'ejagham-francais'}

    entries_count = []

    # requête auprès de l'api pour chaque dictionnaire
    for dic_id, dic_name in dictionnaire_ope.items():

        request = requests.get(f"https://apis.ntealan.net/ntealan/dictionaries/articles/{dic_id}?limit=15000", headers = headers).json()
        nb_entries = len(request['articles'])
        entries_count.append({ "plateforme" : "Ntealan",
                "dictionnaire" : dic_name,
                "nb_entrees" : nb_entries,
                "requêtes" : "" })

    return entries_count

def count_entries_leo():
    '''
    compte le nombre d'entrées pour chaque dictionnaire opérationnel de la plateforme Leo Dict
    return : entries_count - list of dict, les infos de nb entrées/requêtes pour chaque dictionnaire
    '''

    # création et paramètrage du webdriver selenium
    options = Options()
    options.headless = False if args.w=="true" else True
    browser = webdriver.Chrome(executable_path = driver_path, options = options)
    browser.implicitly_wait(6)

    # récupérer les titres et urls de tous les dictionnaires
    page_fr = requests.get(f"https://dict.leo.org/allemand-fran%C3%A7ais/", headers = headers)
    parsed_content = BeautifulSoup(page_fr.content, features="html.parser")
    tableau_lien = parsed_content.find("table", {"itemprop" : "significantLinks"})
    dictionnaires_a = tableau_lien.findAll("a", {"data-dz-ui" : "moredictionaries:switchdict"})
    dictionnaires = []
    for dic in dictionnaires_a :
        titre = dic.text.replace(" ⇔ ", "-")
        lien = dic["href"]
        dictionnaires.append((titre, lien))

    # récupérer les stats
    entries_count = []

    for titre, lien in dictionnaires :
        browser.get(f"https://dict.leo.org{lien}")
        nb_entries = browser.find_element(By.CSS_SELECTOR, "#entriesNumber").text.replace(",", "")
        nb_queries = browser.find_element(By.CSS_SELECTOR, "#queriesNumber").text.replace(",", "")
        entries_count.append({
        "plateforme" : "LeoDict",
        "dictionnaire" : titre,
        "nb_entrees" : int(nb_entries),
        "requêtes" : int(nb_queries)
        })

    browser.quit()

    return entries_count

def main():

    dic_entries = []

    # récupérer le nombre d'entrées des deux plateformes
    dic_entries.extend(count_entries_ntealan())
    dic_entries.extend(count_entries_leo())

    # écriture fichier sortie
    with open("dic_nb_entries.csv", "w") as output_file:
        dict_writer = csv.DictWriter(output_file, dic_entries[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(dic_entries)

if __name__ == "__main__":
    main()
