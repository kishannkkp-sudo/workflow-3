import requests
import json
import re

def get_workday_api_url(url):
    match = re.search(r'https://([^/]+)/([^/]+)', url)
    if match:
        host = match.group(1)
        site = match.group(2)
        tenant = host.split('.')[0]
        return f"https://{host}/wday/cxs/{tenant}/{site}/jobs"
    return None

TEST_URLS = [
    "https://boeing.wd1.myworkdayjobs.com/EXTERNAL_CAREERS",
    "https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

PAYLOAD = {
    "appliedFacets": {},
    "limit": 20,
    "offset": 0,
    "searchText": ""
}

for url in TEST_URLS:
    api_url = get_workday_api_url(url)
    print(f"Testing: {url} -> {api_url}")
    try:
        resp = requests.post(api_url, headers=HEADERS, json=PAYLOAD)
        if resp.status_code == 200:
            data = resp.json()
            print(f"Success! Found {data['total']} jobs.")
            if data['jobPostings']:
                print(f"Sample: {data['jobPostings'][0]['title']} - {data['jobPostings'][0]['postedOn']}")
        else:
            print(f"Failed with {resp.status_code}")
            print(resp.text[:200])
    except Exception as e:
        print(f"Error: {e}")
    print("-" * 20)
