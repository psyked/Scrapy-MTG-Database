from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request

from mtg.items import CardItem

def striplist(l):
	return([x.strip() for x in l])

class CardSpider(BaseSpider):
	name = "cards"
	allowed_domains = ["gatherer.wizards.com"]
	start_urls = [
		"http://gatherer.wizards.com/Pages/Search/Default.aspx?action=advanced&set=+[%22Magic%202013%22]"
		#"http://gatherer.wizards.com/Pages/Search/Default.aspx?text=+[]"
	]

	def getCardDetails(self, response):
		hxs = HtmlXPathSelector(response)

		item = response.request.meta['item']
		item['cardname'] = striplist(hxs.select('//span[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContentHeader_subtitleDisplay"]/text()').extract())
		item['convertedmana'] = striplist(hxs.select('//div[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_cmcRow"]/div[@class="value"]/text()').extract())
		item['types'] = striplist(hxs.select('//div[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_typeRow"]/div[@class="value"]/text()').extract())
		item['cardtext'] = striplist(hxs.select('//div[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_textRow"]/div[@class="value"]//*/text()').extract())
		item['flavortext'] = striplist(hxs.select('//div[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_flavorRow"]/div[@class="value"]//*/text()').extract())
		item['pt'] = striplist(hxs.select('//div[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ptRow"]/div[@class="value"]/text()').extract())
		item['expansion'] = striplist(hxs.select('//div[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_currentSetSymbol"]/div[@class="value"]/text()').extract())
		item['rarity'] = striplist(hxs.select('//div[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rarityRow"]/div[@class="value"]/text()').extract())
		item['allsets'] = striplist(hxs.select('//div[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_otherSetsRow"]/div[@class="value"]/text()').extract())
		item['cardnumber'] = striplist(hxs.select('//div[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_numberRow"]/div[@class="value"]/text()').extract())
		item['artist'] = striplist(hxs.select('//div[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_artistRow"]/div[@class="value"]/text()').extract())
		item['rating'] = striplist(hxs.select('//div[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_playerRatingRow"]/div[@class="value"]/text()').extract())
		item['image'] = "http://gatherer.wizards.com/Pages/Card/" + hxs.select('//img[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_cardImage"]/@src').extract()[0]
		item['image_urls'] = ["http://gatherer.wizards.com/Pages/Card/" + hxs.select('//img[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_cardImage"]/@src').extract()[0]]
		#item['uid'] = hxs.select('//div[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_textRow"]/div[@class="value"]/text()').extract()[0].strip()
		yield item

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
			item['link'] = "http://gatherer.wizards.com/Pages/Search/" + card.select('span[@class="cardTitle"]/a/@href').extract()[0]
			items.append(item)
			yield Request(item['link'], meta={'item':item}, callback=self.getCardDetails)