import os
import sys

# Ensure we can import from the directory
sys.path.append(os.getcwd())

from content_builder import build_html_content
from seo_utils import generate_seo_title, generate_slug, generate_meta_description, generate_labels, get_current_year

def test_seo_upgrades():
    print("Running SEO Upgrade Verification...")
    
    # Mock Data
    job_data = {
        "title": "Software Engineer",
        "company": "Tech Corp",
        "location": "Bangalore",
        "posted_on": "Today",
        "logo": "https://example.com/logo.png",
        "description": "<p>Job Description here...</p>",
        "apply_url": "https://example.com/apply",
        "company_url": "https://techcorp.com"
    }
    
    current_year = get_current_year()
    
    # 1. Test HTML Generation
    print("\n--- Testing HTML Generation ---")
    html = build_html_content(job_data)
    
    if f"IT Jobs {current_year}" in html:
        print("[PASS] Automatic Year Detected in HTML")
    else:
        print(f"[FAIL] Automatic Year NOT Found in HTML (Expected 'IT Jobs {current_year}')")

    if 'class="job-summary"' in html:
        print("[PASS] SEO Summary Block Present")
    else:
        print("[FAIL] SEO Summary Block Missing")
        
    if 'class="related-jobs"' in html:
        print("[PASS] Internal Linking Block Present")
    else:
        print("[FAIL] Internal Linking Block Missing")

    if '"@type": "FAQPage"' in html:
        print("[PASS] FAQ Schema Present")
    else:
        print("[FAIL] FAQ Schema Missing")

    # 2. Test SEO Utilities
    print("\n--- Testing SEO Utilities ---")
    
    title = generate_seo_title(job_data)
    print(f"Title: {title}")
    if f"Recruitment {current_year}" in title and "|" in title:
         print("[PASS] SEO Title Format Correct")
    else:
         print("[FAIL] SEO Title Format Incorrect")

    slug = generate_slug(job_data)
    print(f"Slug: {slug}")
    if slug == f"tech-corp-software-engineer-recruitment-{current_year}-bangalore":
        print("[PASS] Slug Generation Correct")
    else:
        print("[FAIL] Slug Generation Incorrect")

    desc = generate_meta_description(job_data)
    print(f"Meta Description: {desc}")
    if f"Recruitment {current_year}" in desc:
        print("[PASS] Meta Description Format Correct")
    else:
        print("[FAIL] Meta Description Format Incorrect")

    labels = generate_labels(job_data)
    print(f"Labels: {labels}")
    if f"IT Jobs {current_year}" in labels and "Tech Corp" in labels:
        print("[PASS] Labels Generated Correctly")
    else:
        print("[FAIL] Labels Generation Incorrect")

if __name__ == "__main__":
    test_seo_upgrades()
