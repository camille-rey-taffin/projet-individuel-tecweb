# -*- coding: utf-8 -*-
# script contenant les fonctions pour générer la sous-rubrique "perspectives d'évolution'"
# de la rubrique "dictionnaire collaboratif"

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from src import dataframe_nbentrees

def perspectives():
    '''
    Visualisation des données comparatives Ntealan/LeoDict
    '''

    st.subheader("Perspectives d'évolution - Comparaison avec Leo Dict")
    col1, col2, col3 = st.beta_columns([8,6,6])
    with col2 :
        st.image('static/img/fleche.png', width = 70)
    st.text("")
    st.text("")
    st.text("")
    st.markdown("Dans cette section nous proposons de comparer la plateforme de dictionnaires collaboratifs de langues peu dotées NTeALan avec une plateforme de langues mieux dotées plus ancienne, et par conséquent plus développée : LEO.org. Le but de cette comparaison est de montrer le potentiel qu'une plateforme de dictionnaires collaboratifs peut atteindre, lorsqu'elle dispose d'investissements et d'une bonne visibilité.")
    st.text("")

    # Présentation de LEO
    st.markdown("### Présentation de la plateforme LEO.org")
    st.markdown("LEO (Link Everything Online) est une plateforme allemande de dictionnaires en ligne créée en 2006. LEO propose 8 dictionnaires collaboratifs bilingues, de l’allemand vers l’anglais, le français, l’espagnol, l’italien, le chinois, le russe, le portugais, et le polonais, ainsi qu'un dictionnire bilingue anglais-espagnol. La consultation de ces dictionnaires est gratuite, et peut se faire soit sur un navigateur, soit à travers une interface utilisateur téléchargeable. LEO est aujourd’hui une plateforme très riche, grâce au soutien des utilisateurs, mais aussi à celui de leurs nombreux [partenaires et donateurs](https://dict.leo.org/pages/about/ende/contributions_en.html).")
    if st.button('Plateforme LEO'):
        webbrowser.open_new_tab("https://www.leo.org/allemand-fran%C3%A7ais")

    # Comparaison des nombres d'entrées
    st.markdown("### Nombre d'entrées")
    st.markdown("Observons dans un premier temps le nombre d'entrées des différents dictionnaires de la plateforme NTeALan (selon les résultats de l'API NTeAlan) :")
    entrees_ntealan = dataframe_nbentrees[dataframe_nbentrees["plateforme"] == "Ntealan"]
    fig = px.bar(entrees_ntealan, x = "dictionnaire", y = "nb_entrees", color = "nb_entrees", title = "Nombre d'entrées par dictionnaire")
    fig.update_layout(barmode='group', xaxis_tickangle = -45)
    st.write(fig)
    st.markdown("On voit que le nombre d'entrées varie fortement en fonction de la langue, certaines langues sont mieux documentées que d'autres. Le dictionnaire bambara-français est le dictionnaire contenant le plus grand nombre d'entrées (11 487). Observons maintenant les chiffres pour la plateforme LEO :")
    entrees_leo = dataframe_nbentrees[dataframe_nbentrees["plateforme"] == "LeoDict"]
    fig = px.bar(entrees_leo, x = "dictionnaire", y = "nb_entrees", color = "nb_entrees", title = "Nombre d'entrées par dictionnaire")
    fig.update_layout(barmode='group', xaxis_tickangle = -45)
    st.write(fig)
    st.markdown("Les chiffres pour LEO ne se situent pas sur la même échelle : le dictionnaire avec le plus grand nombre d'entrées (allemand-anglais), présente plus de 800 000 entrées, tandis que le dictionnaire avec le plus petit nombre d'entrées (polonais-allemand) possède 82 445 entrées, ce qui reste presque 8 fois plus important que le dictionnaire le plus important de NteALan. Il est certes plus difficile d'obtenir des contributions pour des langues peu dotées, mais nous sommes convaincus qu'avec l'aide des bons partenaires et investisseurs, des plateformes de langues peu dotées telles que NTeALan pourraient également se développer et présenter des chiffres similaires à ceux de la plateforme LEO.")

    # Nombre de requêtes LEO
    st.markdown("### Nombre de requêtes")
    st.markdown("Nous aimerions enfin vous présenter les statistiques de nombre de requêtes moyenne par jour pour la plateforme LEO (source : leo.org).")
    fig = px.bar(entrees_leo, x = "dictionnaire", y = "requêtes", color = "requêtes", title = "Nombre quotidien de requêtes par dictionnaire")
    fig.update_layout(barmode='group', xaxis_tickangle = -45)
    st.write(fig)
    st.markdown("On voit que le dictionnaire le moins consulté est le dictionnaire anglais-espagnol (45 000 consultations/jour) : ce n’est pas surprenant dans la mesure où LEO est à l’origine une plateforme allemande, et a donc plus de visibilité auprès des utilisateurs allemands. Le dictionnaire le plus consulté est le dictionnaire anglais-allemand, avec plus de 2 millions de consultations par jour.")
    st.markdown("Les informations de nombre de requêtes ne sont malheureusement pas disponible pour la plateforme NTeALan, et nous ne pouvons donc pas les comparer. Nous espérons cependant que les statistiques de nombre de requêtes pour la plateforme NTeALan suffiront à vous montrer le potentiel d’attraction et l’utilité de plateformes de dictionnaires collaboratifs en ligne.")
