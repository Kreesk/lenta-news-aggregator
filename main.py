import asyncio
import aiohttp

import logging
import uvicorn

from asgiref.wsgi import WsgiToAsgi
from flask import Flask, render_template
from flask_restful import Api
from bs4 import BeautifulSoup

app = Flask(__name__)
asgi_app = WsgiToAsgi(app)
api = Api(app)
logger = logging.getLogger(__name__)

url_lenta = "https://lenta.ru/parts/news/"
async def fetch_news(news_url: str) -> list[dict[str, str]]:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(news_url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    html_code = await response.text()
                    soup = BeautifulSoup(html_code, 'html.parser')
                    cards_news = soup.find_all('a', class_ = "card-full-news")
                    if cards_news:
                        return await parser_news(cards_news=cards_news)
                    else:
                        logger.warning("Нет новостей на странице")
                        return []
                else:
                    logger.error(f"Код ошибки {response.status}")


        except Exception as e:
            logger.error(f"Произошла ошибка при подключении к сайту. Ошибка - {e}.")

async def parser_news(cards_news: list) -> list[dict[str, str]]:
    news_items = []
    if cards_news:
        for card in cards_news:
            try:
                news_items.append({"title": card.find("h3").text,
                                   "url": "https://lenta.ru" + card.get("href"),
                                   "time": card.find("time").text}
                                  )
            except Exception as e:
                logger.error(f"Ошибка при парсинге карточек новостей: {str(e)}")
                pass
        return news_items

    return []


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/news')
def news():
    try:
        news_data = asyncio.run(fetch_news(url_lenta))
    except Exception as e:
        logger.error(f"Ошибка при получении новостей: {str(e)}")
        news_data = []
    return render_template('news.html', news=news_data)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/login')
def login():
    return render_template('login.html')


async def main():
    logging.basicConfig(filename='./logs/logs.txt', level=logging.INFO)
    logger.info('Started')
    await asyncio.gather(fetch_news(url_lenta))
    logger.info('Finished')

if __name__ == '__main__':
    uvicorn.run(asgi_app, host="127.0.0.1", port=3000)

