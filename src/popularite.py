# -*- coding: utf-8 -*-
# script contenant la fonction pour générer la sous-rubrique "capacité et popularité"
# de la rubrique "tourisme écologique"

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from src import dataframe_hotels

def capacite_popularite():
    '''
    Visualisation des données en rapport avec les capacités et la popularités des hôtels écologiques
    '''

    st.subheader("Optiques de développement - capacité et popularité")
    col1, col2, col3 = st.beta_columns([8,6,6])
    with col2 :
        st.image('static/img/eco_friendly_house.jpeg', width = 150)
    st.text("")
    st.text("")
    st.text("")
    st.text("")

    # conteneur 1 - Popularité  :
    with st.beta_container() :
        st.markdown("**Présentation des avis des hôtels selon TripAdvisor :** ")

        # écriture du diagramme 1
        filtered_df = dataframe_hotels.groupby(["note", 'ecologique']).size().reset_index(name='counts')
        fig = px.bar(filtered_df, x = "note", y = "counts", color = "ecologique", title = "Note des hôtels", color_discrete_map = {'non':'#ffc2c2','oui':'mediumseagreen'}, labels = {"counts": "nombre hôtels"})
        fig.update_layout(barmode='group', xaxis_tickangle = -45)
        st.write(fig)

        st.markdown("Ce diagramme est généré à partir des informations TripAdvisor relayées sur le site de NH Hotels. Tout d'abord, on constate que la majorité des hôtels éco-responsables a une note entre 4 et 4,5 sur 5. On peut donc dire que les établissements écologiques proposés sont globalement très appréciés des clients. Le diagramme permet également de voir que la répartition des notes pour les hôtels éco-responsables est globalement la même que pour les hôtels non éco-responsables. Cela signifie que le caractère eco-responsable d’un logement n’a pas d’impact négatif sur la satisfaction des clients après leur séjour. Les insatisfactions qui font baisser les notes de certains établissements sont donc probablement liées à des facteurs indépendants de l'éco-responsabilité, tels que le personnel, le choix des boissons, l'organisation générale de l'hôtel...")

        # écriture du diagramme 2
        fig = px.histogram(dataframe_hotels, x="nombre_avis", color='ecologique', title = "Nombre d'avis (tranches de 200)", color_discrete_map = {'non':'#ffc2c2','oui':'mediumseagreen'}, labels = {"count": "nombre hôtels"})
        fig.update_layout(barmode='group', xaxis_tickangle = -45, yaxis_title_text = "Nombre d'hôtels", xaxis_title_text = "Nombre d'avis")
        st.write(fig)
        st.write(f"moyenne pour hôtels eco-responsables : ", np.mean(dataframe_hotels[dataframe_hotels['ecologique'] == "oui"]["nombre_avis"]))
        st.write(f"moyenne pour hôtels non eco-responsables : ", np.mean(dataframe_hotels[dataframe_hotels['ecologique'] == "non"]["nombre_avis"]))

        # commentaire
        st.markdown("Ce diagramme montre le nombre d'hôtels par tranche de 200 nombre d'avis laissés. Par exemple, il y a 4 hôtels écologiques pour lesquels entre 0 et 199 avis ont été laissés sur TripAdvisor, face à 18 hôtels non-écologiques. Ce diagramme est intéressant si on l'analyse en partant de l'hypothèse que plus un hôtel a d'avis laissés, plus il est fréquenté ou visible. En l'observant, on voit que les hôtels écologiques ont en général un nombre d'avis assez important, avec un pic entre 600 et 1800 avis, et une quinzaine d'hôtels avec plus de 3000 avis laissés. On remarque également que les hôtels non-écologiques ont une répartition différente, avec un pic plus bas. Les moyennes, 1470 avis pour les hôtels écologiques face à 1075 avis pour les hôtels non-écologiques confirment cette tendance. Il y a donc plus de retours des clients sur les hôtels écologiques que non-écologiques, et on peut supposer que les hôtels écologiques ont ainsi une meilleure visibilité, et/ou une fréquentation plus importante. Ces chiffres mettent en évidence l'importance des hôtels éco-responsables sur le marché de l'hôtellerie.")
    st.text("")

    # conteneur 2 - Capacité  :
    with st.beta_container() :
        st.markdown("**Présentation des capacités des hôtels :** ")

        # écriture du diagramme
        fig = px.histogram(dataframe_hotels, x="nombre_chambres", color='ecologique', title = "Nombre de chambres (tranches de 20)", color_discrete_map = {'non':'#ffc2c2','oui':'mediumseagreen'}, labels = {"count": "nombre hôtels"})
        fig.update_layout(barmode='group', xaxis_tickangle = -45, yaxis_title_text = "Nombre d'hôtels", xaxis_title_text = "Nombre de chambres")
        st.write(fig)
        st.write(f"moyenne pour hôtels eco-responsables : ", np.mean(dataframe_hotels[dataframe_hotels['ecologique'] == "oui"]["nombre_chambres"]))
        st.write(f"moyenne pour hôtels non eco-responsables : ", np.mean(dataframe_hotels[dataframe_hotels['ecologique'] == "non"]["nombre_chambres"]))

        # commentaire
        st.markdown("Ce diagramme se lit de la même manière que le précédent, avec des tranches de 20 chambres. L'observation du diagramme et des moyennes montre que la dimension éco-responsable d'un hôtel n'a pas d'impact négatif sur sa capacité. Au contraire, pour les données étudiées, les logements écologiques ont même globalement une plus grande capacité que les logements non-écologiques. Les logements écologiques sont donc adaptés au tourisme à grande échelle, et peuvent répondre aux besoins de nombreux clients, ce qui est un point non négligeable dans une perspective de rentabilité.")
