from scrapy.crawler import CrawlerProcess
from scrape import scrape_website , extract_body_content , clean_body_content,split_dom_content
# from myproject.spiders.example_spider import ExampleSpider
from spider import MetaScraper
from database import insert_into_db, get_data_from_db
from parse import parse_with_ollama

args = ["Mumbai","Nagpur"]


def start_crawler(args,limit=10):
    links = MetaScraper(keyword=f"flights {args[0]} to {args[1]}").crawl()
    return links
    for url in list(links)[:limit] : 
        dom_content = scrape_website(url)
        body_content, title = extract_body_content(dom_content)
        cleaned_content = clean_body_content(body_content)
        insert_into_db(cleaned_content)

    return links

def infer_sense():
    data = get_data_from_db('1 Day')
    for html in data:
        
        batches = split_dom_content(html[2])
        response = parse_with_ollama(batches)
        print(response)



if __name__ == '__main__':
    #start_crawler(args)
    infer_sense()