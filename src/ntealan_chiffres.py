# -*- coding: utf-8 -*-
# script contenant les fonctions pour générer la sous-rubrique "chiffres actuels"
# de la rubrique "dictionnaire collaboratif"

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from src import dataframe_ntealan

def ntealan_chiffres():
    '''
    Visualisation des données de NTeALan
    '''

    st.subheader("Plateforme Ntealan - Chiffres actuels")
    col1, col2, col3 = st.beta_columns([8,6,6])
    with col2 :
        st.image('static/img/stats.png', width = 70)
    st.text("")
    st.text("")
    st.text("")
    st.markdown("**Les statistiques suivantes sont présentées sur la base de l'analyse des 100 premiers articles pour chaque dictionnaire. Les dictionnaires analysés sont au nombre de 17.** ")
    st.text("")

    # conteneur 1 - statistiques sur les traductions :
    with st.beta_container() :
        st.markdown("**Présentons d'abord quelques statistiques concernant les traductions proposées pour les différentes entrées :** ")
        choix = st.selectbox(
            "Statistiques selon :",
            ("Traductions fr/en", "Nombre de traductions")
        )

        if choix == "Traductions fr/en" :
            counts_fr = dataframe_ntealan[dataframe_ntealan["nb_trads_fr"] > 0].shape[0]
            counts_en = dataframe_ntealan[dataframe_ntealan["nb_trads_en"] > 0].shape[0]
            counts_nt = dataframe_ntealan.loc[(dataframe_ntealan["nb_trads_en"] == 0) & (dataframe_ntealan["nb_trads_fr"] == 0)].shape[0]
            stats = pd.DataFrame({"Traductions" : ["aucune trad/ langue non précisée", "français", "anglais"], "counts" : [counts_nt, counts_fr, counts_en],})

            fig = px.pie(stats, names = "Traductions", values='counts', title = "Proportions de langue dans les traductions", color = "Traductions", color_discrete_map = {"aucune trad":"#A9A9A9", "français":"#6495ED", "anglais":"#DAA520"})
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.write(fig)

            st.markdown("Certains dictionnaires de la plateforme présentent des traductions en français uniquement, en anglais uniquement, ou dans les deux langues. En observant le diagramme, on voit que la majorité des entrées proposent des traductions en français. Il y a cependant un nombre non négligeable de traductions en anglais (187, soit 10.5%). La plateforme présente donc des données utiles dans plusieurs langues cibles. Ces chiffres pourraient être améliorés avec des collaborations supplémentaires.")

        if choix == "Nombre de traductions" :
            nb_trad_fr = dataframe_ntealan[dataframe_ntealan["nb_trads_fr"] > 0].rename(columns = {"nb_trads_fr" : "nb_trads"})
            nb_trad_fr["langue"] = "fr"
            nb_trad_en = dataframe_ntealan[dataframe_ntealan["nb_trads_en"] > 0].rename(columns = {"nb_trads_en" : "nb_trads"})
            nb_trad_en["langue"] = "en"

            fig = px.histogram(pd.concat([nb_trad_fr, nb_trad_en]), x = "langue", title = "Nombre de traductions par langue'", color = "nb_trads")
            fig.update_layout(yaxis_title_text = 'Nb de traductions')
            st.write(fig)

            st.markdown("On voit que la grande majorité (la totalité dans le cas de l'anglais) des entrées proposent une seule traduction. Il y a cependant un nombre important d'entrées qui proposent jusqu'à 10 traductions pour le cas du français. Certaines entrées sont donc riches en traductions, et par conséquent en données.")
    st.text("")

    # conteneur 2 - Exemples :
    with st.beta_container() :
        st.markdown("**Présentonsmaintenant quelques statistiques concernant les exemples proposés pour les différentes entrées :** ")
        choix = st.selectbox(
            "Statistiques selon :",
            ("Présence d'exemples", "Nombre d'entrées par nombre d'exemples", "Nombre d'exemples moyen / dictionnaire")
        )

        if choix == "Présence d'exemples" :
            exemples = pd.DataFrame()
            exemples["exemple"] = np.where(dataframe_ntealan['nb_ex_fr'] > 0, "oui", np.where(dataframe_ntealan['nb_ex_en'] > 0, 'oui', 'non'))
            fig = px.pie(exemples, names = "exemple", title = "Proportion d'entrées avec exemple", color = "exemple", color_discrete_map = {"aucune trad":"#A9A9A9", "français":"#6495ED", "anglais":"#DAA520"})
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.write(fig)

            st.markdown("On voit que presque la moitié des entrées de la plateforme offrent des exemples de tradution langue source -> langue cible. Ces chiffres montrent que la plateforme est déjà assez riche. Elle pourrait l'être encore davantage avec des collaborations supplémentaires pour ajouter des exemples pour la moitié des entrées qui n'en a pas.")

        if choix == "Nombre d'entrées par nombre d'exemples" :
            nb_total_ex = dataframe_ntealan.copy()
            nb_total_ex["total_ex"] = nb_total_ex["nb_ex_en"] + nb_total_ex["nb_ex_fr"]

            fig = px.histogram(nb_total_ex, x = "total_ex", title = "Nombre de traductions par langue")
            fig.update_layout(yaxis_title_text = 'Nb d\'entrées', xaxis_title_text = 'Nb d\'exemples')
            st.write(fig)

            st.markdown("On voit que pour les entrées qui offrent des exemples, un seul exemple est proposé dans la plupart des cas. Il arrive cependant que plusieurs exemples (jusqu'à 13!) soient proposés. Le nombre d'exemples proposés peut augmenter grâce à une mise en valeur de la plateforme pour obtenir davantage de collaborations.")

        if choix == "Nombre d'exemples moyen / dictionnaire" :
            nb_total_ex = dataframe_ntealan.copy()
            nb_total_ex["total_ex"] = nb_total_ex["nb_ex_en"] + nb_total_ex["nb_ex_fr"]

            fig = px.histogram(nb_total_ex, x = "dictionnaire", y="total_ex", histfunc='avg', title = "Nombre d'exemples moyen par entrée, en fonction du dictionnaire")
            fig.update_layout(yaxis_title_text = 'Nb moyen exemple/entrée')
            st.write(fig)

            st.markdown("On observe des résultats très hétérogènes en fonction des dictionnaires : certains dictionnaires sont plus riches que d'autres en exemples. Par exemple, les dictionnaires Duala-Français ou Eton-Français ont en moyenne au moins 1 exemple par entrée, tandis que les Yemba-Français et Yangben-Français n'en ont pas du tout. Il faudrait venir enrichir ces données grâce à de nouvelles contributions.")

    # conteneur 3 - Conjugaisons :
    with st.beta_container() :
        st.markdown("**Présentons maintenant quelques statistiques concernant les conjugaisons proposées pour les verbes :** ")
        choix = st.selectbox(
            "Statistiques selon :",
            ("Présence d'informations de conjugaison", "Nombre de conjugaisons indiquées")
        )

        if choix == "Présence d'informations de conjugaison" :
            verbes = dataframe_ntealan[dataframe_ntealan["categorie"] == "Verbe"].copy()
            verbes["conjug_presence"] = np.where(verbes['nb_conjugaisons'] > 0, "oui", "non")
            verbes = verbes.groupby(['conjug_presence']).size().reset_index(name='counts')
            verbes['pourcentage'] = 100 * verbes.counts / verbes.counts.sum()
            fig = px.bar(verbes, x = "conjug_presence", y = "counts", title = "Présence d'informations de conjugaison pour les verbes", labels = {"counts": "nombre verbes", "conjug_presence" : "informations de conjugaison"}, text = verbes['pourcentage'].apply(lambda x: '{0:1.2f}%'.format(x)))
            fig.update_layout(barmode='group', xaxis_tickangle = -45)
            st.write(fig)

            st.markdown("Les informations de conjugaison sont extrêmement enrichissantes pour une entrée de dictionnaire, et apportent un degré supplémentaire d'informations. On voit que plus d'un quart des verbes (28.6%) ont des informations de conjugaison associées. Ces chiffres sont déjà très prometteurs.")

        if choix == "Nombre de conjugaisons indiquées" :
            conjug = dataframe_ntealan[dataframe_ntealan["categorie"] == "Verbe"].copy()
            conjug = conjug[dataframe_ntealan["nb_conjugaisons"] > 0]
            conjug = conjug.groupby("nb_conjugaisons").size().reset_index(name='counts')
            conjug['pourcentage'] = 100 * conjug.counts / conjug.counts.sum()
            fig = px.bar(conjug, x = "nb_conjugaisons", y = "counts", title = "Nombre de conjugaisons indiquées (pour les verbes présentant des informations de conjugaison)", labels = {"counts": "nombre de verbes", "nb_conjugaisons" : "nombre de conjugaisons"}, text = conjug['pourcentage'].apply(lambda x: '{0:1.2f}%'.format(x)))
            fig.update_layout(barmode='group', xaxis_tickangle = -45)
            st.write(fig)

            st.markdown("Pour les verbes qui ont des informations de conjugaison associées, la très grande majorité ne possède qu'une seule information de conjugaison. Il ne faut pas oublier que toutes les langues n'ont pas la même richesse de conjugaison, ces chiffres sont donc à analyser avec un certain recul.")

    # conteneur 4 - Audio et classes :
    with st.beta_container() :
        st.markdown("**Présentons enfin quelques chiffre supplémentaires que nous avons jugés intéressants:** ")
        choix = st.selectbox(
            "Statistiques selon :",
            ("Présence de fichier audio lié", "Présence d'informations de classe")
        )

        if choix == "Présence de fichier audio lié" :
            audio = dataframe_ntealan.groupby(['audio']).size().reset_index(name='counts')
            audio['pourcentage'] = 100 * audio.counts / audio.counts.sum()
            fig = px.bar(audio, x = "audio", y = "counts", title = "Disponibilité d'audio de prononciation", labels = {"counts": "nombre d'entrées", "audio" : "fichier audio"}, text = audio['pourcentage'].apply(lambda x: '{0:1.2f}%'.format(x)))
            fig.update_layout(barmode='group', xaxis_tickangle = -45)
            st.write(fig)

            st.markdown("La plateforme de dictionnaire de NTeALan propose une fonctionnalité pour lier des fichiers audio de prononciation pour une entrée donnée. Ces informations de prononciation sont extrêmement utiles, et représentent un des avantages des dictionnaires en ligne par rapport aux versions papier. Comme le montre le diagramme ci-dessus, les contributions audio de la plateforme NTeALan sont pour l'instant peu nombreuses. On peut néanmoins imaginer la richesse de données que constituerait la plateforme si davantage de contributions audio étaient effectuées.")

        if choix == "Présence d'informations de classe" :
            adj_noms = dataframe_ntealan.loc[(dataframe_ntealan["categorie"] == "Nom") | (dataframe_ntealan["categorie"] == "Adjectif")]
            adj_noms = adj_noms.groupby("class_info").size().reset_index(name='counts')
            adj_noms['pourcentage'] = 100 * adj_noms.counts / adj_noms.counts.sum()
            fig = px.bar(adj_noms, x = "class_info", y = "counts", title = "Nombre d'entrées (parmi adjectifs et noms) présentant des informations de classe", labels = {"counts": "nombre de noms/adjectifs", "class_info" : "informations de classe"}, text = adj_noms['pourcentage'].apply(lambda x: '{0:1.2f}%'.format(x)))
            fig.update_layout(barmode='group', xaxis_tickangle = -45)
            st.write(fig)

            st.markdown("Certaines entrées (uniquement noms ou adjectifs) de la plateforme présentent des informations de \"classes d'accord\". Ces informations concernent les formes au singulier ou au pluriel. On voit que seulement moins de 7% des entrées de noms et d'adjectifs présentent des informations de classe. Cependant, l'existence même de ces informations dépend de la morphologie de chaque langue, ces chiffres sont donc à analyser avec un certain recul. Ce diagramme montre néanmoins que la plateforme offre des informations morphologiques d'un niveau profond.")
