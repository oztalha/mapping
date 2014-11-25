# coding: utf-8
import pandas as pd

from math import radians, cos, sin, asin, sqrt

def remove_duplicates(df, cols_to_consider):
    grouped = df.groupby(cols_to_consider)
    index = [gp_keys[0] for gp_keys in grouped.groups.values()]
    unique_df = df.reindex(index)
    return unique_df


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance (in miles) between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 

    # 6367 km is the radius of the Earth
    # 1 km is 0.621371 mile
    mi = 6367 * c * 0.621371
    return mi # return in miles

#PO box zip codes are not here !
census = pd.read_table('data/census_2010.tsv',dtype={'GEOID':str},usecols=['GEOID',7,8])
census.rename(columns=lambda x: x.strip(), inplace=True)

myzips = pd.read_table('data/missing_surgery.csv',dtype=str)
# myzips.zipcode[myzips.zipcode.str.len()<5] #251 such zips
merged = pd.merge(myzips,census,how='inner',left_on='zipcode',right_on='GEOID')
unigeo = remove_duplicates(merged,merged.zipcode)
unigeo.to_csv('data/unigeo.csv',index=False)
