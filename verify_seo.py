import os
import sys
import re

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
        "description": "<p>Job Description here... " + "word " * 500 + "</p>", # Simulate length
        "apply_url": "https://example.com/apply",
        "company_url": "https://techcorp.com"
    }
    
    current_year = get_current_year()
    
    # 1. Test HTML Generation
    print("\n--- Testing HTML Generation ---")
    html = build_html_content(job_data)
    
    # Word Count Check
    text_content = re.sub(r'<[^>]+>', '', html)
    word_count = len(text_content.split())
    print(f"Total Word Count: {word_count}")
    
    if word_count > 900:
        print("[PASS] Word Count > 900 (AdSense Safe)")
    else:
        print(f"[FAIL] Word Count Low ({word_count} words). Target: 900+")

    # Section Checks
    checks = {
        "Breadcrumbs": "Home &gt; IT Jobs",
        "SEO Summary": 'class="job-summary"',
        "Career Growth": 'class="career-growth-section"',
        "Prep Guide": 'class="prep-guide-section"',
        "Author Bio": 'class="author-bio"',
        "Internal Links": 'class="related-jobs"',
        "FAQ Schema": '"@type": "FAQPage"'
    }

    for name, marker in checks.items():
        if marker in html:
            print(f"[PASS] {name} Section Present")
        else:
            print(f"[FAIL] {name} Section Missing")

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
