import asyncio
import time
from typing import List
import aiohttp
from bs4 import BeautifulSoup
from db import init_db, save_quote, clear_quotes, count_quotes

URLS = [
    "https://quotes.toscrape.com/",
    "https://quotes.toscrape.com/page/2/",
    "https://quotes.toscrape.com/page/3/",
    "https://quotes.toscrape.com/page/4/",
    "https://quotes.toscrape.com/page/3/",
    "https://quotes.toscrape.com/page/3/",
    "https://quotes.toscrape.com/page/3/",
    "https://quotes.toscrape.com/page/3/",
    "https://quotes.toscrape.com/page/3/",
    "https://quotes.toscrape.com/page/3/",
    "https://quotes.toscrape.com/page/3/",
    "https://quotes.toscrape.com/page/3/",
    "https://quotes.toscrape.com/page/3/",
    "https://quotes.toscrape.com/page/3/",
    "https://quotes.toscrape.com/page/3/",
    "https://quotes.toscrape.com/page/3/",
    "https://quotes.toscrape.com/page/3/",
    "https://quotes.toscrape.com/page/3/",
    "https://quotes.toscrape.com/page/3/",
    "https://quotes.toscrape.com/page/3/",
    "https://quotes.toscrape.com/page/3/",
    "https://quotes.toscrape.com/page/3/",
    "https://quotes.toscrape.com/page/3/",
    "https://quotes.toscrape.com/page/3/",
    "https://quotes.toscrape.com/page/3/",
    "https://quotes.toscrape.com/page/3/",
    "https://quotes.toscrape.com/page/3/",
    "https://quotes.toscrape.com/page/3/",
    "https://quotes.toscrape.com/page/3/",
    "https://quotes.toscrape.com/page/3/",
    "https://quotes.toscrape.com/page/3/",
    "https://quotes.toscrape.com/page/3/",
    "https://quotes.toscrape.com/page/3/",
    "https://quotes.toscrape.com/page/3/",
    "https://quotes.toscrape.com/page/3/",
    "https://quotes.toscrape.com/page/3/",
    "https://quotes.toscrape.com/page/3/",
    "https://quotes.toscrape.com/page/3/",
    "https://quotes.toscrape.com/page/3/",
    "https://quotes.toscrape.com/page/3/",
]


async def parse_and_save(session: aiohttp.ClientSession, url: str):
    async with session.get(url, timeout=10) as response:
        response.raise_for_status()
        html = await response.text()

    soup = BeautifulSoup(html, 'html.parser')

    quotes = soup.find_all('div', class_='quote')

    count = 0
    for quote in quotes:
        text = quote.find('span', class_='text').get_text(strip=True)

        author_elem = quote.find('small', class_='author')
        author = author_elem.get_text(strip=True) if author_elem else "Unknown"

        tags = quote.find_all('a', class_='tag')
        tags_str = ", ".join([tag.get_text(strip=True) for tag in tags])

        save_quote(text=text, author=author, tags=tags_str)
        count += 1


async def async_parser(urls: List[str]):
    connector = aiohttp.TCPConnector(limit=10)
    timeout = aiohttp.ClientTimeout(total=30)

    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        tasks = [parse_and_save(session, url) for url in urls]
        await asyncio.gather(*tasks)


def main():
    init_db()
    clear_quotes()

    start_time = time.time()

    asyncio.run(async_parser(URLS))

    end_time = time.time()
    execution_time = end_time - start_time

    total_quotes = count_quotes()

    print(f"Время выполнения: {execution_time:.2f} сек")
    print(f"Всего сохранено цитат: {total_quotes}")
    print(f"Среднее время на URL: {execution_time / len(URLS):.2f} сек")
    print(f"{'=' * 70}\n")

    return execution_time


if __name__ == "__main__":
    main()
