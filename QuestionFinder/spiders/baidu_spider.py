from QuestionFinder.items import *
import QuestionFinder.spiders.utils


class baidu_spider(scrapy.Spider):
    name = "baidu"
    target_urls = "http://www.baidu.com"
    MAX_DEPTH = 3
    depth_count = 0

    def __init__(self, name=None, **kwargs):
        super(baidu_spider, self).__init__(name, **kwargs)
        self.start_urls = [QuestionFinder.spiders.utils.completeUrl(self.target_urls, kwargs.get('question_url'))]

    def parse(self, response):
        for res in response.xpath('//div[@id="content_left"]/div[@class="result c-container "]'):
            baidu = candidateItem()
            baidu['href'] = res.xpath('h3/a/@href').extract()
            baidu['content'] = (res.xpath('div')).xpath('string(.)').extract()[0].strip()
            baidu['title'] = (res.xpath('h3/a')).xpath('string(.)').extract()[0].strip()
            yield baidu

        next_page = response.xpath('//div[@id="page"]/a')[-1].xpath('@href').extract()[0]
        next_url = QuestionFinder.spiders.utils.completeUrl(self.target_urls, next_page)

        if self.depth_count < self.MAX_DEPTH:
            self.depth_count += 1
            yield scrapy.Request(next_url, callback=self.parse)
