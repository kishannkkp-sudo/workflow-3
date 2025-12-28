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


def publish_post(blog_id: str, title: str, html: str, labels=None) -> str:
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

    post = service.posts().insert(
        blogId=blog_id,
        body=post_body
    ).execute()

    return post["url"]