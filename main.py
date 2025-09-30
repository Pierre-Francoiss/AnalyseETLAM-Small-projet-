import requests
import pandas as pd
from datetime import datetime


data=[]

url=f"https://data.ampmetropole.fr/api/explore/v2.1/catalog/datasets/point-dinteret-datatourisme-multi-niveaux/records?limit=20&refine=niv1_categorie%3A%22F%C3%AAte%20et%20manifestation%22"
response= requests.get(url)
json_data=response.json()
results=json_data['results']


df = pd.DataFrame(results)
print(df.head(10))