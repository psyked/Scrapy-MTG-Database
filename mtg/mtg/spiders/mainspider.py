from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request

from mtg.items import CardItem

class CardSpider(BaseSpider):
   name = "cards"
   allowed_domains = ["gatherer.wizards.com"]
   start_urls = [
       "http://gatherer.wizards.com/Pages/Search/Default.aspx?action=advanced&set=+[%22Magic%202013%22]"
   ]

   def parse(self, response):
       hxs = HtmlXPathSelector(response)
       
       next_page = hxs.select("//div[@class='pagingControls']/a[contains(text(),'>')]/@href").extract()
       if not not next_page:
            yield Request("http://gatherer.wizards.com" + next_page[0], self.parse) 

       cards = hxs.select('//div[@class="cardInfo"]')
       items = []
       for card in cards:
           item = CardItem()
           item['cardname'] = card.select('span[@class="cardTitle"]/a/text()').extract()
           item['convertedmana'] = card.select('span[@class="convertedManaCost"]/text()').extract()
           item['types'] = card.select('span[@class="typeLine"]/text()').extract()[0].strip()
           item['cardtext'] = card.select('div[@class="rulesText"]/p/text()').extract()
           #item['pt'] = card.select('span[@class="cardTitle"]/a/text()').extract()
           #item['expansion'] = card.select('span[@class="cardTitle"]/a/text()').extract()
           #item['rarity'] = card.select('span[@class="cardTitle"]/a/text()').extract()
           #item['allsets'] = card.select('span[@class="cardTitle"]/a/text()').extract()
           #item['cardnumber'] = card.select('span[@class="cardTitle"]/a/text()').extract()
           #item['artist'] = card.select('span[@class="cardTitle"]/a/text()').extract()
           #item['rating'] = card.select('span[@class="cardTitle"]/a/text()').extract()
           #item['link'] = card.select('span[@class="cardTitle"]/a/text()').extract()
           #item['uid'] = card.select('span[@class="cardTitle"]/a/text()').extract()
           items.append(item)
       for item in items:
            yield item