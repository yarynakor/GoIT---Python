import json
import scrapy
from scrapy.http import HtmlResponse


class QuoteItem(scrapy.Item):
    quote = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com',
    ]

    custom_settings = {
        'FEED_URI': 'quotes.json',
        'FEED_FORMAT': 'json',
    }

    def parse(self, response: HtmlResponse):
        quotes = response.css('div.quote')
        for quote in quotes:
            yield QuoteItem(
                quote=quote.css('span.text::text').get(),
                author=quote.css('span small::text').get(),
                tags=[tag.strip() for tag in quote.css('div.tags a.tag::text').getall()],
            )

        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)


class AuthorSpider(scrapy.Spider):
    name = "authors"
    start_urls = [
        'http://quotes.toscrape.com/page',
    ]

    custom_settings = {
        'FEED_URI': 'authors.json',
        'FEED_FORMAT': 'json',
    }

    def parse(self, response: HtmlResponse):
        author_links = response.css('div.quote span a::attr(href)').getall()
        for author_link in author_links:
            yield response.follow(author_link, self.parse_author)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_author(self, response: HtmlResponse):
        author = response.css('h3.author-title::text').get().strip()
        birthday = response.css('span.author-born-date::text').get().strip()
        location = response.css('span.author-born-location::text').get().strip()
        description = response.css('div.author-description::text').get().strip()
        yield {
            'author': author,
            'birthday': birthday,
            'location': location,
            'description': description,
        }
