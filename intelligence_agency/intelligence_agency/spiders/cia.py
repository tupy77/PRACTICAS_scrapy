import scrapy

# si se quieren ver los objetos por consola del navegador se tendria que usar la siguiente linea:
# $x('//a[starts-with(@href, "collection") and (parent::h3|parent::h2)]/@href').values()

# Si quieres buscar a traves del scrapy shell, se puede hacer de la siguiente manera:
# Primero, en el cmd, se debe de ejecutar el siguiente comando:
#       scrapy shell 'https://www.cia.gov/readingroom/historical-collections'
# Despues, se debe de ejecutar el siguiente comando:
#       response.xpath('//a[starts-with(@href, "collection") and (parent::h3|parent::h2)]/@href').getall()

#para terminar vamos colocando los links que queremos obtener en las siguientes lineas que son las que usaremos:

# links = '//a[starts-with(@href, "collection") and (parent::h3|parent::h2)]/@href'
# title = response.xpath('//h1[@class="documentFirstHeading"]/text()').get()
# paragraph = response.xpath('//div[@class="field-item even"]//p[not(@class)]/text()').get()


class CiaSpider(scrapy.Spider):
    name = 'cia'
    #allowed_domains = ['www.cia.gov']
    start_urls = ['https://www.cia.gov/readingroom/historical-collections']
    custom_settings = {
        'FEED_URI': 'cia.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse(self, response):
        links_declassified = response.xpath('//a[starts-with(@href, "collection") and (parent::h3|parent::h2)]/@href').getall()
        for link in links_declassified:
            yield response.follow(link, callback=self.parse_link, cb_kwargs={'url': response.urljoin(link)})

    def parse_link(self, response, **kwargs):
        link = kwargs['url']
        title = response.xpath('//h1[@class="documentFirstHeading"]/text()').get()
        paragraph = response.xpath('//div[@class="field-item even"]//p[not(@class)]/text()').get()

        yield {
            'url': link,
            'title': title,
            'body': paragraph
        }