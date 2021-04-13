import scrapy

from ..items import PostItem


class PythonBlogSpider(scrapy.Spider):
    name = 'python_blog'
    allowed_domains = ['fullstackpython.com']
    start_urls = ['https://www.fullstackpython.com/blog.html']

    def parse(self, response):
        item_links = response.xpath('//div[@class="c9"]//h2//a/@href').extract()
        for item in item_links:
            detail_page = response.urljoin(item)
            yield response.follow(detail_page, callback=self.parse_detail)

    def parse_detail(self, response):
        item = PostItem()
        item['title'] = response.xpath('//h1//text()').get()
        item['body'] = response.xpath('//div[@class="row"]//div[@class="c9"]').get()
        yield item
