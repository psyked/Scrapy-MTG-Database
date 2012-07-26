from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from mtg.items import CardItem

class CardSpider(BaseSpider):
   name = "cards"
   allowed_domains = ["gatherer.wizards.com"]
   start_urls = [
       "http://gatherer.wizards.com/Pages/Search/Default.aspx?action=advanced&set=+[%22Magic%202013%22]"
   ]

   def parse(self, response):
       hxs = HtmlXPathSelector(response)
       sites = hxs.select('//div[@class="cardInfo"]')
       items = []
       for site in sites:
           item = CardItem()
           item['cardname'] = site.select('span[@class="cardTitle"]/a/text()').extract()
           item['convertedmana'] = site.select('span[@class="convertedManaCost"]/text()').extract()
           item['types'] = site.select('span[@class="typeLine"]/text()').extract()[0].strip()
           item['cardtext'] = site.select('div[@class="rulesText"]/p/text()').extract()
           #item['pt'] = site.select('span[@class="cardTitle"]/a/text()').extract()
           #item['expansion'] = site.select('span[@class="cardTitle"]/a/text()').extract()
           #item['rarity'] = site.select('span[@class="cardTitle"]/a/text()').extract()
           #item['allsets'] = site.select('span[@class="cardTitle"]/a/text()').extract()
           #item['cardnumber'] = site.select('span[@class="cardTitle"]/a/text()').extract()
           #item['artist'] = site.select('span[@class="cardTitle"]/a/text()').extract()
           #item['rating'] = site.select('span[@class="cardTitle"]/a/text()').extract()
           #item['link'] = site.select('span[@class="cardTitle"]/a/text()').extract()
           #item['uid'] = site.select('span[@class="cardTitle"]/a/text()').extract()
           items.append(item)
       return items