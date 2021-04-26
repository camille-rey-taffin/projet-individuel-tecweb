# -*- coding: utf-8 -*-
# app_visualisation.py - Camille Rey
# application streamlit pour présenter le projet de propositions d'investissements

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from src import *

# Création du menu de navigation sur la barre latérale
st.sidebar.header("Techniques web - Projet individuel")
st.sidebar.subheader('M2 TAL - 2020/2021')
st.sidebar.info('Etudiante : Camille REY')
st.sidebar.markdown("#### Navigation")
domaine = st.sidebar.selectbox(
    "",
    ("Accueil", "Tourisme écologique", "Dictionnaire collaboratif")
)
if domaine == "Accueil":

    presentation()

if domaine == "Tourisme écologique":

    st.title("Tourisme écologique")
    sous_menu = st.sidebar.radio(
        "Données à visualiser",
        ("Présentation", "Engagement écologique", "Capacité et popularité", "Conclusion")
    )

    if sous_menu == "Présentation":
        presentation_eco()
    if sous_menu == "Engagement écologique":
        engagement_ecologique()
    if sous_menu == "Capacité et popularité":
        capacite_popularite()
    if sous_menu == "Conclusion":
        conclusion_eco()

if domaine == "Dictionnaire collaboratif":

    st.title("Dictionnaires de langues peu dotées")

    sous_menu = st.sidebar.radio(
        "Données à visualiser",
        ("Présentation", "Chiffres actuels", "Perspectives d'évolution", "Conclusion")
    )

    if sous_menu == "Présentation":
        presentation_dico()
    if sous_menu == "Chiffres actuels":
        ntealan_chiffres()
    if sous_menu == "Perspectives d'évolution":
        perspectives()
    if sous_menu == "Conclusion":
        conclusion_dico()
