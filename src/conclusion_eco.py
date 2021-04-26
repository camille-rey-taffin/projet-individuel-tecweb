# -*- coding: utf-8 -*-
# script contenant la fonction pour générer la sous-rubrique "conclusion "
# de la rubrique "tourisme écologique"

import streamlit as st
import pandas as pd
import math
from src import dataframe_hotels

def recherche_hotel(pays_select, villes_select, eco_only):
    '''
    Recherche les hôtels selon des critères de selection:
    params : pays_select - string, pays sélectionné
            villes_select - list of strings, ville(s) sélectionnée(s)
            eco_only - boolean, filtre par critère écologique
    return : resultats - dataframa pandas, résultats de la recherche
    '''

    resultats = dataframe_hotels[dataframe_hotels["pays"] == pays_select]
    if len(villes_select) > 0 :
        resultats = resultats[resultats["ville"].isin(villes_select)]
    if eco_only :
        resultats = resultats[resultats["ecologique"] == "oui"]

    return resultats

def affichage_resultat(resultats):
    '''
    Affiche les resultats d'une recherche d'hôtels
    param : resultats - dataframe pandas, résultats de la recherche
    '''

    st.markdown("**Résultats :**")
    if resultats.empty:
        st.markdown("### **Aucun résultat pour vos critères de recherche**")
    else :
        for index, result in resultats.iterrows():
            etoiles = int(result['etoiles'])*":star:" if not math.isnan(result['etoiles']) else ""
            if result["ecologique"] == "oui":
                st.success(f"{result['nom']} {etoiles}")
            else :
                st.error(f"{result['nom']} {etoiles}")
            st.write(f"Lien vers la page de l'hôtel [ici]({result['lien']})")

def conclusion_eco():
    '''
    Conclusion sur l'étude NH Hotel Group
    '''

    st.subheader("Conclusion et petite illustration")
    st.text("")
    st.text("")
    st.markdown("### **Conclusion**")
    st.markdown("Nous avons montré à travers diverses analyses statistiques que les logements écologiques sont déjà solidement implantés dans le paysage du tourisme, et qu’ils jouissent de fortes popularité, visibilité et capacité (cf rubriques « Engagement écologique » et « Capacité et popularité » dans la barre latérale). L’hôtellerie éco-responsable est donc un domaine **fiable pour l’investissement**, et promis à un grand développement dans les années futures. Pour jouer un rôle important dans cet essor, nous vous proposons d’investir dans le développement de l’outil « Ecôtel », une plateforme de recherche de logements écologiques qui permettrait aux voyageurs soucieux de l’environnement d’accéder à un grand choix d’établissements parmi de nombreux partenaires. Les différents groupes hôteliers, bien qu’offrant souvent une gamme de logement éco-responsables, ne proposent malheureusement que très rarement des options de recherche avec critère d’éco-responsabilité. La plateforme Ecôtel permettrait de filtrer selon des critères d’éco-responsabilité, et de regrouper les offres de différents groupes hôteliers.")

    st.markdown("Nous vous proposons ci-dessous un prototype très simplifié d’outil de recherche de logements éco-responsables en guise d’illustration. Vous devez d'abord choisir un pays, puis vous pouvez ajouter un filtre par ville(s), et enfin un filtre optionnel par éco-responsabilité. Les résultats s'afficheront en vert pour les hôtels éco-responsables, et en rouge sinon. Cet outil n’est basé que sur les données de NH Hotels Group :")

    # prototype d'outil de recherche
    pays = [''] + list(dataframe_hotels.pays.unique())
    pays_select = st.selectbox('Saisissez / Sélectionnez un pays', options = pays, index = 0)
    villes = list(dataframe_hotels[dataframe_hotels["pays"] == pays_select].ville.unique())
    villes_select = st.multiselect('Saisissez / Sélectionnez une ou plusieurs ville(s)',options = villes, default = [] )
    eco_only = st.checkbox("logements eco-responsables uniquement")

    # lancement de la recherche
    if pays_select :
        recherche = st.button('Rechercher')
        if recherche:
            st.balloons()

            #recherche des résultats
            resultats = recherche_hotel(pays_select, villes_select, eco_only)

            # affichage des résultats
            affichage_resultat(resultats)
