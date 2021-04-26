import streamlit as st
import pandas as pd

# Chargement des données - fonction avec cache pour éviter de re-charger à chaque fois
@st.cache
def load_data(path):
    frame = pd.read_csv(path)
    return frame
dataframe_hotels = load_data("data/hotels.csv")
dataframe_ntealan = load_data("data/ntealan_entrees.csv")
dataframe_nbentrees = load_data("data/dic_nb_entries.csv")

from .presentation import *
from .presentation_eco import *
from .engagement import *
from .popularite import *
from .conclusion_eco import *
from .presentation_dico import *
from .ntealan_chiffres import *
from .perspectives_dico import *
from .conclusions_dico import *
