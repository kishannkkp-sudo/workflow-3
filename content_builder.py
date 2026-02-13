def build_html_content(job_data):
    """
    Generates HTML content for a job post matching the specific user-requested headers.
    """
    
    # Clean description (optional: remove inline styles if needed, but usually redundant)
    description_html = job_data['description']
    
    # Format date
    try:
        if "Today" in job_data['posted_on']:
             posted_date = datetime.now().strftime('%d %B %Y')
        else:
             posted_date = job_data['posted_on']
    except:
        posted_date = datetime.now().strftime('%d %B %Y')

    # Try to clean up company name for logo/display
    company_name = job_data['company']
    
    # Generate SEO content
    from seo_utils import (
        generate_summary, generate_related_block, generate_faq_schema, 
        get_current_year, generate_role_based_prep_guide, 
        generate_career_growth_section, generate_author_bio, generate_breadcrumb
    )
    
    seo_summary = generate_summary(job_data)
    related_block = generate_related_block(job_data)
    faq_schema = generate_faq_schema(job_data)
    prep_guide = generate_role_based_prep_guide(job_data)
    career_growth = generate_career_growth_section(job_data)
    author_bio = generate_author_bio()
    breadcrumbs = generate_breadcrumb(job_data)
    current_year = get_current_year()

    html = f"""
    <div class="job-post-container" style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto;">
        
        <!-- Breadcrumbs -->
        <div style="font-size: 14px; margin-bottom: 15px; color: #666;">
            {breadcrumbs}
        </div>

        <!-- Job Overview & Thumbnail -->
        <div style="text-align: center; margin-bottom: 20px;">
            <img src="{job_data['logo']}" alt="{company_name} Logo" style="max-width: 150px; height: auto; margin-bottom: 10px; border-radius: 8px; border: 1px solid #eee; padding: 5px;">
            <h1 style="color: #2c3e50; margin-bottom: 5px; font-size: 24px;">{job_data['title']}</h1>
            <p style="color: #7f8c8d; font-size: 16px; margin-top: 0;">{company_name}</p>
        </div>

        <!-- SEO Summary -->
        {seo_summary}

        <!-- 1. Job Overview -->
        <h2 style="color: #d35400; border-bottom: 2px solid #eee; padding-bottom: 5px;">Job Overview</h2>
        <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
            <tr>
                <td style="padding: 8px; border-bottom: 1px solid #ddd; font-weight: bold; width: 40%;">Role:</td>
                <td style="padding: 8px; border-bottom: 1px solid #ddd;">{job_data['title']}</td>
            </tr>
            <tr>
                <td style="padding: 8px; border-bottom: 1px solid #ddd; font-weight: bold;">Location:</td>
                <td style="padding: 8px; border-bottom: 1px solid #ddd;">{job_data['location']}</td>
            </tr>
            <tr>
                <td style="padding: 8px; border-bottom: 1px solid #ddd; font-weight: bold;">Employment Type:</td>
                <td style="padding: 8px; border-bottom: 1px solid #ddd;">Full Time / Permanent</td>
            </tr>
             <tr>
                <td style="padding: 8px; border-bottom: 1px solid #ddd; font-weight: bold;">Industry:</td>
                <td style="padding: 8px; border-bottom: 1px solid #ddd;">IT / Software / Core</td>
            </tr>
        </table>

        <!-- 2. Career Growth Analysis (New High Value Section) -->
        {career_growth}

        <!-- 3. Organization / Company Name -->
        <h2 style="color: #d35400; border-bottom: 2px solid #eee; padding-bottom: 5px;">Organization / Company Name</h2>
        <p><strong>{company_name}</strong></p>
        <p><em>(See full description for company details)</em></p>

        <!-- 4. Preparation Guide (New Role-Based Section) -->
        {prep_guide}

        <!-- 5. Important Dates -->
        <h2 style="color: #d35400; border-bottom: 2px solid #eee; padding-bottom: 5px;">Important Dates</h2>
        <ul style="list-style-type: square; padding-left: 20px;">
            <li><strong>Posted On:</strong> {posted_date}</li>
            <li><strong>Application Deadline:</strong> ASAP (Apply immediately)</li>
        </ul>

        <!-- 6. Job Description -->
        <h2 style="color: #d35400; border-bottom: 2px solid #eee; padding-bottom: 5px;">Job Description</h2>
        <div class="description-content" style="background: #f9f9f9; padding: 15px; border-radius: 5px;">
            {description_html}
        </div>

        <!-- 7. Educational Qualification -->
        <h2 style="color: #d35400; border-bottom: 2px solid #eee; padding-bottom: 5px;">Educational Qualification</h2>
        <p>Candidates should possess a relevant degree (B.E/B.Tech, M.E/M.Tech, MCA, or equivalent) from a recognized university. Please refer to the specific requirements in the Job Description above.</p>

        <!-- 8. Age Limit -->
        <h2 style="color: #d35400; border-bottom: 2px solid #eee; padding-bottom: 5px;">Age Limit</h2>
        <p>As per company rules. Generally, candidates should be at least 18 years of age.</p>

        <!-- 9. Salary / Pay Scale -->
        <h2 style="color: #d35400; border-bottom: 2px solid #eee; padding-bottom: 5px;">Salary / Pay Scale</h2>
        <p>Best in Industry / Not Disclosed by Company.</p>

        <!-- 10. Application Fee -->
        <h2 style="color: #d35400; border-bottom: 2px solid #eee; padding-bottom: 5px;">Application Fee</h2>
        <p><strong>NIL</strong> (No application fee for private jobs).</p>

        <!-- 11. Selection Process -->
        <h2 style="color: #d35400; border-bottom: 2px solid #eee; padding-bottom: 5px;">Selection Process</h2>
        <ul style="list-style-type: disc; padding-left: 20px;">
            <li>Resume Shortlisting</li>
            <li>Online Assessment / Technical Round</li>
            <li>HR Interview</li>
            <li><em>(Process may vary by company)</em></li>
        </ul>

        <!-- 12. How to Apply -->
        <h2 style="color: #d35400; border-bottom: 2px solid #eee; padding-bottom: 5px;">How to Apply</h2>
        <p>Interested and eligible candidates can apply online using the link provided below.</p>
        <ol>
            <li>Click on the "Apply Now" link below.</li>
            <li>You will be redirected to the official career page of {company_name}.</li>
            <li>Read the job details carefully.</li>
            <li>Click on "Apply" and fill in the required details.</li>
            <li>Submit your application.</li>
        </ol>

        <!-- 13. Important Links -->
        <h2 style="color: #d35400; border-bottom: 2px solid #eee; padding-bottom: 5px;">Important Links</h2>
        <div style="text-align: center; margin: 20px 0;">
            <a href="{job_data['apply_url']}" target="_blank" rel="nofollow" style="background-color: #28a745; color: white; padding: 15px 30px; text-decoration: none; font-size: 18px; border-radius: 5px; font-weight: bold; display: inline-block; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">Apply Now (Official Link)</a>
        </div>
        
        <!-- Internal Linking Block -->
        {related_block}

        <!-- 14. Important Instructions -->
        <h2 style="color: #d35400; border-bottom: 2px solid #eee; padding-bottom: 5px;">Important Instructions</h2>
        <ul style="list-style-type: circle; padding-left: 20px;">
            <li>Read the full job description on the official site before applying.</li>
            <li>Ensure your resume is updated and matches the job requirements.</li>
            <li>Check your email regularly for updates after applying.</li>
        </ul>

        <!-- 15. Author Bio (New Trust Signal) -->
        {author_bio}

        <!-- 16. Disclaimer -->
        <div class="disclaimer" style="font-size: 13px; color: #777; border-top: 1px solid #ddd; padding-top: 20px; margin-top: 40px; background-color: #fff3cd; padding: 10px; border-radius: 4px;">
            <p><strong>Disclaimer:</strong> This job posting is for information purposes only. We are not associated with {company_name} directly. All applications are processed through the official company website. Do not pay any money to anyone for this job.</p>
        </div>
        
        <script type="application/ld+json">
        {{
          "@context": "https://schema.org/",
          "@type": "JobPosting",
          "title": "{job_data['title']}",
          "description": "{job_data['title']} at {job_data['company']}",
          "hiringOrganization": {{
            "@type": "Organization",
            "name": "{company_name}",
            "sameAs": "{job_data['company_url']}",
            "logo": "{job_data['logo']}"
          }},
          "datePosted": "{datetime.now().strftime('%Y-%m-%d')}",
          "jobLocation": {{
            "@type": "Place",
            "address": {{
              "@type": "PostalAddress",
              "addressLocality": "{job_data['location']}",
              "addressCountry": "IN"
            }}
          }},
          "employmentType": "FULL_TIME"
        }}
        </script>
        <!-- FAQ Schema -->
        {faq_schema}
    </div>
    """
    return html
    
from datetime import datetime
