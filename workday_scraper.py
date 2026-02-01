import requests
import re
import time
from datetime import datetime

# Full list of companies from the request
COMPANIES = [
    {"name": "Boeing", "url": "https://boeing.wd1.myworkdayjobs.com/EXTERNAL_CAREERS"},
    {"name": "3M", "url": "https://3m.wd1.myworkdayjobs.com/search"},
    {"name": "Adobe", "url": "https://adobe.wd5.myworkdayjobs.com/external_experienced"},
    {"name": "NVIDIA", "url": "https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite"},
    {"name": "Salesforce", "url": "https://salesforce.wd12.myworkdayjobs.com/External_Career_Site"},
    {"name": "Target", "url": "https://target.wd5.myworkdayjobs.com/targetcareers"},
    {"name": "Walmart", "url": "https://walmart.wd5.myworkdayjobs.com/WalmartExternal"},
    {"name": "Chevron", "url": "https://chevron.wd5.myworkdayjobs.com/jobs"},
    {"name": "Deloitte", "url": "https://deloitteie.wd3.myworkdayjobs.com/Early_Careers"},
    {"name": "Puma", "url": "https://puma.wd3.myworkdayjobs.com/Jobs_at_Puma"},
    {"name": "Sanofi", "url": "https://sanofi.wd3.myworkdayjobs.com/SanofiCareers"},
    {"name": "Comcast", "url": "https://comcast.wd5.myworkdayjobs.com/Comcast_Careers"},
    {"name": "Abbott", "url": "https://abbott.wd5.myworkdayjobs.com/abbottcareers"},
    {"name": "Alcoa", "url": "https://alcoa.wd5.myworkdayjobs.com/careers/1/refreshFacet/318c8bb6f553100021d223d9780d30be"},
    {"name": "American Electric Power", "url": "https://aep.wd1.myworkdayjobs.com/AEPCareerSite"},
    {"name": "Amgen", "url": "https://amgen.wd1.myworkdayjobs.com/Careers"},
    {"name": "Applied Materials", "url": "https://amat.wd1.myworkdayjobs.com/External"},
    {"name": "Arrow Electronics", "url": "https://arrow.wd1.myworkdayjobs.com/AC"},
    {"name": "Assurant", "url": "https://assurant.wd1.myworkdayjobs.com/Assurant_Careers"},
    {"name": "AT&T", "url": "https://att.wd1.myworkdayjobs.com/ATTGeneral"},
    {"name": "Avis Budget Group", "url": "https://avisbudget.wd1.myworkdayjobs.com/ABG_Careers"},
    {"name": "BlackRock", "url": "https://blackrock.wd1.myworkdayjobs.com/BlackRock_Professional"},
    {"name": "Bupa", "url": "https://bupa.wd3.myworkdayjobs.com/EXT_CAREER"},
    {"name": "Cognizant", "url": "https://collaborative.wd1.myworkdayjobs.com/AllOpenings"},
    {"name": "Workday", "url": "https://workday.wd5.myworkdayjobs.com/Workday"},
    {"name": "Fidelity", "url": "https://wd1.myworkdaysite.com/en-US/recruiting/fmr/FidelityCareers"},
    {"name": "AIG", "url": "https://aig.wd1.myworkdayjobs.com/aig"},
    {"name": "Analog Devices", "url": "https://analogdevices.wd1.myworkdayjobs.com/External"},
    {"name": "Intel", "url": "https://intel.wd1.myworkdayjobs.com/External"},
    {"name": "Mastercard", "url": "https://mastercard.wd1.myworkdayjobs.com/CorporateCareers"},
    {"name": "JLL", "url": "https://jll.wd1.myworkdayjobs.com/jllcareers"},
    {"name": "CNX", "url": "https://cnx.wd1.myworkdayjobs.com/external_global"},
    {"name": "Coca-Cola", "url": "https://coke.wd5.myworkdayjobs.com/coca-cola-careers"},
    {"name": "Dell", "url": "https://dell.wd1.myworkdayjobs.com/External"},
    {"name": "Bank of America", "url": "https://ghr.wd1.myworkdayjobs.com/Lateral-US"},
    {"name": "Accenture", "url": "https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/"},
    {"name": "PwC", "url": "https://pwc.wd3.myworkdayjobs.com/Global_Experienced_Careers"},
    {"name": "Huron", "url": "https://huron.wd1.myworkdayjobs.com/huroncareers"},
    {"name": "ING", "url": "https://ing.wd3.myworkdayjobs.com/ICSGBLCOR"},
    {"name": "eBay", "url": "https://ebay.wd5.myworkdayjobs.com/apply/"},
    {"name": "AstraZeneca", "url": "https://astrazeneca.wd3.myworkdayjobs.com/Careers"},
    {"name": "Nexstar", "url": "https://nexstar.wd5.myworkdayjobs.com/nexstar"},
    {"name": "Samsung", "url": "https://sec.wd3.myworkdayjobs.com/Samsung_Careers"},
    {"name": "Warner Bros", "url": "https://warnerbros.wd5.myworkdayjobs.com/global"},
    {"name": "Hitachi", "url": "https://hitachi.wd1.myworkdayjobs.com/hitachi"},
    {"name": "Ciena", "url": "https://ciena.wd5.myworkdayjobs.com/Careers"},
    {"name": "BDX", "url": "https://bdx.wd1.myworkdayjobs.com/EXTERNAL_CAREER_SITE_INDIA"},
    {"name": "Cengage", "url": "https://cengage.wd5.myworkdayjobs.com/CengageIndiaCareers"},
    {"name": "Pfizer", "url": "https://pfizer.wd1.myworkdayjobs.com/PfizerCareers"},
    {"name": "Availity", "url": "https://availity.wd1.myworkdayjobs.com/Availity_Careers_India"},
    {"name": "Wells Fargo", "url": "https://wd1.myworkdaysite.com/recruiting/wf/WellsFargoJobs"},
    {"name": "Motorola Solutions", "url": "https://motorolasolutions.wd5.myworkdayjobs.com/Careers"},
    {"name": "2020 Companies", "url": "https://2020companies.wd1.myworkdayjobs.com/External_Careers"},
    {"name": "Kyndryl", "url": "https://kyndryl.wd5.myworkdayjobs.com/KyndrylProfessionalCareers"},
    {"name": "IFF", "url": "https://iff.wd5.myworkdayjobs.com/en-US/iff_careers"},
    {"name": "Light & Wonder", "url": "https://lnw.wd5.myworkdayjobs.com/LightWonderExternalCareers"},
    {"name": "Bristol Myers Squibb", "url": "https://bristolmyerssquibb.wd5.myworkdayjobs.com/BMS"},
    {"name": "Alcon", "url": "https://alcon.wd5.myworkdayjobs.com/careers_alcon"},
    {"name": "DXC Technology", "url": "https://dxctechnology.wd1.myworkdayjobs.com/DXCJobs"},
    {"name": "London Stock Exchange Group (LSEG)", "url": "https://lseg.wd3.myworkdayjobs.com/Careers"},
    {"name": "Cigna", "url": "https://cigna.wd5.myworkdayjobs.com/cignacareers"},
    {"name": "GE Vernova", "url": "https://gevernova.wd5.myworkdayjobs.com/Vernova_ExternalSite"},
    {"name": "Clarivate", "url": "https://clarivate.wd3.myworkdayjobs.com/Clarivate_Careers"},
    {"name": "Silicon Labs", "url": "https://silabs.wd1.myworkdayjobs.com/SiliconLabsCareers"},
    {"name": "Micron", "url": "https://micron.wd1.myworkdayjobs.com/External"},
    {"name": "Blackbaud", "url": "https://blackbaud.wd1.myworkdayjobs.com/ExternalCareers"},
    {"name": "FIS", "url": "https://fis.wd5.myworkdayjobs.com/en-US/SearchJobs"},
    {"name": "Web Industries", "url": "https://web.wd1.myworkdayjobs.com/ExternalCareerSite"},
    {"name": "Qualys", "url": "https://qualys.wd5.myworkdayjobs.com/Careers"},
    {"name": "Optiv", "url": "https://optiv.wd5.myworkdayjobs.com/Optiv_Careers"},
    {"name": "T-Mobile", "url": "https://tmobile.wd5.myworkdayjobs.com/External"},
    {"name": "Morningstar", "url": "https://morningstar.wd5.myworkdayjobs.com/Americas"}
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def get_session():
    return requests.Session()

def resolve_api_parts(url):
    """
    Extracts host, tenant, and site to build API endpoints.
    Supported pattern: https://<host>/<site>
    """
    match = re.search(r'https://([^/]+)/([^/]+)', url)
    if match:
        host = match.group(1)
        site = match.group(2)
        # Attempt to deduce tenant. Usually host is tenant.wdX...
        # Workday host format is usually: <tenant>.wdX.myworkdayjobs.com
        tenant = host.split('.')[0]
        
        # Special case for some URLs that might have paths, but the standard list is clean
        return host, tenant, site
    return None, None, None

def fetch_job_details(host, tenant, site, job_slug):
    """
    Fetches full job description using the job slug.
    API: https://<host>/wday/cxs/<tenant>/<site>/job/<slug>
    """
    url = f"https://{host}/wday/cxs/{tenant}/{site}/job/{job_slug}"
    try:
        resp = requests.get(url, headers=HEADERS) # GET for details
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        print(f"Error fetching details for {job_slug}: {e}")
    return None

def scrape_workday_jobs(limit=20):
    """
    Iterates through companies and finds jobs posted TODAY.
    Returns a list of detailed job objects.
    """
    all_jobs = []
    session = get_session()
    
    print(f"Scanning {len(COMPANIES)} companies for jobs posted TODAY...")
    
    for company in COMPANIES:
        try:
            host, tenant, site = resolve_api_parts(company["url"])
            if not host:
                continue
                
            api_url = f"https://{host}/wday/cxs/{tenant}/{site}/jobs"
            payload = {
                "appliedFacets": {},
                "limit": 20, # Check top 20 most recent
                "offset": 0,
                "searchText": ""
            }
            
            resp = session.post(api_url, headers=HEADERS, json=payload, timeout=10)
            if resp.status_code != 200:
                print(f"Skipping {company['name']}: API Error {resp.status_code}")
                continue
                
            data = resp.json()
            postings = data.get("jobPostings", [])
            
            # Find jobs posted today
            today_jobs = []
            for job in postings:
                if "postedOn" in job and "Today" in job["postedOn"]:
                    today_jobs.append(job)
            
            if today_jobs:
                print(f"Found {len(today_jobs)} new jobs at {company['name']}")
                
                for job in today_jobs:
                    # Filter for INDIA jobs
                    locations = job.get("locationsText", "") + job.get("location", "")
                    if "India" not in locations and "INDIA" not in locations.upper():
                         continue

                    # Construct proper slug. 
                    # externalPath is like /job/location/title_R123
                    # API expects just title_R123 usually, or maybe full path works if we strip /job/
                    # Let's try to extract the last part of externalPath
                    slug = job["externalPath"].split('/')[-1]
                    
                    details = fetch_job_details(host, tenant, site, slug)
                    if details:
                         # Double check location in details
                        det_loc = details["jobPostingInfo"].get("location", "")
                        if "India" not in det_loc and "INDIA" not in det_loc.upper():
                             continue

                        all_jobs.append({
                            "title": details["jobPostingInfo"]["title"],
                            "company": company["name"],
                            "company_url": company["url"],
                            "description": details["jobPostingInfo"]["jobDescription"],
                            "location": det_loc,
                            "posted_on": details["jobPostingInfo"]["postedOn"],
                            "apply_url": f"{company['url']}{job['externalPath']}",
                            "logo": f"https://logos-api.apistemic.com/domain:{company['name'].replace(' ', '').lower()}.com"
                        })

            if len(all_jobs) >= limit:
                 break
                 
        except Exception as e:
            print(f"Error scraping {company['name']}: {e}")
            continue
            
    return all_jobs[:limit]

if __name__ == "__main__":
    jobs = scrape_workday_jobs()
    print(f"Total jobs found: {len(jobs)}")
