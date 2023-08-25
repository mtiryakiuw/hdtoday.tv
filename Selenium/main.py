from selenium import webdriver
import pandas as pd
import re
from bs4 import BeautifulSoup

def scrape_movie_data(page_range):
    films = []
    chrome_options = webdriver.ChromeOptions()

    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://hdtoday.tv/movie')

    for page_num in range(page_range[0], page_range[1]):
        try:
            page_url = f"{driver.current_url}?page={page_num}"
            driver.get(page_url)

            all_links = [link.get('href') for link in BeautifulSoup(driver.page_source, features="html.parser").findAll('a')]

            base_url = 'https://hdtoday.tv/'
            movie_links = all_links[154:-16:2]

            for link in movie_links:
                main_url = base_url + link
                driver.get(main_url)
                movie_page_soup = BeautifulSoup(driver.page_source, 'html.parser')

                movie_name_section = movie_page_soup.find_all('h2', class_='heading-name')
                imdb_section = movie_page_soup.find_all('span', class_='item mr-2')

                imdb_rating = re.sub('<[^>]+>', '', str(imdb_section)).replace('[', '').replace(']', '').replace(
                    'IMDB: ', '')
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
                duration = duration_element.find_next_sibling(string=True).strip().replace('min', '').replace('\n','').replace(' ', '')
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

        except BaseException as error:
            print(error)

    driver.quit()

    df = pd.DataFrame(films)
    return df

# Example usage
page_range = (1, 2)
movie_details_df = scrape_movie_data(page_range)
print(movie_details_df)
