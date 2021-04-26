# -*- coding: utf-8 -*-
# script contenant la fonction pour générer la sous-rubrique "engagement écologique"
# de la rubrique "tourisme écologique"

import streamlit as st
import pandas as pd
import plotly.express as px
from src import dataframe_hotels

def engagement_ecologique():
    '''
    Visualisation des données en rapport avec l'engagement écologique
    '''

    st.subheader("Preuves d'engagement écologique")
    col1, col2, col3 = st.beta_columns([8,6,6])
    with col2 :
        st.image('static/img/eco_friendly.jpeg', width = 120)
    st.text("")
    st.text("")
    st.text("")
    st.text("")

    # conteneur 1 - repartitions totales :
    with st.beta_container() :
        st.markdown("**Présentons d'abord les proportions totales d'hôtels présentant des caractéristiques ou mentions éco-responsables :** ")
        camembert = st.selectbox(
            "Répartition totale des hôtels en fonction de :",
            ("Eco-friendly", "Certificat ISO", "Green Leader")
        )

        if camembert == "Eco-friendly" :
            filtre = 'ecologique'
            titre =  "Répartition hôtels écologiques / non écologiques :"
            container_camembert = st.beta_container()
            st.markdown("Les efforts de NH Hotel Group pour s'engager dans un programme de développement durable se reflètent dans la répartition d'hôtels écologiques. On voit que **plus de la moitié** des hôtels de NH Hotels ont la mention eco-friendly, signifiant qu'ils utilisent de l'eléctricité provenant d'énergies renouvelables, mettent des vélos ou encore des bornes de rechargement pour véhicules électriques à disposition de leurs clients. ")

        if camembert == "Certificat ISO" :
            filtre = 'iso'
            titre = "Possède un certificat ISO : "
            container_camembert = st.beta_container()
            st.markdown("NH Hotels Group a reçu des certifications pour les normes internationales d'économie d'énergie ISO 14001 et ISO 50001 dans 25,5%, soit **un quart** de ses établissements. Ces chiffres témoignent d'une conscience ecologique et d'une volonté de s'inscrire dans une démarche eco-responsable qui ont « permis de réduire de 70% les émissions de carbonne du groupe depuis 2008, ainsi que d'enregistrer une baisse de 28% des coûts en énergie et de 30% des coûts en eau ». (voir source)")

        if camembert == "Green Leader" :
            filtre = 'green_leader'
            titre = "Possède titre Green Leader : "
            container_camembert = st.beta_container()
            st.markdown("45%, soit **presque la moitié** des hôtels du groupe possèdent un eco-label GreenLeader. Cet eco-label est une mention décernée à certains établissement par TripAdvisor pour mettre en valeur leur démarche de respect de l'environnement.")

        # écriture du diagramme
        with container_camembert:
            fig = px.pie(dataframe_hotels, names = filtre, title = titre, color = filtre, color_discrete_map = {'non':'#ffc2c2','oui':'mediumseagreen'})
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.write(fig)

        if st.button('Source : NH Hotel Groups'):
            webbrowser.open_new_tab("https://www.nh-hotels.fr/environnement/hotels-ecologiques-developpement-durable")

    st.text("")

    # conteneur 2 - repartitions par critères :
    with st.beta_container() :
        st.markdown("**Présentons maintenant les répartitions d'hôtels écologiques/non écologiques en fonction de différentes catégories:** ")
        categorie = st.selectbox(
            "Répartition en fonction de :",
            ("Pays", "Continent", "Nombre d'étoiles")
        )
        if categorie == "Pays":
            filtre = "pays"
            titre = "Répartition par pays"
            container_barchart = st.beta_container()
            st.markdown("On observe tout d'abord que les hôtels proposés par NH Hotels en Allemagne sont à **grande majorité** (82,3%) des hôtels écologiques. C'est également le cas pour les Pays-Bas (97,1%), la Belgique (92,3%), l'Autriche (85,7%) et l'Italie (75,0%). Les répartitions en Espagne ou en France ne sont pas aussi bonnes (respectivement 34,7% et 40% d'hôtels écologiques), mais on note tout de même 33 établissements écologiques proposés en Espagne. Les chiffres des autres pays sont malheureusement trop bas pour être soumis à une analyse. Ces chiffres montrent que certains pays ont fermement entamé une démarche d'eco-responsibilisation, et offrent déjà de nombreux établissements constituant des bases solides pour un investisseur qui souhaiterait soutenir le développement du tourisme écologique.")

        if categorie == "Continent":
            filtre = "continent"
            titre = "Répartition par continent"
            container_barchart = st.beta_container()
            st.markdown("NH Hotels n'est malheureusement pas encore très développé en Afrique et au Moyen Orient. Pour pallier ce manque, il serait utile d'avoir un outil de recherche de logements écologiques qui rassemblerait les établissements de plusieurs groupes hôteliers, afin de couvrir davantage de secteurs. Analysons donc les chiffres pour l'Europe et l'Amérique. On constate que les logements écologiques sont majoritaires pour les hôtels en Europe (60,5%). L'Union Européenne a en effet mis l'accent sur la transition écologique au cours des dernières années, ce qui a aidé dans la démarche d'eco-responsabilisation de NH Hotels. Avec des investissements supplémentaires, ces chiffres pourraient être encore meilleurs, mais ils indiquent déjà le potentiel du tourisme écologique : la transition est en cours.")
            st.markdown("En ce qui concerne les Amériques, le processus est malheureusement plus lent : seulement 25% des hôtels NH Hotel ont la mention éco-responsable. Pour un voyageur souhaitant séjourner dans un logement éco-responsable en Amérique en ayant du choix, il semble donc essentiel d’avoir un outil qui puisse proposer les offres de plusieurs chaîne d’hôtels. La transition écologique est coûteuse, et les subventions gouvernementales ne suffisent souvent pas. Il serait donc également intéressant d'investir pour développer les infrastructures écologiques dans les Amériques, destination prisée de nombreux voyageurs à la conscience éco-responsable ! ")

        if categorie == "Nombre d'étoiles":
            filtre = "etoiles"
            titre = "Répartition par nombre d'étoiles (3, 4 ou 5)"
            container_barchart = st.beta_container()
            st.markdown("Les hôtels du groupe NH Hotels sont uniquement de standing 3, 4 ou 5 étoiles (exception faite de quelques cas non renseignés sur le site). Pour les hôtels de standing 3 ou 5 étoiles, les logements écologiques sont pour l'instant minoritaires. Les hôtels 4 étoiles sont en majorités des hôtels eco-responsables (60,8%). Les logements eco-responsables sont donc disponibles en grand nombre pour la tranche importante de voyageurs qui cherchent du confort sans pour autant opter pour les solutions les plus chères. On constate cependant un nombre non négligeable d’hôtels écologiques 5 étoiles (15 hôtels), qui montre que le luxe n'est pas nécessairement synonyme de gaspillage, et que le tourisme écologique est adaptable à toutes les exigences et à tous les standings !")

        # écriture du diagramme
        with container_barchart:
            filtered_df = dataframe_hotels.groupby([filtre, 'ecologique']).size().reset_index(name='counts')
            filtered_df['pourcentage'] = dataframe_hotels.groupby([filtre, 'ecologique']).size().groupby(level=0).apply(lambda x: 100 * x / float(x.sum())).values
            fig = px.bar(filtered_df, x = filtre, y = "counts", color = "ecologique", title = titre, color_discrete_map = {'non':'#ffc2c2','oui':'mediumseagreen'}, labels = {"counts": "nombre hôtels"}, text = filtered_df['pourcentage'].apply(lambda x: '{0:1.2f}%'.format(x)))
            fig.update_layout(barmode='group', xaxis_tickangle = -45)
            # pour ne pas avoir des "2.5, 3.5" dans l'axe x des étoiles, forcer le type catégorie :
            fig.update_xaxes(type='category')
            st.write(fig)
