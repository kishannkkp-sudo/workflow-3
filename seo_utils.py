import re
import requests
import json
from datetime import datetime

def get_current_year():
    """Returns the current year dynamically."""
    return datetime.now().year

def generate_seo_title(job_data):
    """
    Generates an SEO-optimized title.
    Format: {Company} {Title} Recruitment {Year} – {Location} | Apply Online
    """
    year = get_current_year()
    return f"{job_data['company']} {job_data['title']} Recruitment {year} – {job_data['location']} | Apply Online"

def generate_slug(job_data):
    """
    Generates an SEO-friendly slug (permalink).
    Format: company-title-recruitment-year-location
    """
    year = get_current_year()
    slug = f"{job_data['company']} {job_data['title']} recruitment {year} {job_data['location']}"
    # Remove special characters, keep alphanumeric and spaces
    slug = re.sub(r'[^a-zA-Z0-9\s]', '', slug)
    # Convert to lowercase and replace spaces with hyphens
    return slug.lower().strip().replace(" ", "-")

def generate_meta_description(job_data):
    """
    Generates a high-CTR meta description.
    """
    year = get_current_year()
    return f"Apply for {job_data['company']} {job_data['title']} Recruitment {year} in {job_data['location']}. Check eligibility, salary, selection process and apply online link."

def generate_labels(job_data):
    """
    Generates SEO-friendly labels for the post.
    """
    year = get_current_year()
    labels = [
        job_data['company'],
        job_data['location'],
        f"IT Jobs {year}",
        f"Private Jobs {year}",
        job_data['title']
    ]
    
    # Add extra categories if relevant
    title_lower = job_data['title'].lower()
    if any(word in title_lower for word in ["engineer", "developer", "software"]):
        labels.append("Engineering Jobs")
    if "fresher" in title_lower:
        labels.append("Freshers Jobs")
    
    return list(set(labels))  # Remove duplicates

def generate_summary(job_data):
    """
    Generates a unique 300-word summary to prevent thin content issues.
    """
    year = get_current_year()
    return f"""
<div class="job-summary" style="background-color: #f0fdf4; border-left: 4px solid #28a745; padding: 15px; margin-bottom: 20px; font-size: 16px;">
    <p><strong>{job_data['company']}</strong> is hiring talented professionals for the position of <strong>{job_data['title']}</strong> in <strong>{job_data['location']}</strong>. 
    This opportunity is ideal for candidates looking to build a strong career in the IT industry in {year}. 
    Applicants should carefully review the eligibility criteria, required skills, and selection process before applying online.</p>
    
    <p>The recruitment drive for {year} offers a great chance for job seekers to join a reputed organization. 
    Make sure to prepare well for the interview and submit your application before the deadline. 
    Read below for full details on how to apply, educational qualifications, and other important instructions.</p>
</div>
"""

def generate_related_block(job_data):
    """
    Generates an internal linking block for SEO.
    """
    year = get_current_year()
    return f"""
<div class="related-jobs" style="margin-top: 30px; padding: 20px; background-color: #f8f9fa; border-radius: 8px;">
    <h3 style="color: #2c3e50; border-bottom: 2px solid #ddd; padding-bottom: 5px;">Latest IT Jobs {year}</h3>
    <ul style="list-style-type: none; padding: 0;">
        <li style="margin-bottom: 8px;">👉 <a href='/search/label/IT Jobs {year}' style="text-decoration: none; color: #007bff; font-weight: bold;">More IT Jobs {year}</a></li>
        <li style="margin-bottom: 8px;">👉 <a href='/search/label/{job_data['location']}' style="text-decoration: none; color: #007bff; font-weight: bold;">Jobs in {job_data['location']}</a></li>
        <li style="margin-bottom: 8px;">👉 <a href='/search/label/{job_data['company']}' style="text-decoration: none; color: #007bff; font-weight: bold;">More {job_data['company']} Jobs</a></li>
        <li style="margin-bottom: 8px;">👉 <a href='/search/label/Freshers Jobs' style="text-decoration: none; color: #007bff; font-weight: bold;">Latest Freshers Jobs</a></li>
    </ul>
</div>
"""

def generate_faq_schema(job_data):
    """
    Generates FAQ Schema for Rich Snippets.
    """
    year = get_current_year()
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f"What is the role at {job_data['company']}?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"The role is for the position of {job_data['title']}."
                }
            },
            {
                "@type": "Question",
                "name": f"Where is the job location for {job_data['company']} recruitment?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"The job location is {job_data['location']}."
                }
            },
            {
                "@type": "Question",
                "name": f"Is this a freshers job?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"Please refer to the detailed eligibility criteria in the post to confirm if freshers can apply for the {job_data['title']} role."
                }
            },
            {
                "@type": "Question",
                "name": "How to apply for this job?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"You can apply online by clicking the 'Apply Now' link provided in the Important Links section."
                }
            }
        ]
    }
    return f'<script type="application/ld+json">{json.dumps(schema, indent=2)}</script>'

def ping_sitemap(sitemap_url="https://www.firstjobtech.in/sitemap.xml"):
    """
    Pings Google with the sitemap URL to speed up indexing.
    """
    ping_url = f"https://www.google.com/ping?sitemap={sitemap_url}"
    try:
        response = requests.get(ping_url)
        if response.status_code == 200:
            print(f"✅ Successfully pinged Google Sitemap: {sitemap_url}")
        else:
            print(f"⚠️ Failed to ping sitemap. Status Code: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Error pinging sitemap: {e}")
