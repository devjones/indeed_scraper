#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'Job_Hunter'
BOT_VERSION = '0.1'

SPIDER_MODULES = ['indeed.spiders']
NEWSPIDER_MODULE = 'indeed.spiders'
DEFAULT_ITEM_CLASS = 'indeed.items.IndeedItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
DOWNLOAD_DELAY = 1.0
'''
ITEM_PIPELINES = [
	'indeed.pipelines.IndeedPipeline',
	'indeed.pipelines.MysqlInsert',
	]
'''

DOWNLOADER_MIDDLEWARES = {
'scrapy.contrib.downloadermiddleware.redirect.RedirectMiddleware' : 543,
}

MYSQL = {'user':'',
	'host' :'',
	'passwd':'',
	'dbname':''}

