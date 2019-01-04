import scrapy
import QuestionFinder.spiders.utils
import QuestionFinder.spiders.page_spiders.zhidao_spider


class dispatch_spider(scrapy.Spider):
    name = "dispatcher"

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.start_urls = [kwargs.get('question_url')]

    def parse(self, response):
        parse = QuestionFinder.spiders.utils.dispatch(response.url)
        if parse is not None:
            yield scrapy.Request(self.start_urls[0], parse)
