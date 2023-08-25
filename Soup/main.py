import requests
import pandas as pd
import re
from bs4 import BeautifulSoup

def scrape_movie_details(page_range):
    films = []

    for page_num in range(page_range[0], page_range[1]):
        try:
            page_url = f'https://hdtoday.tv/movie?page={page_num}'
            page_response = requests.get(page_url)
            page_soup = BeautifulSoup(page_response.content, 'html.parser')

            all_page_links = [link.get('href') for link in page_soup.findAll('a')]

            base_url = 'https://hdtoday.tv'
            movie_links = all_page_links[154:-16:2]

            for movie_link in movie_links:
                movie_page_url = base_url + movie_link
                movie_page_response = requests.get(movie_page_url)
                movie_page_soup = BeautifulSoup(movie_page_response.content, 'html.parser')

                movie_info = movie_page_soup.find_all('div', class_='description')
                movie_name_section = movie_page_soup.find_all('h2', class_='heading-name')
                imdb_section = movie_page_soup.find_all('span', class_='item mr-2')

                movie_info_str = re.sub('<[^>]+>', '', str(movie_info)).replace('[', '').replace(']', '')
                imdb_rating = re.sub('<[^>]+>', '', str(imdb_section)).replace('[', '').replace(']', '').replace('IMDB: ','')
                movie_name = re.sub('<[^>]+>', '', str(movie_name_section)).replace('[', '').replace(']', '')

                release_date_element = movie_page_soup.find('span', string=re.compile(r'Released:'))
                release_date = release_date_element.find_next_sibling(string=True).strip()

                genres_element = movie_page_soup.find('span', string=re.compile(r'Genre:'))
                genres = [a.get_text(strip=True) for a in genres_element.find_next_siblings('a')]
                genres_line = ', '.join(genres)

                casts_element = movie_page_soup.find('span', string=re.compile(r'Casts:'))
                casts = [a.get_text(strip=True) for a in casts_element.find_next_siblings('a')]
                casts_line = ', '.join(casts)

                duration_element = movie_page_soup.find('span', string=re.compile(r'Duration:'))
                duration = duration_element.find_next_sibling(string=True).strip().replace('min', '').replace('\n', '').replace(' ', '')
                formatted_duration = f"{duration} min"

                country_element = movie_page_soup.find('span', string=re.compile(r'Country:'))
                country = country_element.find_next('a').get_text(strip=True)

                films.append({
                    'Movie_Name': movie_name,
                    'Release_Date': release_date,
                    'Genres': genres_line,
                    'Casts': casts_line,
                    'Duration': formatted_duration,
                    'Country': country,
                    'IMDB_Rating': imdb_rating
                })
        except:
            continue

    df = pd.DataFrame(films)
    return df

# Example usage
page_range = (1, 2)
movie_details_df = scrape_movie_details(page_range)
print(movie_details_df)
