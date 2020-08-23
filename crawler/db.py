
import psycopg2

from pg_python.pg_python import *


def connect_db():
    pgs = pg_server("crawler_db", "postgres", "Layer0_123", "localhost", server='default', application_name='pg_python')





if __name__ == '__main__':
    connect_db()
    data_map = { 'author': 'Reuters Editorial', 'title': 'France to ban cafe terrace heaters as no longer cool - Reuters', 'description': 'France plans to ban heaters used by restaurants and cafes on outdoor terraces from early next year, as it accelerates a shift to a low carbon economy, Ecology Minister Barbara Pompili said on Monday.', 'url': 'https://www.reuters.com/article/us-climate-change-france-idUSKCN24S1HA', 'url_to_image': 'https://s4.reutersmedia.net/resources/r/?m=02&d=20200727&t=2&i=1527261836&w=1200&r=LYNXNPEG6Q0VT', 'publishedAt': '2020-07-27T12:27:00Z', 'content': 'PARIS (Reuters) - France plans to ban heaters used by restaurants and cafes on outdoor terraces from early next year, as it accelerates a shift to a low carbon economy, Ecology Minister Barbara Pompi… [+1101 chars]'}
    write("article",data_map)
