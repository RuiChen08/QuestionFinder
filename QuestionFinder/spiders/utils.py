import QuestionFinder.spiders.page_spiders.zhidao_spider

def completeUrl(tar, ques):
    if ques.startswith("/s?wd="):
        return tar + ques
    else:
        return tar + "/s?wd=" + ques


def dispatch(url):
    if url.startswith("https://zhidao.baidu.com/"):
        return QuestionFinder.spiders.page_spiders.zhidao_spider.zhidao.parse
    else:
        return None