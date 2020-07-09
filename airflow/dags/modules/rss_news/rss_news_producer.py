
import re
from dataclasses import dataclass, asdict
import atoma
from dateutil import parser
from rss_news.rss_news_exporter import NewsExporter
from parser import WebParser


@dataclass(frozen=True)
class News:

    title: str
    link: str
    published: str
    news_id: str
    
    def as_dict(self):
        return self.__dict__


class NewsProducer:
    def __init__(self, rss_feed):
        self.parser = WebParser(rss_feed)

    def _extract_rss_feed(self, proxies):
        content = self.parser.get_content(proxies=proxies)
        return atoma.parse_rss_bytes(content)

    def get_news_stream(self, proxies):
        rss_feed = self._extract_rss_feed(proxies) 
        for entry in rss_feed.items:
            news_id = self.construct_id(entry.title)
            published_date = self.unify_date(entry.pub_date)
            yield News(
                entry.title,
                entry.link,
                published_date,
                news_id
            )

    @staticmethod
    def construct_id(title):
        return (
            re.sub("[^0-9a-zA-Z_-]+", "", title).lower()
        )

    @staticmethod
    def unify_date(date):
        return date.strftime("%Y-%m-%d %H:%M:%S")