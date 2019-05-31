from bs4 import BeautifulSoup
import scrapy
from ..items import LiquorItem

class RecipesCrawlerSpider(scrapy.Spider):
    name = 'recipes_crawler'
    allowed_domains = ['liquor.com']
    start_urls = ['http://liquor.com/']

    def start_requests(self):
        for i in range(1, 45):
            url="https://www.liquor.com/recipes/page/{0}".format(i)
            # The meta is used to send our search text into the parser as metadata
            yield scrapy.Request(url, callback = self.parse, meta = {"i": i})


    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')

        cocktails = soup.find("div", class_="container-grid")

        for cocktail in cocktails:
            # name = cocktail.find("h3", class_="archive-item-headline sans").find("a").get_text()
            link = cocktail.find("h3", class_="archive-item-headline sans").find("a").get("href")
            # image = 'http://' + cocktail.find("div", class_="item image").get("data-href")[2:]
            
            yield response.follow(link, self.parse_cocktails)

            # yield {
            #     'name': name,
            #     'link': link,
            #     'image': image,
            # }

    def parse_cocktails(self, response):
        soup = BeautifulSoup(response.text, 'lxml')

        name = soup.find("div", class_="row head-row text-center").find("h1").get_text()
        link = response.request.url
        image = 'http://' + soup.find("div", class_="center-block img-hero heart-me").find("img").get("src")[2:]

        try:
            introduce = soup.find(itemprop="description").get_text()
        except AttributeError:
            introduce = "No Information Available." 

        try:
            material = []
            units = [units.get_text().replace('\t', '').replace('\n', '').replace('\xa0', ' ') for units in soup.find_all("div", class_="parts-value")]
            ingredient = [ingredient.get_text().replace('\t', '').replace('\n', '')   for ingredient in soup.find_all("div", class_="col-xs-9 x-recipe-ingredient")]
            while True: 
                try: 
                    combine = units.pop(0) + ': ' + ingredient.pop(0) 
                    material.append(combine) 
                except IndexError: 
                    break 
        except AttributeError:
            material = "None"

        try:
            steps = [step.get_text() for step in soup.find(itemprop="recipeInstructions").find_all("p")]
        except AttributeError:
            steps = "No Information Available."

        try:
            basespirit = soup.find("div", class_="col-xs-7 x-recipe-spirit").get_text()
        except AttributeError:
            basespirit = "None"

        liquorItem = LiquorItem(name = name, link=link, image=image, introduce=introduce, material=material, steps=steps, basespirit=basespirit)
        
        yield liquorItem