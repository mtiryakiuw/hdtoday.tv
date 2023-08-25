import scrapy

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
            with open("myproject/links.csv", "rt") as f:
                start_urls = [url.strip() for url in f.readlines()][1:]
        except:
            start_urls = []

        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_movie)

    def parse_movie(self, response):
        movie_item = Movie()

        movie_item['name'] = response.xpath('//h2[@class="heading-name"]//text()').get()
        movie_item['imdb'] = response.xpath('//span[@class="item mr-2"]//text()').get()

        released = response.xpath('//span/strong[contains(text(), "Released:")]/following-sibling::text()').get()
        genres = response.xpath('//span/strong[contains(text(), "Genre:")]/following-sibling::a/text()').getall()
        casts = response.xpath('//span/strong[contains(text(), "Casts:")]/following-sibling::a/text()').getall()

        duration = response.xpath('//span/strong[contains(text(), "Duration:")]/following-sibling::text()').get()
        duration = duration.strip() if duration else None

        country = response.xpath('//span/strong[contains(text(), "Country:")]/following-sibling::a/text()').get()

        movie_item['released'] = released.strip() if released else None
        movie_item['genres'] = [genre.strip() for genre in genres]
        movie_item['casts'] = [cast.strip() for cast in casts]
        movie_item['duration'] = duration
        movie_item['country'] = country.strip() if country else None

        yield movie_item