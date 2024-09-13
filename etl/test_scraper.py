from scraper import scrape_articles

if __name__ == "__main__":
    max_pages = 5  # Set the number of pages you want to scrape
    articles = scrape_articles(max_pages=max_pages)
    for article in articles:
        print(article)
