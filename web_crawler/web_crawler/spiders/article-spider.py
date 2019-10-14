import scrapy


class QuotesSpider(scrapy.Spider):
    name = "articles"
    start_urls = [
        'https://pubsonline.informs.org/journal/deca'
    ]

    def parse(self, response):
        for link_to_article in response.css('li.issue-item a'):
            yield response.follow(link_to_article, callback=self.parse_abstract)

        # follow pagination links
        for href in response.css('li.next a::attr(href)'):
            yield response.follow(href, self.parse)

    def parse_abstract(self, response):
        def extract_with_css(query):
            return response.css(query).get()

        extracted_title = extract_with_css('h1.citation__title::text')
        extracted_abstract = extract_with_css('div.abstractSection p::text')
        extracted_date = extract_with_css('span.epub-section__date::text')

        if extracted_title != None and extracted_abstract != None:
            yield {
                'title': extracted_title,
                'abstract': extracted_abstract,
                'published': extracted_date
            }

        # print(response.url.split("/")[-2]+ "------------")
        # if response.url.split("/")[-3] == 'doi':
        #     article_name = response.css('h1.citation__title::text').get()
        #     article_doi = response.url.split("/")[-3]
        #
        #     print(article_name)
        #     print(article_doi)

        # next_page = response.css('li.issue-item a::attr(href)').get()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #
        #     print("ichdrücke hier mal was." + response.url)
        #
        #     if 'doi' in response.url:
        #         article_name = response.css('h1.citation_title').get()
        #         article_doi = response.url.split("/")[-2]
        #
        #         print(article_name)
        #         print(article_doi)
        #         print('---------------------------------')
        #
        #     # filename = 'export/abstract-%s.html' % article_name
        #     # with open(filename, 'wb') as f:
        #     #     f.write(response.body)
        #     # self.log('Saved file %s' % filename)
        #
        #     yield scrapy.Request(next_page, callback=self.parse)
