import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def get_session():
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def scrape_offcampusjobs4u():
    try:
        session = get_session()
        response = session.get("https://offcampusjobs4u.com/", headers=HEADERS, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        # Added check to ensure elements exist before accessing text
        return [{"title": a.text.strip()} for a in soup.select("article h2 a")[:20] if a]
    except Exception as e:
        print(f"Error scraping offcampusjobs4u: {e}")
        return []

def scrape_job4freshers():
    try:
        session = get_session()
        response = session.get("https://job4freshers.co.in/", headers=HEADERS, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        return [{"title": a.text.strip()} for a in soup.select("h2.entry-title a")[:20] if a]
    except Exception as e:
        print(f"Error scraping job4freshers: {e}")
        return []
