import scrapy

# Titulo = //h1/a/text()
# Cita = //span[@class="text" and @itemprop="text"]/text()
# Autor = //small[@class="author" and @itemprop="author"]/text()
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
        'CONCURRENT_REQUESTS': 30,
        'MEMUSAGE_LIMIT_MB': 2048,
        'MEMUSAGE_NOTIFY_MAIL': ['tupy77@hotmail.com'],
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT': 'QuotesSpyder test',
        'FEED_EXPORT_ENCODING': 'utf-8',
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
            author = kwargs['author']
        quotes.extend(response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall())
        author.extend(response.xpath('//small[@class="author" and @itemprop="author"]/text()').getall())

        next_page_button = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page_button:
            yield response.follow(next_page_button, callback=self.parse_only_quotes, cb_kwargs={'quotes': quotes, 'author': author})
        else:
            yield {
                'quotes': quotes,
                'author': author
            }

    def parse(self, response):
        
        title = response.xpath(
            '//h1/a/text()').get()        
        quotes = response.xpath(
            '//span[@class="text" and @itemprop="text"]/text()').getall()
        author = response.xpath(
            '//small[@class="author" and @itemprop="author"]/text()').getall()
        top_tags = response.xpath(
            '//div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()').getall()
        
        
        top = getattr(self, 'top', None) # getattr() es una funcion de python que permite obtener un atributo de un objeto

        if top:
            top = int(top)
            top_tags = top_tags[:top]

        yield {
            'title': title,
            'top_tags': top_tags
        }

        next_page_button = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page_button:
            yield response.follow(next_page_button, callback=self.parse_only_quotes, cb_kwargs={'quotes': quotes, 'author': author})

