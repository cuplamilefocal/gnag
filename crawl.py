import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from os import path

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)

class Crawler:

    def __init__(self, urls=[]):
        self.visited_urls = []
        self.urls_to_visit = urls

    def download_url(self, url):
        fname = url.split('/')[-1]
        if path.exists(fname):
            with open(fname, 'r') as f:
                return f.read()
        import time
        time.sleep(22)
        ret = requests.get(url).text
        with open(fname, 'w') as f:
            f.write(ret)
        return ret

    def get_linked_urls(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            path = link.get('href')
            if not path:
                continue
            if not path.startswith('https://'):
                path = urljoin(url, path)
                path = path.replace('http:/nualeargais', 'http://nualeargais')
            yield path.split('#')[0]

    def add_url_to_visit(self, url):
        if url and url not in self.visited_urls and url not in self.urls_to_visit:
            if '/http://nualeargais.ie/' in url:
                self.urls_to_visit.append(url)

    def crawl(self, url):
        html = self.download_url(url)
        for url in self.get_linked_urls(url, html):
            self.add_url_to_visit(url)

    def run(self):
        while self.urls_to_visit:
            url = self.urls_to_visit.pop(0)
            logging.info(f'Crawling: {url}')
            try:
                self.crawl(url)
            except Exception:
                logging.exception(f'Failed to crawl: {url}')
            finally:
                self.visited_urls.append(url)

if __name__ == '__main__':
    Crawler(urls=['https://web.archive.org/web/20230304221524if_/http://nualeargais.ie/gnag/gram.htm']).run()
