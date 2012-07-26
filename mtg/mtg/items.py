# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class CardItem(Item):
    cardname = Field()
    convertedmana = Field()
    types = Field()
    cardtext = Field()
    pt = Field()
    expansion = Field()
    rarity = Field()
    allsets = Field()
    cardnumber = Field()
    artist = Field()
    rating = Field()
    link = Field()
    uid = Field()