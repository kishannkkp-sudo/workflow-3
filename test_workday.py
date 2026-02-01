import requests
import json
import re

def get_workday_api_url(url):
    # Pattern: https://<host>/<path> -> https://<host>/wday/cxs/<tenant>/<site>/jobs
    # Example: https://boeing.wd1.myworkdayjobs.com/EXTERNAL_CAREERS
    # API: https://boeing.wd1.myworkdayjobs.com/wday/cxs/boeing/EXTERNAL_CAREERS/jobs
    
    match = re.search(r'https://([^/]+)/([^/]+)', url)
    if match:
        host = match.group(1)
        site = match.group(2)
        # Tenant is usually the first part of the host before .wdX, OR it's inside the path.
        # Actually for myworkdayjobs, the tenant is often needed.
        # Let's try to deduce tenant from host: boeing.wd1... -> boeing
        tenant = host.split('.')[0]
        
        return f"https://{host}/wday/cxs/{tenant}/{site}/jobs"
    return None

TEST_URLS = [
    "https://boeing.wd1.myworkdayjobs.com/EXTERNAL_CAREERS",
    "https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite"
]

for url in TEST_URLS:
    api_url = get_workday_api_url(url)
    print(f"Testing: {url} -> {api_url}")
    try:
        resp = requests.get(api_url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
        if resp.status_code == 200:
            data = resp.json()
            print(f"Success! Found {data['total']} jobs.")
            if data['jobPostings']:
                print(f"Sample: {data['jobPostings'][0]['title']} - {data['jobPostings'][0]['postedOn']}")
        else:
            print(f"Failed with {resp.status_code}")
    except Exception as e:
        print(f"Error: {e}")
    print("-" * 20)
