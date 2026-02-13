import re
import requests
import json
import random
from datetime import datetime

# --- Role-Based Content Templates ---
ROLE_TEMPLATES = {
    "Software Engineer": {
        "prep_tips": [
            "Focus on Data Structures and Algorithms (DSA), especially Arrays, Linked Lists, and Trees.",
            "Practice coding problems on platforms like LeetCode and HackerRank.",
            "Revise core CS concepts: OS, DBMS, and Computer Networks.",
            "Prepare for System Design questions if applying for senior roles.",
            "Build a strong portfolio with full-stack projects using React, Node.js, or Django."
        ],
        "career_growth": [
            "Software Engineering is one of the highest-paying domains in India.",
            "With the rise of AI and Web3, demand for skilled engineers is at an all-time high.",
            "expect a salary hike of 10-30% annually with upskilling.",
            "Moving from service-based to product-based companies can double your package."
        ]
    },
    "Data Scientist": {
        "prep_tips": [
            "Master Python libraries: Pandas, NumPy, Scikit-learn, and TensorFlow.",
            "Brush up on Statistics and Probability theory.",
            "Practice SQL queries for data extraction and manipulation.",
            "Work on real-world datasets from Kaggle to showcase your skills.",
            "Understand the basics of MLOps and model deployment."
        ],
        "career_growth": [
            "Data Science is labeled the 'Sexiest Job of the 21st Century'.",
            "Companies are aggressively hiring for AI/ML roles in Bangalore and Hyderabad.",
            "Senior potential is huge, with paths leading to AI Architect or Chief Data Officer."
        ]
    },
    "Web Developer": {
        "prep_tips": [
            "Solidify your HTML, CSS, and JavaScript fundamentals.",
            "Learn a modern frontend framework like React.js, Vue.js, or Angular.",
            "Understand RESTful APIs and how to consume them.",
            "Practice building responsive layouts that work on all devices.",
            "Get familiar with version control (Git) and deployment platforms like Vercel."
        ],
        "career_growth": [
            "Web Development is the backbone of the digital economy.",
            "Freelancing opportunities are abundant for skilled web developers.",
            "Full-stack developers command premium salaries in the current market."
        ]
    },
    "General": {
        "prep_tips": [
            "Research the company's culture and values before the interview.",
            "Update your resume to highlight relevant skills and achievements.",
            "Prepare answers for common behavioral questions (STAR method).",
            "Work on your communication and soft skills.",
            "Mock interviews can significantly boost your confidence."
        ],
        "career_growth": [
            "The IT sector in India is projected to grow significantly in 2026.",
            "Continuous learning and upskilling are key to a long-term career.",
            "Networking on LinkedIn can open doors to unadvertised opportunities."
        ]
    }
}

def get_role_category(title):
    """Determines the role category based on the job title."""
    title_lower = title.lower()
    if any(k in title_lower for k in ["software", "sde", "engineer", "developer", "programmer"]):
        if "web" in title_lower or "frontend" in title_lower or "backend" in title_lower:
            return "Web Developer"
        return "Software Engineer"
    if any(k in title_lower for k in ["data", "analyst", "scientist", "ml", "ai"]):
        return "Data Scientist"
    return "General"

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

def generate_breadcrumb(job_data):
    """
    Generates a simple breadcrumb string.
    Format: Home > IT Jobs > {Company} Recruitment
    """
    return f"Home &gt; IT Jobs &gt; {job_data['company']} Recruitment"


def generate_role_based_prep_guide(job_data):
    """
    Generates a role-specific preparation guide using randomized templates.
    """
    role = get_role_category(job_data['title'])
    tips = ROLE_TEMPLATES.get(role, ROLE_TEMPLATES["General"])["prep_tips"]
    selected_tips = random.sample(tips, min(3, len(tips)))
    
    html = f"""
    <div class="prep-guide-section">
        <h3>🎯 How to Prepare for {job_data['title']} Role</h3>
        <p>To crack the interview at <strong>{job_data['company']}</strong>, focus on the following:</p>
        <ul class="prep-guide-list">
    """
    for tip in selected_tips:
        html += f"<li>{tip}</li>"
    html += """
        </ul>
    </div>
    """
    return html

def generate_career_growth_section(job_data):
    """
    Generates a high-value 'Why This Role' section.
    """
    role = get_role_category(job_data['title'])
    points = ROLE_TEMPLATES.get(role, ROLE_TEMPLATES["General"])["career_growth"]
    selected_points = random.sample(points, min(2, len(points)))
    year = get_current_year()
    
    html = f"""
    <div class="career-growth-section">
        <h3>🚀 Why {job_data['title']} is a Strategic Career Move in {year}</h3>
        <p>Joining <strong>{job_data['company']}</strong> as a {job_data['title']} offers excellent growth prospects. Here's why this role is trending:</p>
        <ul class="career-growth-list">
    """
    for point in selected_points:
         html += f"<li>{point}</li>"
    
    html += f"""
        </ul>
        <p><em>Industry Insight: {role} roles in {job_data['location']} are currently seeing high demand.</em></p>
    </div>
    """
    return html

def generate_author_bio():
    """
    Generates the specific Author Bio signal.
    """
    return """
    <div class="author-bio">
        <div class="bio-img-wrapper">
            <img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgLI2OWm0OjCH8plxz9SkZZ_k_rOC2sUNoCy00qmVL9Z7Z5ACxKeNnWYypZPnA4g_UxNxhfFf8wszR3uYCKCWraO06QfqgP4iRrbAUSzfCX2YIWXnlpMChVpjINtFDpnOoiiCWlAn9rxDN8WNGzPZWftcodAnlNbdqKUljDMsIT4ZnfrhKFkrkTGyj2xK6n/s1600/FirstJobTech_logo_175x55.png" alt="Kishan Prajapati">
        </div>
        <div class="bio-text">
            <h4>Kishan Prajapati</h4>
            <p>Career Researcher & IT Industry Analyst. Helping freshers and professionals find verified private IT job opportunities in India.</p>
        </div>
    </div>
    """

def generate_summary(job_data):
    """
    Generates a unique 300-word summary to prevent thin content issues.
    """
    year = get_current_year()
    return f"""
<div class="job-summary">
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
<div class="related-jobs-block">
    <h3>Latest IT Jobs {year}</h3>
    <ul>
        <li>👉 <a href='/search/label/IT Jobs {year}'>More IT Jobs {year}</a></li>
        <li>👉 <a href='/search/label/{job_data['location']}'>Jobs in {job_data['location']}</a></li>
        <li>👉 <a href='/search/label/{job_data['company']}'>More {job_data['company']} Jobs</a></li>
        <li>👉 <a href='/search/label/Freshers Jobs'>Latest Freshers Jobs</a></li>
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
