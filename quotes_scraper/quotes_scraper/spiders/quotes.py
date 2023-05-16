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

    def parse(self, response):
        
        # PROBAR RESPUESTAS
        # print(response.status, response.headers)
        #print('\n\n', '*' * 50, '\n\n')
        
        # VER DATOS EN CONSOLA
        # print ('\n\n','*' * 50, '\n\n')
        # title = response.xpath('//h1/a/text()').get()
        # print(f'Titulo: {title}')
        # print('\n\n', '*' * 50, '\n\n')
        # quotes = response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall()
        # print('Citas: ')
        # for quote in quotes:
        #     print(f'- {quote}')
        # print('\n\n', '*' * 50, '\n\n')
        # top_ten_tags = response.xpath('//div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()')
        # print('Top ten tags: ')
        # for tag in top_ten_tags:
        #     print(f'- {tag.get()}')
        # print('\n\n', '*' * 50, '\n\n')

        
        title = response.xpath(
            '//h1/a/text()').get()        
        quotes = response.xpath(
            '//span[@class="text" and @itemprop="text"]/text()').getall()
        top_ten_tags = response.xpath(
            '//div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()').getall()

        yield {
            'title': title,
            'quotes': quotes,
            'top_ten_tags': top_ten_tags
        }

        next_page_button = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page_button:
            yield response.follow(next_page_button, callback=self.parse)

