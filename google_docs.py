import os
import datetime  
from googleapiclient.discovery import build
from google.oauth2 import service_account

SERVICE_ACCOUNT_FILE = "google_creds.json"
SCOPES = ["https://www.googleapis.com/auth/documents"]

def write_to_google_docs(document_id, content):
    """Writes AI-generated LinkedIn posts to Google Docs with no extra explanations."""
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    docs_service = build("docs", "v1", credentials=creds)

    formatted_content = f"""
📌 **Generated LinkedIn Posts for 1 Month:**  
{content}  
"""
    
    requests = [{"insertText": {"location": {"index": 1}, "text": formatted_content + "\n\n"}}]
    docs_service.documents().batchUpdate(documentId=document_id, body={"requests": requests}).execute()

    print(f"✅ Saved to Google Docs: https://docs.google.com/document/d/{document_id}")
