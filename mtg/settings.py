# Scrapy settings for mtg project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
#
#BOT_NAME = 'mtg'
#BOT_VERSION = '1.0'

SPIDER_MODULES = ['mtg.spiders']
NEWSPIDER_MODULE = 'mtg.spiders'
#USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
ITEM_PIPELINES = ['scrapy.contrib.pipeline.images.ImagesPipeline']
IMAGES_STORE = 'output/images'