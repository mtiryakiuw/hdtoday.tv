import scrapy
import re
from bs4 import BeautifulSoup

class Link(scrapy.Item):
    link = scrapy.Field()

class LinkListsSpider(scrapy.Spider):
    name = 'LinkListsSpider'
    allowed_domains = ['hdtoday.tv']
    start_urls = ['https://hdtoday.tv/home']

    def parse(self, response):
        link_elements = response.xpath('//h3[@class="film-name"]//@href').getall()
        for link in link_elements:
            absolute_link = response.urljoin(link)
            yield Link(link=absolute_link)

class Movie(scrapy.Item):
    name = scrapy.Field()
    imdb = scrapy.Field()
    duration = scrapy.Field()
    country = scrapy.Field()
    released = scrapy.Field()
    genres = scrapy.Field()
    casts = scrapy.Field()

class MoviesSpider(scrapy.Spider):
    name = 'MoviesSpider'
    allowed_domains = ['hdtoday.tv']

    def start_requests(self):
        try:
            with open("links.csv", "rt") as f:
                start_urls = [url.strip() for url in f.readlines()][1:]
        except:
            start_urls = []

        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_movie)

    def parse_movie(self, response):
        movie_item = Movie()

        movie_item['name'] = response.xpath('//h2[@class="heading-name"]//text()').get()
        imdb_rating_text = response.xpath('//span[@class="item mr-2"]//text()').get()
        imdb_rating = re.search(r'\d+(\.\d+)?', imdb_rating_text)

        if imdb_rating:
            movie_item['imdb'] = imdb_rating.group()
        else:
            movie_item['imdb'] = None

        # Parse the HTML content using Beautiful Soup
        movie_page_soup = BeautifulSoup(response.body, 'html.parser')

        release_date_element = movie_page_soup.find('span', string=re.compile(r'Released:'))
        release_date = release_date_element.find_next_sibling(string=True).strip()

        genres_element = movie_page_soup.find('span', string=re.compile(r'Genre:'))
        genres = [a.get_text(strip=True) for a in genres_element.find_next_siblings('a')]
        genres_line = ', '.join(genres)

        casts_element = movie_page_soup.find('span', string=re.compile(r'Casts:'))
        casts = [a.get_text(strip=True) for a in casts_element.find_next_siblings('a')]
        casts_line = ', '.join(casts)

        duration_element = movie_page_soup.find('span', string=re.compile(r'Duration:'))
        duration = duration_element.find_next_sibling(string=True).strip().replace('min', '').replace('\n', '').replace(
            ' ', '')
        formatted_duration = f"{duration} min"

        country_element = movie_page_soup.find('span', string=re.compile(r'Country:'))
        country = country_element.find_next('a').get_text(strip=True)

        movie_item['released'] = release_date
        movie_item['genres'] = genres
        movie_item['casts'] = casts_line
        movie_item['duration'] = duration
        movie_item['country'] = country

        yield movie_item
