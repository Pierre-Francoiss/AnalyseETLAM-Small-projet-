import requests
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


data=[]

#Récupération des données API

urlEvents=f"https://data.ampmetropole.fr/api/explore/v2.1/catalog/datasets/point-dinteret-datatourisme-multi-niveaux/records?limit=50&refine=niv1_categorie%3A%22F%C3%AAte%20et%20manifestation%22"
responseEvent= requests.get(urlEvents)
jsonDataEvent=responseEvent.json()
resultsEvent=jsonDataEvent['results']

urlCom=f"https://geo.api.gouv.fr/communes"
responseCom= requests.get(urlCom)
resultsCom=responseCom.json()


#Transformation en DataFrame + test des dataframes

dfEve = pd.DataFrame(resultsEvent)
#print(dfEve.head(10))
#print(dfEve.columns)
#print("taille du data frame :", dfEve.shape)

dfCom = pd.DataFrame(resultsCom)
#print(dfCom.head(10))
#print(dfCom.columns)
#print("taille du data frame :", dfCom.shape)

# Harmoniser les noms des communes dans dfEve
dfEve['commune'] = dfEve['commune'].replace(
    to_replace=r"Marseille .* Arrondissement",
    value="Marseille",
    regex=True
)

# Vérification des noms des communes
print(dfEve['commune'].unique())


#Visualisation du nombre d'événements par commune
commune_counts = dfEve['commune'].value_counts()


#Identfication de la densité d'événements relativement à la population des communes
merged_df = pd.merge(dfEve, dfCom, left_on='commune', right_on='nom', how='left')
merged_df['density'] = merged_df['commune'].map(merged_df['commune'].value_counts()) / merged_df['population']
print(merged_df[['commune', 'population', 'density']].drop_duplicates())
print(merged_df[['commune', 'population', 'density']].drop_duplicates().sort_values(by='density', ascending=False))

#Visualisation de la densité d'événements par commune rangé par densité
plt.figure(figsize=(10, 6))
sns.barplot(x='commune', y='density', data=merged_df.drop_duplicates(subset=['commune']), palette='magma', order=merged_df.drop_duplicates(subset=['commune']).sort_values(by='density', ascending=False)['commune'])
plt.title('Densité d\'événements par commune')
plt.xlabel('Commune')
plt.ylabel('Densité d\'événements (événements par habitant)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#Analyse temporelle des événements


#Création du dashboard
st.set_page_config(page_title="Analyse des événements festifs et manifestations Métropole Aix-Marseille-Provence", layout="wide")
#titre
st.title("Analyse des événements festifs et manifestations Métropole Aix-Marseille-Provence")
#nombre d'events
st.subheader("Nombre d'événements par commune")
st.bar_chart(commune_counts)
#nombre d'events par commune"
st.subheader("Densité d'événements par commune")
st.bar_chart(merged_df.drop_duplicates(subset=['commune']).set_index('commune')['density'].sort_values(ascending=False))
#histogramme des événements par mois
st.write("Densité d'événements par commune (événements par habitant)")
st.dataframe(merged_df[['commune', 'population', 'density']].drop_duplicates().sort_values(by='density', ascending=False))
#carte des événements
st.subheader("Carte des événements")
st.map(merged_df.dropna(subset=['latitude', 'longitude']).rename(columns={'latitude': 'lat', 'longitude': 'lon'})[['lat', 'lon']])
st.write("Données sources : [DataTourisme](https://data.ampmetropole.fr/explore/dataset/point-dinteret-datatourisme-multi-niveaux/information/) et [API Découpage administratif des communes](https://geo.api.gouv.fr/communes)")
