import json
import re

import requests
import random
from crawler.words_magoosh import magoosh_1000
import hashlib
from pg_python import pg_python
from crawler.db import connect_db
import urllib.request
from inscriptis import get_text
from bs4.element import Comment



import requests
from bs4 import BeautifulSoup

api_key_lst = ['d6b09fbb0c4d449f9d28a868090bd59a','31bbe9fc44634dd2a6a07f998d4ee52a','c74afd2d2a5b4515a912057f35c635b8']
api_token = 'your_api_token'
api_url_base = 'http://newsapi.org/v2/everything?q=%s&from=2020-07-22&sortBy=publishedAt&apiKey=%s'

from newsapi import NewsApiClient

newsapi = NewsApiClient(api_key=random.choice(api_key_lst))


def get_web_text(url):

    print("getting web text for %s"%url)

    try:

        html = urllib.request.urlopen(url).read().decode('utf-8')
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

    pg_python.insert_multiple('article',['key','source_id','source_name','url_to_image',
                                            'author','title','description','url','publishedat','content','web_text'],

                              article_dict_lst)





def crawl_words():


    print("crawling words")
    for word in magoosh_1000:
        print("crawling for %s" %word)

        all_articles = newsapi.get_everything(q=word,

                                              from_param='2020-07-22',

                                              language='en',
                                              sort_by='relevancy',
                                              page=1,
                                              page_size=100)

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