"""
Multiprocessing подход для параллельного парсинга цитат
Загружает HTML, парсит цитаты и сохраняет в БД используя процессы
"""

import multiprocessing
import time
from typing import List
import requests
from bs4 import BeautifulSoup
from db import init_db, save_quote, clear_quotes, count_quotes

# Список URL-адресов для парсинга
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


def parse_and_save(url: str):
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

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


def multiprocessing_parser(urls: List[str]):
    processes = []

    for url in urls:
        process = multiprocessing.Process(target=parse_and_save, args=(url,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()


def main():
    init_db()
    clear_quotes()

    start_time = time.time()

    multiprocessing_parser(URLS)

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
