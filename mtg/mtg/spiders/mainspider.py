from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request

from mtg.items import CardItem

import re

def striplist(l):
	return([x.strip() for x in l])

class CardSpider(BaseSpider):
	name = "cards"
	allowed_domains = [
		"gatherer.wizards.com",
		"www.manaleak.com"
	]
	start_urls = [
		"http://gatherer.wizards.com/Pages/Search/Default.aspx?action=advanced&set=+[%22Magic%202013%22]"
		# "http://gatherer.wizards.com/Pages/Search/Default.aspx?text=+[]"
	]

	def getPricesFor(self, response):
		hxs = HtmlXPathSelector(response)

		item = response.request.meta['item']
		item['prices'] = striplist(hxs.select('//table[@class="productListing"]//tr/td[4][@class="productListing-data"]/text()').extract())

		yield item

	def getCardDetails(self, response):
		hxs = HtmlXPathSelector(response)

		item = response.request.meta['item']
		item['cardname'] = striplist(hxs.select('//span[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContentHeader_subtitleDisplay"]/text()').extract())[0]
		item['manacost'] = striplist(hxs.select('//div[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_manaRow"]//img/@alt').extract())
		item['convertedmana'] = striplist(hxs.select('//div[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_cmcRow"]/div[@class="value"]/text()').extract())
		item['types'] = striplist(hxs.select('//div[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_typeRow"]/div[@class="value"]/text()').extract())[0]
		item['cardtext'] = striplist(hxs.select('//div[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_textRow"]/div[@class="value"]//*/text()').extract())
		item['flavortext'] = striplist(hxs.select('//div[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_flavorRow"]/div[@class="value"]//*/text()').extract())

		if len(hxs.select('//div[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ptRow"]/div[@class="value"]/text()')) > 0:
			item['pt'] = striplist(hxs.select('//div[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ptRow"]/div[@class="value"]/text()').extract())

		item['expansion'] = striplist(hxs.select('//div[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_currentSetSymbol"]//img/@alt').extract())[0]
		item['rarity'] = striplist(hxs.select('//div[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rarityRow"]/div[@class="value"]//*/text()').extract())[0]
		item['allsets'] = hxs.select('//div[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_otherSetsRow"]/div[@class="value"]//img/@alt').extract()
		item['cardnumber'] = striplist(hxs.select('//div[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_numberRow"]/div[@class="value"]/text()').extract())[0]
		item['artist'] = striplist(hxs.select('//div[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_artistRow"]/div[@class="value"]//*/text()').extract())[0]
		item['rating'] = striplist(hxs.select('//div[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_playerRatingRow"]//span[@class="textRatingValue"]/text()').extract())[0]

		# ../../Handlers/Image.ashx?multiverseid=214673&type=card
		#item['image_urls'] = ["http://gatherer.wizards.com/Pages/Card/" + hxs.select('//img[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_cardImage"]/@src').extract()[0]]
		item['image_urls'] = []

		alternatelinks = hxs.select('//div[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_otherSetsRow"]/div[@class="value"]//a/@href').extract()
		for varients in alternatelinks:
			# extract the unique card ID for this card, using regular expressions.
			#ytburl = card.select('span[@class="cardTitle"]/a/@href').extract()[0] #"../Card/Details.aspx?multiverseid=265718"
			regexp = "(?<=multiverseid=)(\\w*)"

			#It's a good idea to compile it if you're gonna use it more than once.
			regexp = re.compile(regexp, re.IGNORECASE)
			result = regexp.search(varients)

			if (result):
				item['image_urls'].append("http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=" + result.group() + "&type=card")

		if len(hxs.select('//div[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ptRow"]/div[@class="value"]/text()')) > 0:
			item['pt'] = striplist(hxs.select('//div[@id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ptRow"]/div[@class="value"]/text()').extract())

		priceURL = "http://www.manaleak.com/store/advanced_search_result.php?keywords=" + item['cardname'] + "&exact_title=1&categories_id=21"
		yield Request(priceURL, meta={'item':item}, callback=self.getPricesFor)

	def parse(self, response):
		hxs = HtmlXPathSelector(response)

		next_page = hxs.select("//div[@class='pagingControls']/a[contains(text(),'>')]/@href").extract()
		if not not next_page:
			yield Request("http://gatherer.wizards.com" + next_page[0], self.parse) 

		cards = hxs.select('//div[@class="cardInfo"]')
		items = []

		for card in cards:
			item = CardItem()
			item['cardname'] = card.select('span[@class="cardTitle"]/a/text()').extract()[0]
			item['link'] = "http://gatherer.wizards.com/Pages/Search/" + card.select('span[@class="cardTitle"]/a/@href').extract()[0]

			# extract the unique card ID for this card, using regular expressions.
			ytburl = card.select('span[@class="cardTitle"]/a/@href').extract()[0] #"../Card/Details.aspx?multiverseid=265718"
			regexp = "(?<=multiverseid=)(\\w*)" 

			#It's a good idea to compile it if you're gonna use it more than once.
			regexp = re.compile(regexp, re.IGNORECASE)
			result = regexp.search(ytburl)

			if (result):
				item['uid'] = result.group()
			
			items.append(item)
			
			yield Request(item['link'], meta={'item':item}, callback=self.getCardDetails)