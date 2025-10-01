import requests
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns


data=[]

url=f"https://data.ampmetropole.fr/api/explore/v2.1/catalog/datasets/point-dinteret-datatourisme-multi-niveaux/records?limit=50&refine=niv1_categorie%3A%22F%C3%AAte%20et%20manifestation%22"
response= requests.get(url)
json_data=response.json()
results=json_data['results']


df = pd.DataFrame(results)
print(df.head(10))
print(df.columns)
print("taille du data frame :", df.shape)

commune_counts = df['commune'].value_counts()
print(commune_counts)

plt.figure(figsize=(10, 6))
sns.barplot(x=commune_counts.index, y=commune_counts.values, palette='viridis')
plt.title('Nombre d\'événements par commune')
plt.xlabel('Commune')
plt.ylabel('Nombre d\'événements')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()