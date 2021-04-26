# -*- coding: utf-8 -*-
# extraction_ntealan.py - Camille Rey
# extraction des informations d'informations jugées intéressantes depuis les entrées
# dictionnaires du site https://ntealan.net/dictionaries/content/
# et écriture des données dans des fichiers .csv

import urllib.request
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import csv
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
parser.add_argument('-e', type = int, help = "number of entries to extract (supported : 1-200)")
args = parser.parse_args()

# liste des dictionnaires opérationnels
dictionnaire_ope = ["fulfulde-français", "medʉmba-francais", "ŋk̀ùnàbémbé-français",
"yemba-français", "yangben-français", "soninké-français-anglais", "ndemli-français",
"ghomala-français", "bambara-français", "mafa-francais", "duala-français", "bassa-français",
"ejagham-francais", "feefee-français", "Eton-français", "oku-english", "ŋgəmba-français"]

# création et paramètrage du webdriver selenium
options = Options()
options.headless = False if args.w=="true" else True
browser = webdriver.Chrome(executable_path = driver_path, options = options)
browser.implicitly_wait(6)

def close_popup():
    '''
    Fonction pour fermer la popup covid
    '''
    try :
        boite_info = browser.find_element(By.CSS_SELECTOR, "#dialInfo")
        bouton_fermer = boite_info.find_element_by_tag_name("button")
        bouton_fermer.click()
    except :
        pass

def login():
    '''
    Fonction pour se connecter sur le site ntealan
    '''
    bouton_login = browser.find_element(By.CSS_SELECTOR, "span[title='Login'] a")
    # solution avec execute_script, car .click() directement posait un problème de conflit de superposition d'élément
    browser.execute_script("arguments[0].click();", bouton_login)
    boite_login = browser.find_element(By.CSS_SELECTOR, "#myModalLoggin")
    # entrer identifiants
    boite_login.find_element(By.CSS_SELECTOR, "#pseudo").send_keys(username)
    boite_login.find_element(By.CSS_SELECTOR, "#password").send_keys(password)
    # soumettre le formulaire (cliquer sur le bouton connexion)
    boite_login.find_element_by_xpath("//div[@class='modal-footer']//button").click()

def get_translations(entree):
    '''
    Renvoie la liste des traductions (fr et en) pour une entrée
    param : entree - webelement - l'entrée du dictionnaire analysée
    return : trads_fr, trad_en - lists of string, listes des traductions respectivement en français et anglais
    '''
    trads_fr = []
    trads_en = []
    traductions = entree.find_elements(By.CSS_SELECTOR, ".translation>.group_equiv")
    for traduction in traductions:
        langue = traduction.find_element(By.CSS_SELECTOR, ".lang").text
        if langue == "fr":
            trads_fr.append(traduction.find_element(By.CSS_SELECTOR, ".equivalent").text)
        elif langue == "en":
            trads_en.append(traduction.find_element(By.CSS_SELECTOR, ".equivalent").text)

    return trads_fr, trads_en

def get_examples(entree):
    '''
    Renvoie la liste des exemples (fr et en) pour une entrée
    param : entree - webelement - l'entrée du dictionnaire analysée
    return : ex_fr, ex_en - lists of string, listes des exemples respectivement en français et anglais
    '''
    ex_fr = []
    ex_en = []
    exemples = entree.find_elements(By.CSS_SELECTOR, ".group_example")
    for ex in exemples:
        try :
            langue = ex.find_element(By.CSS_SELECTOR, ".lang").text
            full_exemple = ex.find_element(By.CSS_SELECTOR, ".example").text + " <--> " + ex.find_element(By.CSS_SELECTOR, ".target").text
            if langue == "fr":
                ex_fr.append(full_exemple)
            elif langue == "en":
                ex_en.append(full_exemple)
        except :
            pass
    return ex_fr, ex_en

def get_prefix(variant):
    '''
    Renvoie le prefixe (vide si inexistant) pour une entrée/variant
    param : variant - webelement, l'element depuis lequel extraire le premier prefixe trouvé
    return : prefixe - string, le prefixe
    '''
    try :
        return variant.find_element(By.CSS_SELECTOR, ".aprefix").text
    except :
        return ""

def get_suffix(variant):
    '''
    Renvoie le suffixe (vide si inexistant) pour une entrée/variant
    param : variant - webelement, l'element depuis lequel extraire le premier suffixe trouvé
    return :  string, le suffixe
    '''
    try :
        return variant.find_element(By.CSS_SELECTOR, ".suffix").text
    except :
        return ""

def has_audio(entree):
    '''
    Teste si une entrée possède (au moins) un fichier audio associé
    param : entree - webelement, l'entrée analysée
    return : boolean, la présence ou non d'un audio
    '''
    try :
        audio = entree.find_element(By.CSS_SELECTOR, "audio>source")
    except :
        return False
    return audio.get_attribute("src") != "https://ntealan.net/dictionaries/null"

def has_class_info(entree):
    '''
    Teste si une entrée possède (au moins) des informations concernant la classe
    param : entree - webelement, l'entrée analysée
    return : boolean, la présence ou non d'informations de classe
    '''
    try :
        entree.find_element(By.CSS_SELECTOR, ".classes")
        return True
    except :
        return False

def get_variants(entree):
    '''
    Renvoie la liste des variants(mots complets comprenant suffixe et préfixe) au mot principal
      d'une entrée (les autres "variants" que le premier)
    param : entree - webelement, l'entrée du dictionnaire analysée
    return : variants_text - list of string, liste des variants (vide si un seul mot dans l'entrée)
    '''
    variants = entree.find_elements(By.CSS_SELECTOR, ".variant>.variant")
    variants_text = []
    for variant in variants :
        variant_entree = get_prefix(variant) + variant.find_element(By.CSS_SELECTOR, ".radical").text + get_suffix(variant)
        variants_text.append(variant_entree)

    return variants_text

def get_conjugation(entree):
    '''
    Renvoie la liste des conjugaisons pour une entrée sous la forme type:forme
    param : entree - webelement, l'entrée du dictionnaire analysée
    return : conjugaisons_list - list of string, liste des conjugaisons spécifiées (vide si pas de conjugaison spécifié)
    '''
    conjugaisons_list = []
    conjugaisons = entree.find_elements(By.CSS_SELECTOR, ".conj_group")
    for conjugaison in conjugaisons:
        conj_type = conjugaison.find_element(By.CSS_SELECTOR, ".type_conj").text
        conj_form = conjugaison.find_element(By.CSS_SELECTOR, ".forme_conj").text
        full_conj = conj_type + " : " + conj_form
        conjugaisons_list.append(full_conj)

    return conjugaisons_list

def extract_entry_info(entree):
    '''
    extrait les infos d'une entrée de dictionnaire
    param : entree - webelement, l'entrée du dictionnaire analysée
    return : entree_infos - dict, informations extraites de l'entrée
    '''

    # extraction des informations "obligatoires" (communes à toutes les entrées)
    radical = entree.find_element(By.CSS_SELECTOR, ".radical").text
    type = entree.find_element(By.CSS_SELECTOR, ".type").text
    forme = entree.find_element(By.CSS_SELECTOR, ".forme").text
    pos = entree.find_element(By.CSS_SELECTOR, ".cat_part").text.split()[0]
    trads_fr, trads_en = get_translations(entree)

    # désactivation du "implicitly_wait" pour le bloc suivant, car il concerne des informations FACULTATIVES,
    # on s'attend donc à ce qu'elles ne soient souvent pas trouvées, et on ne veut pas ralentir le traitement avec "implicitly_wait"
    browser.implicitly_wait(0)
    prefixe = get_prefix(entree)
    suffixe = get_suffix(entree)
    variants = get_variants(entree)
    audio = "oui" if has_audio(entree) else "non"
    class_info = "oui" if has_class_info(entree) else "non"
    conjugaisons = get_conjugation(entree)
    ex_fr, ex_en = get_examples(entree)
    browser.implicitly_wait(4)

    entree_infos = {"full_entree" : prefixe + radical + suffixe,
            "radical" : radical,
            "prefixe" : prefixe,
            "suffixe" : suffixe,
            "type" : type,
            "forme" : forme,
            "nb_variants" : len(variants)+1,
            "variants" : "@@@".join(variants),
            "categorie" : pos,
            "nb_trads_fr" : len(trads_fr),
            "trads_fr" : "@@@".join(trads_fr),
            "nb_trads_en" : len(trads_en),
            "trads_en" : "@@@".join(trads_en),
            "nb_ex_fr" : len(ex_fr),
            "ex_fr" : "@@@".join(ex_fr),
            "nb_ex_en" : len(ex_en),
            "ex_en" : "@@@".join(ex_en),
            "audio" : audio,
            "class_info" : class_info,
            "nb_conjugaisons" : len(conjugaisons),
            "conjugaisons" : "@@@".join(conjugaisons)}

    return entree_infos

def get_dic_entries(dic, nb_entries):
    '''
    extrait les infos d'un nombre fixé d'entrées pour un dictionnaire
    param : dic - string, le dictionnaires
            nb_entries - int, le nombre d'entrée à extraire
    return : entrees_dic - list of dicts, les informations des entrées du dictionnaire
    '''

    entrees_dic = []

    # selectionner le dictionnaire :
    menu_dico = browser.find_element(By.CSS_SELECTOR, "ng-select[bindvalue='id_dico']")
    browser.execute_script("arguments[0].scrollIntoView(true);", menu_dico)
    time.sleep(0.5)
    menu_dico.click()
    browser.find_element_by_xpath(f"//div[@role='option' and span/text()='{dic}']").click()
    time.sleep(3)
    close_popup()
    time.sleep(1)

    # iterer sur les entrees
    liste_entrees = browser.find_element(By.CSS_SELECTOR, ".listeUL")
    compteur_entree = 1
    for entree in liste_entrees.find_elements_by_tag_name("li")[:nb_entries]:
        print(f"Processing {dic} - {compteur_entree}/{nb_entries} entry")
        try :
            browser.execute_script("arguments[0].scrollIntoView(true);", entree)
            time.sleep(0.5)
            entree.click()
            time.sleep(0.5)
            # extraction des informations de l'entrée
            entree = browser.find_element(By.CSS_SELECTOR, ".article")
            entree_infos = extract_entry_info(entree)
            entree_infos["dictionnaire"] = dic
            entrees_dic.append(entree_infos)

        except Exception as e:
            print(f"ERROR - while treating entry data - passing to next entry\n(error message = {e})")
        compteur_entree += 1

    return entrees_dic

def main():

    entrees_ntealan = []

    # charger la page
    browser.get("https://ntealan.net/dictionaries/content/")

    #fermer popup covid
    close_popup()
    time.sleep(1)

    # se connecter
    login()
    time.sleep(3)

    # récupérer les 100 premières entrées pour chaque dictionnaire opérationnel
    for dictionnaire in dictionnaire_ope:
        nb_entries = args.e if args.e else 100
        try :
            entrees_ntealan.extend(get_dic_entries(dictionnaire, nb_entries))
        except Exception as e:
            print(f"ERROR - error processing {dictionnaire} dictionnary, processing to next dictionnary\n(error message = {e})")

    browser.quit()

    # écriture fichier sortie
    with open("ntealan_entrees.csv", "w") as output_file:
        dict_writer = csv.DictWriter(output_file, entrees_ntealan[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(entrees_ntealan)

if __name__ == "__main__":
    main()
