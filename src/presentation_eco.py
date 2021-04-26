# -*- coding: utf-8 -*-
# script contenant les fonctions pour générer la sous-rubrique "présentation"
# de la rubrique "tourisme écologique"

import streamlit as st
import pandas as pd
import webbrowser
from streamlit_folium import folium_static
import folium
from src import dataframe_hotels

def generate_html_hotel_desc(row):
    '''
    Génère le contenu html de la description d'un hôtel pour la carte
    param : row - rang d'un dataframe correspondant à l'hôtel
    return : decription - string, la description en html
    '''
    description = "<ul>"
    if row["ecologique"] == "oui":
        description += "<li>eco-responsable</li>"
    if row["iso"] == "oui" :
        description += "<li>certification ISO</li>"
    if row["green_leader"] == "oui":
        description += "<li>GreenLeader</li>"
    description += f"</ul>aller à <a href=\"{row['lien']}\" target=\"_blank\">{row['nom']}"

    return description

# st.cache pour économiser du temps si on recharge la page car opération coûteuse
@st.cache(hash_funcs={folium.folium.Map: lambda _: None}, allow_output_mutation=True)
def generate_map():
    '''
    Génération de la carte avec des marqueurs pour tous les hôtels et leur description
    return : m - folium.Map, la carte générée
    '''
    # création de la carte
    m = folium.Map(zoom_start = 2)

    # ajout des marqueurs pour chaque hôtel
    for index, row in dataframe_hotels.iterrows():
        couleur = "#ffc2c2" if row["ecologique"] == "non" else "mediumseagreen"
        popup_content = folium.Html(generate_html_hotel_desc(row), script=True)
        popup = folium.Popup(popup_content, max_width = 300)
        folium.CircleMarker(
            location = [row["latitude"], row["longitude"]],
            popup = popup,
            tooltip = row["nom"],
            fill_color = couleur,
            color = couleur,
            fill_opacity = 0.7,
            radius = 6
        ).add_to(m)

    return m

def presentation_eco():
    '''
    Présentation du projet d'investissement et du groupe NH Hotel Group
    '''

    st.subheader("Présentation du projet - étude de cas")
    col1, col2, col3 = st.beta_columns([8,6,6])
    with col2 :
        st.image('static/img/eco_feuilles.jpg', width = 90)
    st.text("")
    st.text("")
    st.text("")
    st.text("")
    st.markdown("### **Projet d'investissement**")
    st.markdown("L'écologie est un domaine qui préoccupe de plus en plus : les consciences s’éveillent. Dans toute démarche ou toute activité, il devient naturel de se poser la question « est-ce mauvais pour la planète ? N’y a-t-il pas une alternative plus éco-responsable ? ». Le tourisme est un secteur de loisirs qui n’échappe pas à ce phénomène de prise de conscience, et de nombreux établissements mettent désormais en avant leur engagement écologique. Nous pensons que le tourisme écologique représente l’avenir du tourisme, et si de nombreux groupes d’hôtels proposent déjà un certain nombre de logements respectueux de l’environnement, il n’est pas toujours aisé pour le client d’avoir accès à l’ensemble des propositions écologiques. Nous vous proposons donc d’investir dans le développement d'un système de recherche de logements touristiques écologiques, qui regrouperait en un seul endroit les établissements éco-responsables de nombreux partenaires, pour offrir au client une diversité de choix optimale.")
    st.markdown("Afin de vous prouver qu’un tel système possède un réel potentiel et est réalisable, nous vous présentons une étude statistique sur les offres d’un groupe d’hôtels particulier : le groupe NH Hotel Group. A travers cette étude, nous démontrerons tout d’abord qu’une grande partie des logements proposés aujourd’hui présente des caractéristiques éco-responsables, ce qui permettrait, en combinant plusieurs partenaires, d’avoir suffisamment d’offres d'établissements pour développer un système de recherche. Nous montrerons ensuite que les logements écologiques présentent à la fois attractivité, popularité et capacité, et peuvent donc être envisagés comme rentables de manière durable, ce qui assurerait également une durabilité à notre système de recherche.")
    st.markdown("### **NH Hotel Group**")
    st.markdown("Le groupe NH Hotel Group est une chaîne d’hôtel née en 1978 en Espagne. Elle propose aujourd’hui un total de 357 hôtels répartis dans 29 pays, et se revendique comme une compagnie proposant des services et établissements de haute qualité. NH Hotel Group met également en avant leur engagement écologique sur leur site internet, avec notamment une liste de « prix de durabilité » reçus, comprenant entre autres le European Business Awards for the Environment ou le Green Awards IMEX. ")
    if st.button('Site de NH Hotel Group'):
        webbrowser.open_new_tab("https://www.nh-hotels.fr/")
    st.markdown("En guise de présentation, nous avons regroupé les hôtels de NH Hotel Groupe sur la carte ci-dessous, ce qui permet d’avoir un aperçu global des répartitions géographiques des hôtels, et des répartitions des hôtels possédant la mention éco-responsable (verts) face à ceux ne la possédant pas (roses). En passant la souris sur chaque point, le nom de l'hôtel est indiqué. En cliquant, vous pouvez voir la liste des mentions écologiques d'un hôtel, ainsi qu'il lien vers sa page.")

    # générer la carte folium
    m = generate_map()

    # afficher la carte folium
    folium_static(m)
