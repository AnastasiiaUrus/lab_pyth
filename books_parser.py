import requests
from bs4 import BeautifulSoup
import csv
import re

BASE_URL = "https://books.toscrape.com/catalogue/"
START_URL = "https://books.toscrape.com/catalogue/page-1.html"

RATING_MAP = {
    "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5
}


def get_soup(url):
    """Отримує HTML сторінки та перетворює на об'єкт BeautifulSoup"""
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.content, 'html.parser')
    return None


def parse_book_data(book_tag):
    """Обробляє дані однієї конкретної книги"""
    title = book_tag.h3.a['title']

    # Витягуємо ціну та перетворюємо на число (прибираємо символ валюти)
    price_text = book_tag.find('p', class_='price_color').text
    price = float(re.sub(r'[^\d.]', '', price_text))

    # Витягуємо рейтинг з назви класів (напр. 'star-rating Three')
    rating_class = book_tag.find('p', class_='star-rating')['class'][1]
    rating = RATING_MAP.get(rating_class, 0)

    #очищаємо від зайвих пробілів та знаків
    availability = book_tag.find('p', class_='instock availability').text.strip()

    # Посилання на сторінку книги
    link_relative = book_tag.h3.a['href']
    link = f"https://books.toscrape.com/catalogue/{link_relative}"

    return {
        'title': title,
        'price': price,
        'rating': rating,
        'availability': availability,
        'link': link
    }


def main():
    all_books = []
    current_url = START_URL

    print("Починаємо збір даних...")

    while current_url:
        soup = get_soup(current_url)
        if not soup:
            break

        # Знаходимо всі блоки з книгами на сторінці
        book_tags = soup.find_all('article', class_='product_pod')
        for tag in book_tags:
            all_books.append(parse_book_data(tag))

        # Шукаємо посилання на наступну сторінку
        next_button = soup.find('li', class_='next')
        if next_button:
            next_page_url = next_button.a['href']
            # Перехід реалізовано через конкатенацію базового URL
            current_url = BASE_URL + next_page_url
            print(f"Перехід на: {current_url}")
        else:
            current_url = None

    total_books = len(all_books)
    prices = [b['price'] for b in all_books]
    avg_price = sum(prices) / total_books if total_books > 0 else 0

    # кількість книг для кожного рейтингу
    rating_stats = {i: 0 for i in range(1, 6)}
    for b in all_books:
        rating_stats[b['rating']] += 1

    # Найдорожча та найдешевша
    max_book = max(all_books, key=lambda x: x['price'])
    min_book = min(all_books, key=lambda x: x['price'])


    print("\n" + "=" * 30)
    print(f"Зібрано книг: {total_books}")
    print(f"Середня ціна: {avg_price:.2f} £")
    print(f"Найдорожча: {max_book['title']} ({max_book['price']} £)")
    print(f"Найдешевша: {min_book['title']} ({min_book['price']} £)")
    print("Статистика рейтингів:")
    for r, count in rating_stats.items():
        print(f"  Рейтинг {r}: {count} книг")
    print("=" * 30)

    with open('books.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['title', 'price', 'rating', 'availability', 'link'])
        writer.writeheader()
        writer.writerows(all_books)

    print("\nДані збережено у файл books.csv")


if __name__ == "__main__":
    main()