import itertools
import json
import re

import requests
import random
from crawler.words_magoosh import magoosh_1000_1, magoosh_1000_2, magoosh_1000_3
import hashlib
from pg_python import pg_python
from crawler.db import connect_db
import urllib.request
from inscriptis import get_text
from bs4.element import Comment
from datetime import datetime
import urllib3



import requests
from bs4 import BeautifulSoup

api_key_lst1 = ['d6b09fbb0c4d449f9d28a868090bd59a','31bbe9fc44634dd2a6a07f998d4ee52a','c74afd2d2a5b4515a912057f35c635b8']
api_key_lst2 = ['db41554ea8db48e9bd3ed7459ce41e8b', '10d8076dab5d4a78abe16f00effebd29']
api_key_lst = api_key_lst1 + api_key_lst2
api_token = 'your_api_token'
api_url_base = 'http://newsapi.org/v2/everything?q=%s&from=2020-07-22&sortBy=publishedAt&apiKey=%s'

from newsapi import NewsApiClient


round_robin = itertools.cycle(api_key_lst)


def get_web_text(url):

    print("getting web text for %s"%url)

    try:

        hdr = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}


        req = urllib.request.Request(url)
        req.add_header(            'User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
)


        html = urllib.request.urlopen(req).read().decode('utf-8')
        result = get_text(html)

        result = re.sub('\n', ' ', result)
        result = re.sub(' +', ' ', result)
        return result

    except Exception as e:
        print(e)
        return None


def get_web_text_v2(url):
    def tag_visible(element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

    def text_from_html(body):
        soup = BeautifulSoup(body, 'html.parser')
        texts = soup.findAll(text=True)
        visible_texts = filter(tag_visible, texts)
        return u" ".join(t.strip() for t in visible_texts)

    html = urllib.request.urlopen('http://www.nytimes.com/2009/12/21/us/21storm.html').read()
    return text_from_html(html)

def get_id(url):
    return hashlib.sha1(str.encode(url)).hexdigest()

def save_all_articles(all_articles):
    """
    save all articles
    :param all_articles:
    :return:
    """
    articles_lst = all_articles['articles']

    article_dict_lst = []

    for article in articles_lst:
        temp_dict = {}
        temp_dict.update(article)
        temp_dict.pop('source')
        temp_dict['source_id'] = article['source']['id']
        temp_dict['source_name'] = article['source']['name']

        temp_dict.pop('urlToImage')
        temp_dict['url_to_image'] = article['urlToImage']
        temp_dict['key'] = get_id(temp_dict['url'])
        temp_dict['publishedat'] = temp_dict.pop('publishedAt')


        web_text = get_web_text(temp_dict['url'])
        if web_text is None:
            continue
        temp_dict['web_text'] = web_text
        article_dict_lst.append(temp_dict)


    if len(article_dict_lst) == 0:
        return
    pg_python.insert_multiple('article',['key','source_id','source_name','url_to_image',
                                            'author','title','description','url','publishedat','content','web_text'],

                              article_dict_lst)





def crawl_words():


    print("crawling words")
    for word in magoosh_1000_1:
        print("crawling for %s" %word)

        newsapi = NewsApiClient(random.choice(api_key_lst))

        all_articles = newsapi.get_everything(q=word,

                                              from_param=datetime.today().date().strftime("%Y-%m-%d"),

                                              language='en',
                                              sort_by='relevancy',
                                              page=1,
                                              page_size=100)

        if all_articles['totalResults'] == 0:
            continue

        save_all_articles(all_articles)

        # num_res = all_articles['totalResults']
        #
        # pages_to_crawl = int(num_res/100)
        # if pages_to_crawl > 10:
        #     pages_to_crawl = 10
        #
        # for counter in range(1,pages_to_crawl+1):
        #     if counter == 1:
        #         continue
        #     all_articles = newsapi.get_everything(q='aberrant',
        #
        #                                           from_param='2020-07-22',
        #
        #                                           language='en',
        #                                           sort_by='relevancy',
        #                                           page=counter,
        #                                           page_size=100)
        #
        #     save_all_articles(all_articles)






if __name__ == '__main__':
    connect_db()
    crawl_words()