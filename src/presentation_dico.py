# -*- coding: utf-8 -*-
# script contenant les fonctions pour générer la sous-rubrique "présentation"
# de la rubrique "dictionnaire collaboratif"

import streamlit as st
import pandas as pd
import webbrowser
from src import dataframe_ntealan

def presenter_article(article):
    '''
    Affiche un article de dictionnaire NTeALan
    param : article - row de dataframe panda, l'article à afficher
    '''

    # entrée, pref-suf, variants
    with st.beta_container() :
        col1, col2 = st.beta_columns([10, 10])
        col1.markdown(f"## **{article['full_entree']}**")
        if str(article["prefixe"]) != "nan":
            col1.markdown(f"prefixe : ***{article['prefixe']}***")
        if str(article["suffixe"]) != "nan":
            col1.markdown(f"suffixe : ***{article['suffixe']}***")
        if int(article['nb_variants']) > 1:
            col2.markdown(f"### *variants:* **{', '.join(article['variants'].split('@@@'))}**")
    st.write("")

    # cat, type, forme, conjugaisons
    with st.beta_container() :
        col1, col2 = st.beta_columns([10, 10])
        col1.markdown(f"***catégorie*** : {article['categorie']}")
        col1.markdown(f"###### *forme* : {article['forme']} - *type* : {article['type']}")

        if article["nb_conjugaisons"] > 0:
            col2.markdown("#### Conjugaisons :")
            for conj in article["conjugaisons"].split("@@@"):
                mode, forme = conj.split(" : ")
                col2.markdown(f"*{mode}* : {forme}")
    st.write("")

    # traductions
    with st.beta_container() :
        col1, col2 = st.beta_columns([10, 10])
        if article["nb_trads_en"] > 0:
            col1.markdown("#### Traductions anglaises :")
            i = 1
            for trad in article["trads_en"].split("@@@"):
                col1.markdown(f"{i}. {trad}")
                i += 1
        if article["nb_trads_fr"] > 0:
            col2.markdown("#### Traductions françaises :")
            i = 1
            for trad in article["trads_fr"].split("@@@"):
                col2.markdown(f"{i}. {trad}")
                i += 1

    # exemples
    with st.beta_container() :
        col1, col2 = st.beta_columns([10, 10])
        col1, col2 = st.beta_columns([10, 10])
        if article["nb_ex_en"] > 0:
            col1.markdown("#### Exemples anglais :")
            for ex in article["ex_en"].split("@@@"):
                col1.markdown(f"- {ex.replace('<-->', '&#8594')}")
        if article["nb_ex_fr"] > 0:
            col2.markdown("#### Exemples français :")
            for ex in article["ex_fr"].split("@@@"):
                col2.markdown(f"- {ex.replace('<-->', '&#8594')}")

def presentation_dico():
    '''
    Présentation du projet d'investissement et du groupe NH Hotel Group
    '''

    st.subheader("Présentation du projet - étude de cas")
    col1, col2, col3 = st.beta_columns([8,6,6])
    with col2 :
        st.image('static/img/dic1.jpeg', width = 90)
    st.text("")
    st.text("")
    st.text("")
    st.text("")
    st.markdown("### **Projet d'investissement**")
    st.markdown("Internet est aujourd'hui l'outil premier lorsqu'on cherche la réponse à une question. Il n'est donc pas étonnant qu'on se tourne également vers lui pour trouver la traduction d'un mot ou d'une phrase. Les dictionnaires en ligne sont donc de plus en plus utilisés, et font donc face à un besoin constant d'accroître leur quantité de données. Si de nombreuses plateformes existantes proposent déjà un grand nombre de données pour les paires de langues \"bien documntées\", qu'en est-il pour les langues dites \"peu dotées\" ? Ces langues, pour lesquelles il est difficile de trouver des données textuelles numérisées, sont souvent laissées de côté par les plateformes de dictionnaires multilingues. \"peu dotée\" ne signifie pourtant pas nécessairement \"peu parlée\", et l'accès à des dictionnaires multilingues de langues peu dotées peut donc s'avérer extrêmement utile. Nous vous proposons donc d'investir dans une plateforme de dictionnaires en ligne de langue peu dotées. Nous vous présenterons pour cela une plateforme déjà existence et en voie de développement : NTeALan ")
    if st.button('NTeAlan'):
        webbrowser.open_new_tab("https://ntealan.org/")
    st.markdown("### **NTeALan**")
    st.markdown("Le projet NTeALan (New Technologies for African Languages), qui a déjà plus de trois ans d'existence, vise à promouvoir le développement et l’enseignement des langues nationales africaines à travers à la mise en œuvre d’outils technologiques intelligents. NTeALan propose une plateforme de dictionnaire collaboratif en ligne qui permet aux spécialistes de langues et cultures africaines de partager et échanger sur leurs ressources culturelles et linguistiques. Nous vous présenterons quelques chiffres sur cette plateforme, puis quelques chiffres de plateformes plus importantes, afin de vous montrer que bien qu'en cours de développement, la plateforme NTeALan possède un véritable potentiel qui n'attend que vos investissements pour être pleinement atteint !")
    if st.button('NTeAlan - dictionnaire collaboratif'):
        webbrowser.open_new_tab("https://ntealan.net/dictionaries/")

    # présentation d'article
    st.markdown("En guise de présentation de l'outil, nous vous proposons de consulter des exemples d'articles de dictionnaires actuellement disponibles sur le site :")
    dicos_operationnels = list(dataframe_ntealan.dictionnaire.unique())
    dictionnaire = st.selectbox('Sélectionnez un dictionnaire', options = dicos_operationnels, index = 5 )

    # affichage de l'article
    best_articles = {"fulfulde-français" : "addugol", "medʉmba-francais" : "bə̀ntʉ", "ŋk̀ùnàbémbé-français" : "ɓìoɓìòhla",
    "yemba-français" : "lebāt", "yangben-français" : "ɛmbɔlbɔl", "soninké-français-anglais" : "a", "ndemli-français" : "láŋlī",
    "ghomala-français" : "mbì", "bambara-français" : "àbarika", "mafa-francais" : "ngigádà", "duala-français" : "ansanɛ", "bassa-français" : "hìɓàŋ",
    "ejagham-francais" : "eri", "feefee-français" : "béhsīē", "Eton-français" : "ìdídígá", "oku-english" : "kɛchak", "ŋgəmba-français" : "mmzáŋ"}
    article = dataframe_ntealan.loc[(dataframe_ntealan["dictionnaire"] == dictionnaire) & (dataframe_ntealan["full_entree"] == best_articles[dictionnaire])].iloc[0]
    st.markdown("""---""")
    presenter_article(article)
