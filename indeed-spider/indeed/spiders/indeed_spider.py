from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.spider import BaseSpider
from scrapy.http import Request
import time
import sys
from indeed.items import IndeedItem
import lxml




class IndeedSpider(CrawlSpider):
  name = "indeed"
  allowed_domains = ["indeed.com"]
  pages = 4
  url_template = "http://www.indeed.com/jobs?q=%s&l=Chicago&start=%s"
  start_urls = []

  rules = (


        Rule(SgmlLinkExtractor(restrict_xpaths=("//div[@class='row ' or @class='row lastRow']/h2/a/@href"))),
      Rule(SgmlLinkExtractor(allow=('http://www.indeed.com/jobs',),deny=('/my/mysearches', '/preferences', '/advanced_search','/my/myjobs')), callback='parse_item', follow=False),

      )

  #Initialize the start_urls
  job_queries = []
  with open('job_queries.cfg', 'r') as f:
    for line in f:
      job_queries.append(line.strip())


  # Build out the start_urls to scrape
  for job_query in job_queries:
    for page in range(1,pages):
      full_url = url_template % (job_query, str(page*10))
      start_urls.append(full_url)


  '''
  def __init__(self, *args, **kwargs):
    # Get the search queries for the jobs from the job_queries.cfg file
    # Config file must have 1 query per line

    super(IndeedSpider, self).__init__(*args, **kwargs)

  '''

  def get_job_description(self, html, summary_string):

    root = lxml.html.document_fromstring(html)
    target_element = None


    # For some reason the summary will not match the lxml extracted text, figure out why
    # This solution is hacky


    # Get only the first sentence
    # Indeed cobbles together multiple sentences from the job posting
    summary_string = summary_string.split(".",1)[0]

    summary_start_list = summary_string.split(" ")[:3]
    summary_start = " ".join(summary_start_list)



    counter  = 0
    # Find the element that contains the initial words in the summary string
    for element in root.iter():
      counter += 1
      if element.text:
        if (summary_start in element.text):
          target_element = element
          print 'YES. element.txt'
          break
      elif element.tail:
        if (summary_start in element.tail):
          target_element = element
          print 'YES element.tail'
          break



    generation_count = 0

    target_ancestor = None

    job_posting_min_length = 500


    # Find the best parent element that contains the entire job description without the extra html
    if target_element is not None:
      for ancestor in target_element.iterancestors():
        generation_count += 1

        ancestor_text = ancestor.text_content()

        target_ancestor = ancestor

        # The loop will pre-maturely break once the ancestor elements has minimum threshold of characters
        if len(ancestor_text) > job_posting_min_length:
          break


    return target_ancestor.text_content()

  def parse_next_site(self, response):



    item = response.request.meta['item']
    item['source_url'] = response.url
    item['crawl_timestamp'] =  time.strftime('%Y-%m-%d %H:%M:%S')



    summary = item['summary'][0][1:-5]
    job_description = self.get_job_description(response.body, summary)
    item['full_description'] = job_description



    pass
    return item


  def parse_item(self, response):
    '''
    import pdb
    pdb.set_trace()
    '''


    self.log('\n Crawling  %s\n' % response.url)
    hxs = HtmlXPathSelector(response)
    sites = hxs.select("//div[@class='row ' or @class='row lastRow']")
    #sites = hxs.select("//div[@class='row ']")
    items = []

    #Skip top two sponsored ads
    for site in sites[:-2]:
      item = IndeedItem(company='none')

      item['job_title'] = site.select('h2/a/@title').extract()
      link_url= site.select('h2/a/@href').extract()
      item['link_url'] = link_url
      item['crawl_url'] = response.url
      item['location'] = site.select("span[@itemprop='jobLocation']/span[@class='location']/span[@itemprop='addressLocality']/text()").extract()
      # Not all entries have a company
      company_name = site.select("span[@class='company']/span[@itemprop='name']/text()").extract()
      if company_name == []:
        item['company'] = [u'']
      else:
        item['company'] = company_name

      item['summary'] =site.select("table/tr/td/div/span[@class='summary']/text()").extract()
      #item['source'] = site.select("table/tr/td/span[@class='source']/text()").extract()
      item['found_date'] =site.select("table/tr/td/span[@class='date']/text()").extract()
      #item['source_url'] = self.get_source(link_url)


      if len(item['link_url']):
        request = Request("http://www.indeed.com" + item['link_url'][0], callback=self.parse_next_site)
        request.meta['item'] = item

        yield request


    return



SPIDER=IndeedSpider()
