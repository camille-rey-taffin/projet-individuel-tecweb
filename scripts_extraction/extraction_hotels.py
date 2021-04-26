# -*- coding: utf-8 -*-
# extraction_hotels.py - Camille Rey
# extraction des informations d'informations jugées intéressantes de tous les hôtels
# du site https://www.nh-hotels.fr  et écriture des données dans un fichier .csv

import requests
from bs4 import BeautifulSoup
import csv
import json
import re

headers = {"User-Agent":"Mozilla/5.0"}

def make_url(resource):
    return "https://www.nh-hotels.fr" + resource

def extract_hotel_list(url):
    '''
    Extrait la liste d'hôtels sur une page de liste d'hôtels donnée
    param : url - string, url de la liste d'hôtels
    return : url_list - list of strings, url des hotels listés
    '''
    list_page = requests.get(url, headers = headers)
    parsed_content = BeautifulSoup(list_page.content, features="html.parser")

    liens = parsed_content.find("article").findAll("li")
    url_list = [lien.find("a")["href"] for lien in liens]

    return url_list

def extract_reviews_info(id):
    '''
    Extrait la note et le nombre d'avis Tripadvisor d'un élément (uniquement le contenu qui était présent sur la page de l'hotel)
    param : id - string, l'identifiant tripadvisor de l'élément
    return : rating - string, la note de l'établissement (catégories par paliers de 0.5)
             nb_reviews - int, le nombre d'avis
    '''
    trip_page = requests.get("https://www.tripadvisor.com/" + id, headers = headers)
    parsed_tripadvisor = BeautifulSoup(trip_page.content, features="html.parser")
    bloc_reviews = parsed_tripadvisor.find("a", {"href" : "#REVIEWS"})
    rating, nb_reviews = bloc_reviews.findAll("span")
    rating = rating["class"][1].replace("bubble_", "")
    rating = rating[0] + "." + rating[1]
    nb_reviews = nb_reviews.text.replace(" reviews", "").replace(",", "")
    nb_reviews = int(nb_reviews)

    return rating, nb_reviews

def extract_hotel_info(url):
    '''
    Extrait les informations d'un hôtel donné via l'url
    param : url - string, url de l'hôtel dont on veut extraire les informations
    return : hotel_infos - dict, informations importantes (pour notre projet) de l'hôtel
    '''

    print(f"traitement de {url}")

    hotel_page = requests.get(url, headers = headers)
    parsed_content = BeautifulSoup(hotel_page.content, features="html.parser")

    # extraction nom hotel + nombre d'étoiles
    header = parsed_content.find("section", {"class": "box m-hotel-detail"}).find("header")
    hotel_name = header.find("h1").text
    nb_stars = len(header.findAll("span", {"class": "nh-ic-star"}))
    if nb_stars == 0 :
        nb_stars = ""

    # extraction nombre de chambres
    try :
        nb_rooms = parsed_content.find("img", {"alt": "Chambres"}).findNext('p').text
        nb_rooms = int(nb_rooms.replace(" Chambres", ""))
    except :
        nb_rooms = ""

    # extraction longitude et latitude
    script_map = parsed_content.find("div",{"id" : "modal-hotel-map-detail"}).findNext("script").string
    latitude = re.findall(r"location : \[parseFloat\('([^/']*)", script_map)[0]
    longitude = re.findall(r",parseFloat\('([^/']*)", script_map)[0]

    # extraction note + nombre d'avis
    try :
        # récupération de l'id tripadvisor
        tripadvisor_id = parsed_content.find("div", {"class": "trip-rating js-widget-trip"})["data-idtrip"]
        # parsing de la page tripadvisor pour récupérer UNIQUEMENT les infos disponibles dans le widget(mais pas le code source) sur https://www.nh-hotels.fr
        rating, nb_reviews = extract_reviews_info(tripadvisor_id)
    except :
        rating = ""
        nb_reviews = ""

    # attribution des mentions écologiques
    iso = "oui" if url in iso_list else "non"
    ecofriendly = "oui" if url in ecofriendly_list else "non"
    greenleader = "oui" if url in greenleaders_list else "non"

    hotel_infos = {"nom" : hotel_name,
                    "nombre_chambres" : nb_rooms,
                    "etoiles" : nb_stars,
                    "note" : rating,
                    "nombre_avis" : nb_reviews,
                    "lien" : url,
                    "iso" : iso,
                    "ecologique" : ecofriendly,
                    "green_leader" : greenleader,
                    "longitude" : longitude,
                    "latitude" : latitude}

    return hotel_infos

def extract_hotels_country(url):
    '''
    Extrait les informations de tous les hôtels pour un pays donné (via l'url)
    param : url - string, url de la page d'hotels par villes pour un pays
    return : hotel_list - list of dict, liste des informations par hôtel
    '''

    country_page = requests.get(url, headers = headers)
    parsed_content = BeautifulSoup(country_page.content, features="html.parser")

    hotel_list = []

    city_blocs = parsed_content.findAll("div", {"class": "grid-item"})
    for bloc in city_blocs:
        # extraction du nom de la ville
        city = bloc.findAll("h2")[0].text.replace("Hôtels en ", "")
        # extraction des liens des hôtels pour cette ville
        hotels_links = [a["href"] for a in bloc.find("ul").findAll("a")]
        # ajout des infos de chaque hôtel pour cette ville
        for link in hotels_links :
            hotel_infos = extract_hotel_info(make_url(link))
            hotel_infos["ville"] = city
            hotel_list.append(hotel_infos)

    return hotel_list

def extract_hotels_continent(url):
    '''
    Extrait les informations de tous les hôtels du site (via l'url des hotels par continent)
    param : url - string, url de la page d'hotels par pays/continent
    return : hotels - list of dict, liste des informations par hôtel
    '''

    page_hotels = requests.get(url, headers = headers)
    parsed_content = BeautifulSoup(page_hotels.content, features="html.parser")

    hotels = []
    # extraction de tous les blocs continents
    blocs_continents = parsed_content.findAll("div", {"class": "grid-item"})
    for continent in blocs_continents :
        continent_name = continent.findAll("h2")[0].text.replace("Hôtels en ", "")
        # extraction de tous les liens de pays
        country_links = continent.findAll("a")
        for country in country_links:
            country_name = country.findAll("strong")[0].text
            country_hotels_links = country["href"]
            country_hotels = extract_hotels_country(country_hotels_links)
            # ajout des informations de pays et de continent aux données récupérées
            for hotel in country_hotels:
                hotel["pays"] = country_name
                hotel["continent"] = continent_name
            hotels.extend(country_hotels)

    return hotels

def main():

    # extraction des listes d'hôtels possédant certificat iso, greenleader, et ecofriendly
    url_iso = "https://www.nh-hotels.fr/environnement/hotels-ecologiques-developpement-durable/iso-hotels"
    url_greenleaders = "https://www.nh-hotels.fr/environnement/hotels-ecologiques-developpement-durable/green-leaders-hotels"
    url_ecofriendly = "https://www.nh-hotels.fr/environnement/hotels-ecologiques-developpement-durable/eco-friendly-hotels"
    global iso_list
    iso_list = extract_hotel_list(url_iso)
    global greenleaders_list
    greenleaders_list = extract_hotel_list(url_greenleaders)
    global ecofriendly_list
    ecofriendly_list = extract_hotel_list(url_ecofriendly)

    # extraction des informations d'hôtel
    hotels = extract_hotels_continent("https://www.nh-hotels.fr/hotels")

    # écriture sortie csv
    with open('hotels.csv', 'w', newline='')  as output_file:
        dict_writer = csv.DictWriter(output_file, hotels[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(hotels)

if __name__ == "__main__":
    main()
