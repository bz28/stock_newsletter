from __future__ import annotations
import os
import base64
from email.mime.text import MIMEText
from pathlib import Path
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def get_gmail_service():
    # Path relative to this script
    cred_path = Path(__file__).resolve().parent / "credentials.json"
    token_path = Path(__file__).resolve().parent / "token.json"

    if not cred_path.exists():
        raise FileNotFoundError(f"credentials.json not found at: {cred_path}")

    creds = None
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(str(cred_path), SCOPES)
        creds = flow.run_local_server(port=0)
        token_path.write_text(creds.to_json())

    return build("gmail", "v1", credentials=creds)

def create_html_message(to_addrs: list[str] | str, subject: str, html_path: str, sender: str | None = None):
    if isinstance(to_addrs, list):
        to_header = ", ".join(to_addrs)
    else:
        to_header = to_addrs

    with open(html_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Remove any Markdown code fences (``` or ```html)
    cleaned_lines = [line for line in lines if not line.strip().startswith("```")]
    html = "".join(cleaned_lines)

    msg = MIMEText(html, "html")
    msg["to"] = to_header
    msg["subject"] = subject
    if sender:
        msg["from"] = sender  # optional; Gmail will use the authenticated account
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    return {"raw": raw}

if __name__ == "__main__":
    service = get_gmail_service()
    message = create_html_message(
        to_addrs=[],   # add emails
        subject="Daily Move Newsletter",
        html_path="test_prompts/email_formatting_prompt/output.html" 
    )
    sent = service.users().messages().send(userId="me", body=message).execute()
    print("Message Id:", sent.get("id"))