from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request

from mtg.items import CardItem

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
		#item = CardItem()
		item['cardname'] = hxs.select('//span[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContentHeader_subtitleDisplay"]/text()').extract()
		item['convertedmana'] = hxs.select('//div[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_cmcRow"]/div[@class="value"]/text()').extract()
		item['types'] = hxs.select('//div[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_typeRow"]/div[@class="value"]/text()').extract()
		item['cardtext'] = hxs.select('//div[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_textRow"]/div[@class="value"]/text()').extract()
		item['flavortext'] = hxs.select('//div[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_flavorRow"]/div[@class="value"]/text()').extract()
		item['pt'] = hxs.select('//div[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ptRow"]/div[@class="value"]/text()').extract()
		item['expansion'] = hxs.select('//div[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_currentSetSymbol"]/div[@class="value"]/text()').extract()
		item['rarity'] = hxs.select('//div[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rarityRow"]/div[@class="value"]/text()').extract()
		item['allsets'] = hxs.select('//div[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_otherSetsRow"]/div[@class="value"]/text()').extract()
		item['cardnumber'] = hxs.select('//div[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_numberRow"]/div[@class="value"]/text()').extract()
		item['artist'] = hxs.select('//div[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_artistRow"]/div[@class="value"]/text()').extract()
		item['rating'] = hxs.select('//div[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_playerRatingRow"]/div[@class="value"]/text()').extract()
		item['image'] = hxs.select('//div[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_cardImage"]/@href')
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
			#result = Request("http://gatherer.wizards.com/" + card.select('span[@class="cardTitle"]/a/@href').extract()[0], self.getCardDetails)
			#items.append(result) 
			item = CardItem()
			#item['cardname'] = card.select('span[@class="cardTitle"]/a/text()').extract()
			#item['convertedmana'] = card.select('span[@class="convertedManaCost"]/text()').extract()
			#item['types'] = card.select('span[@class="typeLine"]/text()').extract()[0].strip()
			#item['cardtext'] = card.select('div[@class="rulesText"]/p/text()').extract()
			#item['pt'] = card.select('span[@class="cardTitle"]/a/text()').extract()
			#item['expansion'] = card.select('span[@class="cardTitle"]/a/text()').extract()
			#item['rarity'] = card.select('span[@class="cardTitle"]/a/text()').extract()
			#item['allsets'] = card.select('span[@class="cardTitle"]/a/text()').extract()
			#item['cardnumber'] = card.select('span[@class="cardTitle"]/a/text()').extract()
			#item['artist'] = card.select('span[@class="cardTitle"]/a/text()').extract()
			#item['rating'] = card.select('span[@class="cardTitle"]/a/text()').extract()
			item['link'] = "http://gatherer.wizards.com/Pages/Search/" + card.select('span[@class="cardTitle"]/a/@href').extract()[0]
			#item['uid'] = card.select('span[@class="cardTitle"]/a/text()').extract()
			items.append(item)
			yield Request(item['link'], meta={'item':item}, callback=self.getCardDetails)

		for item in items:
			yield item