# -*- coding: utf-8 -*-
# script contenant les fonctions pour générer la sous-rubrique "conclusion'"
# de la rubrique "dictionnaire collaboratif"

import streamlit as st

def conclusion_dico():
    '''
    Conclusion pour la proposition d'investissement dictionnaires
    '''

    st.subheader("Conclusion - Pourquoi investir ?")
    col1, col2, col3 = st.beta_columns([8,6,6])
    st.text("")
    st.text("")
    st.text("")

    st.markdown("A travers la présentation de différents chiffres, nous avons cherché à vous montrer les différents intérêts que vous trouverez à investir dans une plateforme de dictionnaires collaboratifs de langues peu dotées. Récapitulons ces intérêts :")

    st.markdown("### Soutenir des langues peu dotées")
    st.markdown("En investissant, vous permettrez de mieux documenter et de mettre en valeur des langues peu dotées, souvent délaissées par les outils technologiques. Ces langues, qu’elles soient parlées par un grand nombre de locuteurs ou non, font partie de la richesse linguistique de notre monde, et rassembler les connaissances à leur sujet aide à les préserver.")

    st.markdown("### Potentiel d'attractivité")
    st.markdown("Nous avons montré que les dictionnaires en ligne, s’ils sont complets et facilement accessibles, peuvent être consultés jusque’à 2 millions de fois par jour. En investissant pour améliorer la visibilité et la richesse d’une plateforme de langue peu dotées, vous contribuerez à un outil qui aura l’attention de milliers d’utilisateurs quotidiens.")

    st.markdown("### Marché de la donnée")
    st.markdown("Les dictionnaires en ligne constituent des bases de données très riches et prisées sur le marché de la donnée linguistique. Avec des investissements pour augmenter le nombre d’entrées des dictionnaires de langues peu dotées, vous contribuerez à l’expansion d’une base de données rares, et permettrez à la plateforme de prendre énormément de valeur.")
