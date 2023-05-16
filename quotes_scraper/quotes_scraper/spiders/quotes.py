import scrapy

# Titulo = //h1/a/text()
# Cita = //span[@class="text" and @itemprop="text"]/text()
# Top ten tags = //div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()
# Next page button = //li[@class="next"]/a/@href


class QuotesSpyder(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'http://quotes.toscrape.com/page/1/'
    ]


    custom_settings = {
        'FEED_URI': 'quotes.json',
        'FEED_FORMAT': 'json',
        #'CONCURRENT_REQUESTS': 24,
        #'MEMUSAGE_LIMIT_MB': 2048,
        #'MEMUSAGE_NOTIFY_MAIL': ['email'],
        #'ROBOTSTXT_OBEY': True,
        #'USER_AGENT': 'QuotesSpyder (http://quotes.toscrape.com)',
        #'FEED_EXPORT_ENCODING': 'utf-8',
        #'HTTPCACHE_ENABLED': True,
        #'HTTPCACHE_EXPIRATION_SECS': 86400,
        #'HTTPCACHE_DIR': 'httpcache',
        #'HTTPCACHE_IGNORE_HTTP_CODES': [],
        #'HTTPCACHE_STORAGE': 'scrapy.extensions.httpcache.FilesystemCacheStorage',
        #'LOG_LEVEL': 'INFO',
        #'LOG_FILE': 'log.txt',
        #'LOG_FORMAT': '%(levelname)s: %(message)s',
        #'LOG_STDOUT': True,
        #'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
        #'JOBDIR': 'quotes_scraper/jobs',
    }

    def parse_only_quotes(self, response, **kwargs):
        if kwargs:
            quotes = kwargs['quotes']
        quotes.extend(response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall())

        next_page_button = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page_button:
            yield response.follow(next_page_button, callback=self.parse_only_quotes, cb_kwargs={'quotes': quotes})
        else:
            yield {
                'quotes': quotes
            }

    def parse(self, response):
        
        title = response.xpath(
            '//h1/a/text()').get()        
        quotes = response.xpath(
            '//span[@class="text" and @itemprop="text"]/text()').getall()
        top_tags = response.xpath(
            '//div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()').getall()
        
        
        top = getattr(self, 'top', None) # top es un atributo de la clase QuotesSpyder. Si existe, se le asigna a top, si no, se le asigna None

        if top:
            top = int(top)
            top_tags = top_tags[:top]

        # Luego, en la consola, se ejecuta:
        # scrapy crawl quotes -a top=3
        # para que solo se muestren las 3 primeras etiquetas

        yield {
            'title': title,
            'top_tags': top_tags
        }

        next_page_button = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page_button:
            yield response.follow(next_page_button, callback=self.parse_only_quotes, cb_kwargs={'quotes': quotes})

