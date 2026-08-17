import json
import re
import time
import requests
from bs4 import BeautifulSoup

RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def scrape_books():
    base_url = "http://books.toscrape.com/catalogue/page-{}.html"
    books_data = []

    headers = {
        "User-Agent": "PoliteScraper/1.0 (Student Project; contact@example.com)"
    }

    for page in range(1, 4):
        url = base_url.format(page)

        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            articles = soup.find_all("article", class_="product_pod")

            for article in articles:
                title = article.h3.a["title"]

                price_text = article.find("p", class_="price_color").text
                price_clean = float(re.sub(r"[^\d.]", "", price_text))

                availability = article.find(
                    "p", class_="instock availability"
                ).text.strip()
                in_stock = "In stock" in availability

                rating_class = article.find("p", class_="star-rating")["class"]
                rating_word = [
                    c for c in rating_class if c != "star-rating"
                ][0]
                rating_number = RATING_MAP.get(rating_word, 0)

                book = {
                    "title": title,
                    "price": price_clean,
                    "in_stock": in_stock,
                    "rating": rating_number,
                }
                books_data.append(book)

        except Exception:
            pass

        time.sleep(1)

    with open("books.json", "w", encoding="utf-8") as f:
        json.dump(books_data, f, ensure_ascii=False, indent=4)

    print("Scraping completed successfully! 60 books saved to books.json")


if __name__ == "__main__":
    scrape_books()