import json
import scrapy
from sys import stdout
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from settings import db, api_key


class MainSpider(scrapy.Spider):
    name = 'main'
    count = 0  # to count parsed orders
    hypixel_url = f'https://api.hypixel.net/skyblock/auctions?key={api_key}'  # url to parse

    def start_requests(self):
        # requesting 0 page to get total pages
        yield scrapy.Request(''.join((self.hypixel_url, '&page=0')), callback=self.parse_pages)

    def parse_pages(self, response, **kwargs):
        data = json.loads(response.text)    # getting response text and transforming it to dictionary
        # parsing all available pages
        for page in range(data['totalPages'] + 1):
            page_url = ''.join((self.hypixel_url, f'&page={page}'))
            yield scrapy.Request(page_url, callback=self.parse)

    def parse(self, response, **kwargs):
        data = json.loads(response.text)
        for order in data['auctions']:
            db.upload_order_to_db(order)
            self.count += 1
            if need_progress:
                stdout.write(f'\rCollecting orders {self.count}/{data["totalAuctions"]}')


def run_spider(need_progress_=True):
    global need_progress
    need_progress = need_progress_
    db.clear_orders()
    process = CrawlerProcess(settings=get_project_settings())
    process.crawl(MainSpider)
    process.start()
    db.save()
    if need_progress_: print()


need_progress = True
