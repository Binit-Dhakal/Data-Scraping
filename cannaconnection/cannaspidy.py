import scrapy
import string
import re

class CannaspidySpider(scrapy.Spider):
    name = 'cannaspidy'
    # allowed_domains = ['https://www.cannaconnection.com/strains']
    # start_urls = ['https://www.cannaconnection.com/strains?show_char=a']

    def start_requests(self):
        urls = [f"https://www.cannaconnection.com/strains?show_char={ch}" for ch in string.ascii_lowercase]
        urls.append("https://www.cannaconnection.com/strains?show_char=0-9")

        for url in urls:
            yield scrapy.Request(url = url, callback = self.parse)

    def parse(self, response):
        for r in response.xpath('//ul[contains(@class,"strains-list")]/li/a/@href'):
            yield scrapy.Request(url = r.get(), callback = self.parse)
            
            title = response.xpath('//div[contains(@class,"post-content")]/h1/text()')
            top_right = response.xpath('//div[contains(@class,"feature-wrapper")]/div[contains(@class,"feature-title")]')
            
            rows = {key.xpath('.//text()').get():[] for key in top_right}
            for key in top_right:
                for k in key.xpath('.//following-sibling::div/text()'):
                    if k.get() == "\n":
                        k = key.xpath('.//following-sibling::div/a/text()')
                        if re.sub('/n','',k.get()) in rows[key.xpath('.//text()').get()]:
                            continue
                    rows[key.xpath('.//text()').get()].append(re.sub('\n','',k.get()))
            for key,val in rows.items():
                rows[key] = ",".join(val)
            rows['title'] = title

            description = " "
            for r in response.xpath('response.xpath("//div[@class="rte"]/p/text()")'):
                description += r.get()
            rows['description'] = description

            list_of_keys = [x.get() for x in response.xpath('//dl[@class="data-sheet"]/dt/text()')]
            list_of_vals = [re.sub('\n',"",x.get()) for x in response.xpath('//dl[@class="data-sheet"]/dt/following-sibling::dd/text()')]

            extraProductiveFeature = dict(zip(list_of_keys,list_of_vals))
            rows.update(extraProductiveFeature)
            breeder_name = response.xpath('//div[@class="breeder-name"]/text(').get()
            rows['breeder_name'] = breeder_name

            yield(rows)