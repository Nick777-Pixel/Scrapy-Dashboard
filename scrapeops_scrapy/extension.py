from scrapy import signals

from scrapeops_scrapy.controller.engine import ScrapeopsCore 
from scrapeops_scrapy.signals import scrapeops_signals


class ScrapeOpsMonitor(ScrapeopsCore):

    def __init__(self, crawler):
        ScrapeopsCore.__init__(self)
        self.crawler = crawler

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls(crawler)

        # connect the extension object to signals
        crawler.signals.connect(ext.spider_opened,
                                signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed,
                                signal=signals.spider_closed)

        crawler.signals.connect(ext.log_request,
                                signal=signals.request_reached_downloader)

        crawler.signals.connect(ext.log_response,
                                signal=signals.response_received)
        
        crawler.signals.connect(ext.item_scraped, 
                                signal=signals.item_scraped)

        crawler.signals.connect(ext.log_response_middleware, 
                                signal=scrapeops_signals.scrapeops_response_recieved)

        crawler.signals.connect(ext.log_exception, 
                                signal=scrapeops_signals.scrapeops_exception_recieved)

        crawler.signals.connect(ext.response_rejected, 
                                signal=scrapeops_signals.scrapeops_response_rejected)

        # return the extension object
        return ext

    def spider_opened(self, spider):
        self.start_sdk(spider=spider, crawler=self.crawler)

    def spider_closed(self, spider, reason):
        self.close_sdk(spider=spider, reason=reason)

    def log_request(self, request, spider):
        self.request_stats(request=request)

    def log_response(self, response, request, spider):
        if self.scrapeops_middleware_enabled() == False:
            self.response_stats(request=request, response=response)

    def log_response_middleware(self, request=None, response=None, spider=None):
        if self.scrapeops_middleware_enabled():
            self.response_stats(request=request, response=response)

    def log_exception(self, request=None, spider=None, exception_class=None):
        if self.scrapeops_middleware_enabled():
            self.exception_stats(request=request, exception_class=exception_class)
        
    def item_scraped(self, item, response, spider): 
        self.item_stats(signal_type='item_scraped', item=item, response=response, spider=spider) 

    def item_dropped(self, item, response, spider): 
        self.item_stats(signal_type='item_dropped', item=item, response=response, spider=spider) 
    
    def item_error(self, item, response, spider): 
        self.item_stats(signal_type='item_error', item=item, response=response, spider=spider) 

    def response_rejected(self, spider=None, response=None, reason=None): 
        pass
