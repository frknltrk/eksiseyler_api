import requests
from bs4 import BeautifulSoup


def scrape_articles():
    url = "https://eksiseyler.com/"
    h = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0"
    }
    response = requests.get(url, headers=h)
    soup = BeautifulSoup(response.content, "lxml")
    articles = []

    divs = soup.find_all("div", class_=["content-img", "mashup-img"])

    articles = []
    for div in divs:
        url = div.a["href"]
        title = div.img["alt"]
        img = div.img.get("data-src") or div.img.get("src")  # content-img or mashup-img

        # as tuples:
        articles.insert(0, (url, title, img))
        # as dict items:
        # parsed_dict.append({
        #     'article_url': url,
        #     'article_title': title,
        #     'cover_image': img
        # })

    return articles
