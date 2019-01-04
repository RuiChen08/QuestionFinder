import scrapy
from QuestionFinder.items import q_and_a_Item


class zhidao():

    def parse(response):
        qaa = q_and_a_Item()

        answer = response.xpath('//div[@class="line content"]/div').xpath('string(.)').extract()[0].strip()
        if answer.startswith("展开全部"):
            answer = answer[4:].strip()
        qaa['answer'] = answer

        p_des = response.xpath('//div[@class="wgt-ask accuse-response line "]/div/span/text()').extract()
        if len(p_des) != 0:
            qaa['description'] = p_des[0]
        else:
            qaa['description'] = "No description"

        qaa['question'] = response.xpath('//div[@class="wgt-ask accuse-response line "]/h1/span/text()').extract()[0].strip()
        yield qaa
