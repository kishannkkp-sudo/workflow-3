import json
import random
import time
import re
from datetime import datetime, time as dt_time, timedelta
from dotenv import load_dotenv
from scraper import scrape_offcampusjobs4u, scrape_job4freshers
# from rewriter import rewrite_content
from formatter import markdown_to_html
from blogger import publish_post, blogger_service

load_dotenv()

# ✅ Load blogs
with open("blogs.json") as f:
    blogs = json.load(f)

# ✅ POST ONLY TO TECKFY
TECKFY = blogs[0]

def normalize_title(title: str) -> str:
    """
    Creates a normalized, lowercase hash of a title for comparison.
    Removes special characters and extra spaces.
    """
    # Remove common job post suffixes/prefixes that might vary
    title = re.sub(r'\b(hiring|walkin|walk-in|drive|notification|vacancy|job|opening)\b', '', title, flags=re.IGNORECASE)
    # Remove special characters and numbers, keep only letters and spaces
    title = re.sub(r'[^a-zA-Z\s]', '', title)
    # Convert to lowercase and remove extra whitespace
    return " ".join(title.lower().split())

def get_existing_titles(service, blog_id: str) -> set:
    """
    Fetches the last 100 posts from the blog and returns a set of
    normalized titles to check for duplicates.
    """
    print("Fetching existing posts from Blogger API to check for duplicates...")
    try:
        posts = service.posts().list(
            blogId=blog_id,
            maxResults=100, # Fetch the last 100 posts
            fields="items(title)" # Only fetch the titles to save bandwidth
        ).execute()
        
        normalized_titles = {normalize_title(p['title']) for p in posts.get('items', [])}
        print(f"Found {len(normalized_titles)} existing unique post titles.")
        return normalized_titles
    except Exception as e:
        print(f"Error fetching existing posts: {e}")
        # If API fails, return an empty set to proceed with caution
        return set()

def is_duplicate(title: str, existing_titles: set) -> bool:
    """Checks if a title's normalized version already exists."""
    return normalize_title(title) in existing_titles

def is_within_posting_hours():
    """Check if current time is within 6AM-6PM window."""
    now = datetime.now().time()
    return dt_time(6, 0) <= now <= dt_time(18, 0)

def get_random_posting_time():
    """Generate a random time between 6AM and 6PM."""
    hour = random.randint(6, 17)
    minute = random.randint(0, 59)
    return dt_time(hour, minute)

def wait_until_posting_time(target_time):
    """Wait until the specified time."""
    now = datetime.now()
    target = datetime.combine(now.date(), target_time)
    
    # If target time has passed today, schedule for tomorrow
    if target < now:
        target += timedelta(days=1)
    
    sleep_seconds = (target - now).total_seconds()
    print(f"Waiting until {target.strftime('%I:%M %p')} to post...")
    time.sleep(sleep_seconds)

def add_job_schema(html_content: str, title: str) -> str:
    """Add JobPosting schema for SEO."""
    schema = f"""
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "JobPosting",
        "title": "{title}",
        "datePosted": "{datetime.now().strftime('%Y-%m-%d')}",
        "description": "Detailed information about the job opportunity: {title}",
        "employmentType": "FULL_TIME",
        "hiringOrganization": {{
            "@type": "Organization",
            "name": "Various Companies"
        }}
    }}
    </script>
    """
    return html_content.replace('<div class="post-content">', f'<div class="post-content">{schema}')

def generate_labels(title: str) -> list:
    """Generate relevant labels based on job title."""
    labels = ["Jobs", "Career", "Hiring"]
    title_lower = title.lower()
    
    if any(word in title_lower for word in ["engineer", "developer", "software"]):
        labels.append("Engineering")
    if "freshers" in title_lower or "fresher" in title_lower:
        labels.append("Freshers")
    if "off campus" in title_lower:
        labels.append("Off Campus Drive")
    if "walk" in title_lower and "drive" in title_lower:
        labels.append("Walk-in Drive")
        
    return list(set(labels)) # Return unique labels

# --- Main Execution Logic ---

# 1. Initialize Blogger service and get existing titles
service = blogger_service()
existing_titles = get_existing_titles(service, TECKFY["blog_id"])

# 2. Collect job titles from scraper
print("Scraping new job listings from Workday sites...")
# Only scrape and post Workday jobs as per request
from workday_scraper import scrape_workday_jobs
from content_builder import build_html_content

# Fetch jobs posted TODAY
all_items = scrape_workday_jobs(limit=25) # Fetch a bit more to account for duplicates

# 3. Filter out duplicates by checking against the API data
new_items = [item for item in all_items if not is_duplicate(item["title"], existing_titles)]
print(f"Found {len(all_items)} total items, {len(new_items)} are new after duplicate check.")

# 4. Limit to 5 posts per day (AdSense Optimized)
max_posts = min(5, len(new_items))
if max_posts == 0:
    print("No new jobs to post today. Exiting.")
    exit()

# Randomly select items if there are more than max
items_to_post = random.sample(new_items, max_posts) if len(new_items) > max_posts else new_items
print(f"Will attempt to post {len(items_to_post)} jobs today.")

# 5. Assign random posting times and SCHEDULE via API
# Spreading posts over the NEXT 12 hours (e.g. 6am - 6pm IST)
# We assume the script runs once a day (e.g. at 6:00 AM IST)

base_time = datetime.now()
print(f"Current System Time: {base_time}")

# Prepare a list of future times for today/tomorrow
scheduled_times = []
for _ in range(len(items_to_post)):
    # Generate a random time offset between 10 minutes and 12 hours from now
    # This ensures posts are spread out over the day
    offset_minutes = random.randint(10, 720) 
    scheduled_time = base_time + timedelta(minutes=offset_minutes)
    scheduled_times.append(scheduled_time)

scheduled_times.sort()

# 6. Process and SCHEDULE each item
for i, item in enumerate(items_to_post):
    
    publish_at = scheduled_times[i]
    # Convert to ISO 8601 format required by Blogger API (RFC 3339)
    # We must ensure it has timezone info. .astimezone() uses system local time.
    publish_date_iso = publish_at.astimezone().isoformat()
    
    print("-" * 50)
    print(f"Scheduling ({i+1}/{len(items_to_post)}): {item['title']} - {item['company']}")
    print(f"   > Scheduled Time: {publish_at.astimezone().strftime('%Y-%m-%d %I:%M %p %Z')}")

    # Build HTML content
    try:
        html_content = build_html_content(item)
    except Exception as e:
        print(f"Error building HTML for {item['title']}: {e}")
        continue
    
    # 🚨 AdSense Gate: Check Word Count
    text_content = re.sub(r'<[^>]+>', '', html_content)
    word_count = len(text_content.split())
    
    if word_count < 900:
        print(f"⚠️ Skipping post due to Low Word Count: {word_count} words (Minimum 900 required)")
        continue
    else:
        print(f"✅ Word Count Pass: {word_count} words")

    # Generate SEO Metadata
    from seo_utils import generate_seo_title, generate_slug, generate_meta_description, generate_labels
    
    seo_title = generate_seo_title(item)
    seo_slug = generate_slug(item)
    seo_description = generate_meta_description(item)
    seo_labels = generate_labels(item)
    
    print(f"   > SEO Title: {seo_title}")
    print(f"   > Slug: {seo_slug}")

    try:
        url = publish_post(
            blog_id=TECKFY["blog_id"],
            title=seo_title,
            html=html_content,
            labels=seo_labels,
            description=seo_description,
            slug=seo_slug,
            publish_date=publish_date_iso # 👈 NEW: Schedule the post
        )
        print(f"✅ Successfully Scheduled: {url}")
        
        # Ping Sitemap (Deprecated/404)
        # from seo_utils import ping_sitemap
        # ping_sitemap()
        
        # Add the new title to our set to avoid potential duplicates within the same run
        existing_titles.add(normalize_title(item['title']))

    except Exception as e:
        print(f"❌ Failed to schedule post '{seo_title}'. Error: {e}")
    
    # Valid 5-minute delay between API calls as requested
    if i < len(items_to_post) - 1:
        print("Waiting 5 minutes before scheduling next post...")
        time.sleep(300)

print("-" * 50)
print("Daily scheduling process completed. GitHub Action will exit now.")
