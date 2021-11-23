from selenium import webdriver

driver = webdriver.Firefox()
driver.get('https://www.certik.org/')
project_link = []

next_btn = driver.find_element_by_xpath('//*[@id="projects"]/div[2]/div/div[2]/div[2]/div/ul/li[9]/button[1]')

while(True):
    table = driver.find_element_by_xpath('//*[@id="projects"]/div[2]/div/div[1]/div/div/div/div/div/div/table/tbody')
    elems = table.find_elements_by_tag_name('a')

    for elem in elems:
        href = elem.get_attribute('href')
        project_link.append(href)
    
    if (not next_btn.is_enabled()):
        break
    else:
        next_btn.click()


driver.close()

with open('a_file.txt','w') as f:
    for item in project_link:
        f.write(item + '\n')


'''
    sec_score = response.selector.xpath('//*[@id="__next"]/div/div[2]/div/div/div[2]/div[1]/div/div[2]/div/div[1]/div/div[1]/svg/text[1]/text()').get()
    ticker = response.selector.xpath('//*[@id="__next"]/div/div[2]/div/div/div[2]/div[2]/div/div[1]/div/div[1]/div[2]/text()').get()
    name = response.selector.xpath('//*[@id="__next"]/div/div[2]/div/div/div[1]/div[1]/div/div[2]/h1/text()').get()
    market_cap (easy)
    onboard_date(easy)
    security_type = response.selector.xpath('//*[@id="audit"]/div/div[2]/div/div/div[2]/div/div[3]/div[1]/div[1]/div/div/div[2]/h4/text()').get()
    language = response.selector.xpath('//*[@id="audit"]/div/div[2]/div/div/div[2]/div/div[3]/div[2]/div[1]/div/div/div[2]/h4/text()').get()
    req_date = response.selector.xpath('//*[@id="audit"]/div/div[2]/div/div/div[2]/div/div[3]/div[1]/div[2]/div/div/div[2]/h4/text()').get()
    rev_date =  response.selector.xpath('//*[@id="audit"]/div/div[2]/div/div/div[2]/div/div[3]/div[2]/div[2]/div/div/div[2]/h4/text()').get()
    total_find = response.selector.xpath('//*[@id="audit"]/div/div[2]/div/div/div[2]/div/div[4]/div[1]/div/svg/text[1]/text()').get()
'''
'''
take2 = response.selector.css('div.ant-col.ant-col-0.ant-col-md-10')[1]
take2.css('span::text').get().strip()
'''
