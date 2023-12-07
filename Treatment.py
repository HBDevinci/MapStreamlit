import pandas as pd

reefs = pd.read_csv('deep_sea_corals.csv')
oceans = pd.read_csv('CODAP_NA_v2021.csv')

columns_to_keep = ['ScientificName', 'VernacularNameCategory', 'TaxonRank', 'ObservationDate', 
                   'latitude', 'longitude', 'DepthInMeters', 'Locality']
columns_to_drop = [x for x in list(reefs.columns) if x not in columns_to_keep ]
#columns_to_drop = ['CatalogNumber', 'DataProvider', 'Station', 'DepthMethod', 'Locality']

reefs.drop(columns=columns_to_drop, axis=1, inplace=True)

reefs.drop(index=reefs.index[0], axis=0, inplace=True)

reefs.dropna(axis=0, how='any', inplace=True)

reefs.latitude = reefs.latitude.astype(float)
reefs.longitude = reefs.longitude.astype(float)

pd.to_datetime(reefs.ObservationDate, format='%Y-%m-%d', errors='coerce')

def extract_year(date):
    if len(date) >= 4:
        return date.split('-')[0]
    else:
        return date
    
reefs['ObservationYear'] = reefs['ObservationDate'].astype(str).apply(extract_year)

reefs.drop(axis=1, columns=['ObservationDate'], inplace=True)

reefs.loc[417782, 'ObservationYear'] = reefs.loc[417782, 'ObservationYear'][-4:]
reefs['ObservationYear'] = pd.to_datetime(reefs['ObservationYear'], errors='coerce').dt.year

reefs_sorted = reefs.sort_values(by='ObservationYear')

subset_1842_1900 = reefs_sorted.loc[reefs_sorted['ObservationYear'].between(1842, 1900)]

subset_1901_1950 = reefs_sorted.loc[reefs_sorted['ObservationYear'].between(1901, 1950)]

subset_1951_2000 = reefs_sorted.loc[reefs_sorted['ObservationYear'].between(1951, 2000)]

subset_2001_2016 = reefs_sorted.loc[reefs_sorted['ObservationYear'].between(2001, 2016)]

dates = reefs_sorted["ObservationYear"].unique()