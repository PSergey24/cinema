import requests
import time
import pandas as pd
from bs4 import BeautifulSoup


# parse img and description to movies
def parse_movies():
    df = pd.read_csv('data/movies.csv', sep='\t', on_bad_lines='skip')
    df_2 = pd.read_csv('data/movies_2.csv', sep='\t', on_bad_lines='skip')

    for i, row in df.iterrows():

        if isinstance(df_2.loc[i, 'linkImg'], float) is False:
            continue

        # 404 page
        if row["tconst"] in ['tt3704428']:
            continue

        link = 'https://www.movieposterdb.com/search?q=' + row['tconst']

        soup = get_soup(link)

        if soup.find_all(attrs={"class": ["mt-1"]})[0].text.find('0 results for') != -1:
            print(f'{i}, {row["name"]}: not info')
            continue

        link_description = soup.find_all(attrs={"class": ["vertical-image"]})[0].parent['href']

        time.sleep(3)
        soup_description = get_soup('https://www.movieposterdb.com' + link_description)

        description = soup_description.find_all(attrs={"class": ["py-0"]})[0].find('p').text
        if soup.find_all(attrs={"class": ["vertical-image"]})[0].has_attr("data-src"):
            src = soup.find_all(attrs={"class": ["vertical-image"]})[0].attrs["data-src"]
        elif len(soup_description.find_all(attrs={"class": ["vertical-image"]})) > 0 and soup_description.find_all(attrs={"class": ["vertical-image"]})[0].has_attr("data-src"):
            src = soup_description.find_all(attrs={"class": ["vertical-image"]})[0].attrs["data-src"]
        else:
            src = ''

        df_2.loc[i, 'linkImg'] = src
        df_2.loc[i, 'description'] = description

        print(f'{i}, {row["name"]}')
        df_2.to_csv('data/movies_2.csv', index=False, sep='\t')
        time.sleep(2)


def get_soup(link):
    response = requests.get(link)
    return BeautifulSoup(response.text, "html.parser")
