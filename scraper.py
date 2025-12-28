import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0"}

def scrape_offcampusjobs4u():
    soup = BeautifulSoup(
        requests.get("https://offcampusjobs4u.com/", headers=HEADERS).text,
        "html.parser"
    )
    return [{"title": a.text.strip()} for a in soup.select("article h2 a")[:20]]


def scrape_job4freshers():
    soup = BeautifulSoup(
        requests.get("https://job4freshers.co.in/", headers=HEADERS).text,
        "html.parser"
    )
    return [{"title": a.text.strip()} for a in soup.select("h2.entry-title a")[:20]]
