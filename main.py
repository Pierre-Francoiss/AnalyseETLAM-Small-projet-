import requests
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns


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
print(dfEve.head(10))
print(dfEve.columns)
print("taille du data frame :", dfEve.shape)

dfCom = pd.DataFrame(resultsCom)
print(dfCom.head(10))
print(dfCom.columns)
print("taille du data frame :", dfCom.shape)



#Visualisation du nombre d'événements par commune
commune_counts = dfEve['commune'].value_counts()
print(commune_counts)
"""
plt.figure(figsize=(10, 6))
sns.barplot(x=commune_counts.index, y=commune_counts.values, palette='viridis')
plt.title('Nombre d\'événements par commune')
plt.xlabel('Commune')
plt.ylabel('Nombre d\'événements')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
"""