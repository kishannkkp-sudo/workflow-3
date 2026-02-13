import os
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/blogger"]

def blogger_service():
    creds = Credentials(
        token=None,
        refresh_token=os.getenv("BLOGGER_REFRESH_TOKEN"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.getenv("BLOGGER_CLIENT_ID"),
        client_secret=os.getenv("BLOGGER_CLIENT_SECRET"),
        scopes=SCOPES
    )
    return build("blogger", "v3", credentials=creds)


def publish_post(blog_id: str, title: str, html: str, labels=None, description=None, slug=None, publish_date=None) -> str:
    service = blogger_service()
    
    # Prepare post body
    post_body = {
        "title": title,
        "content": html,
        "isDraft": False
    }
    
    # Add labels if provided
    if labels:
        post_body["labels"] = labels

    # Add Meta Description (customMetaData or searchDescription depending on API behavior, user requested customMetaData)
    if description:
        # Note: 'customMetaData' might be a user-specific implementation detail or valid API field. 
        # API v3 uses 'customMetaData' for specific things or 'searchDescription' for meta description.
        # We will set 'customMetaData' as requested by user.
        post_body["customMetaData"] = description

    # Add URL Slug (if API permits - 'url' is the field, but often read-only)
    if slug:
         # Warning: Blogger API may ignore this or require it to be unique/valid
        post_body["url"] = slug

    # Add Scheduled Publish Date (ISO 8601 format)
    if publish_date:
        post_body["published"] = publish_date

    post = service.posts().insert(
        blogId=blog_id,
        body=post_body
    ).execute()

    return post["url"]