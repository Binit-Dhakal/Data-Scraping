import scrapy
import json

class CoinSpider(scrapy.Spider):
    name = "coinspider"

    def start_requests(self):
        with open('/home/binit/python files/Python/SCRAPY_PROJECT/coin/a_file.txt','r') as f:
            start_urls = f.read().split('\n')
        
        for url in start_urls:
            yield scrapy.Request(url)

    def parse(self,response):
        issues_dict = {'Informational': [],'Major' : [], 'Medium': [], 'Minor': [], 'Critical' : [], 'Discussion':[]}
        final =response.selector.xpath('//*[@id="__NEXT_DATA__"]/text()').get()
        final = json.loads(final)['props']['pageProps']['project']
            
        try:
            issueses = final['audits'][0]['issues']
            for j in issueses:
                if(j['type'][0] not in issues_dict[j['severity']]):
                    issues_dict[j['severity']].append(j['type'][0])
        except:
            pass

        name = final['name'] 

        try:    ticker = final['tokenTickers']
        except:     ticker = None

        try:    sec_score = final['securityScore']
        except:     sec_score = None
        
        try:    lang = final['audits'][0]['language']
        except:     lang = []

        try:    types = final['audits'][0]["type"]
        except: types = ""
        
        try:    rev_date = final['audits'][0]['revisionDate']
        except:     rev_date = None

        try:    
            req_date = final['audits'][0]['requestDate']
        except:     req_date = None
        
        #for market cap - handling exception
        
        try:    cap = response.selector.xpath('//*[@id="__next"]/div/div[2]/div/div/div[2]/div[2]/div/div[1]/div/div[2]/div[3]/div[1]/div[2]/div/div/text()')[1].get()
        except:     cap = "unavailable"

        yield({
            "Project Name" : name,
            "Ticker" : ticker,
            "Security Score" : sec_score,
            "Market Cap" : cap,
            "Onboard Date" : response.selector.xpath('//*[@id="__next"]/div/div[2]/div/div/div[1]/div[1]/div/div[3]/div/div[2]/text()')[1].get(),
            "Type" : types,
            "Language" : lang,
            "Request Date" : req_date,
            "Revision Date" :  rev_date,
            "Total Findings" : response.selector.xpath('//*[@id="audit"]/div/div[2]/div/div/div[2]/div/div[4]/div[1]/div/svg/text[1]/text()').get(),
            "Critical" : issues_dict["Critical"],
            "Major" : issues_dict["Major"],
            "Minor" : issues_dict["Minor"],
            "Medium" : issues_dict["Medium"],
            "Informational" : issues_dict['Informational'],
        })