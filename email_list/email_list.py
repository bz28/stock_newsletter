from __future__ import annotations
import os, re, base64, time
from pathlib import Path
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from bs4 import BeautifulSoup

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

# ---------- Gmail auth ----------
def get_gmail_service():
    here = Path(__file__).resolve().parent
    cred_path = here / "credentials.json"
    token_path = here / "token.json"

    if not cred_path.exists():
        raise FileNotFoundError(f"credentials.json not found at: {cred_path}")

    creds = Credentials.from_authorized_user_file(str(token_path), SCOPES) if token_path.exists() else None
    if not creds:
        flow = InstalledAppFlow.from_client_secrets_file(str(cred_path), SCOPES)
        creds = flow.run_local_server(port=0)
        token_path.write_text(creds.to_json())

    return build("gmail", "v1", credentials=creds)

# ---------- HTML loading / cleaning ----------
def load_clean_html(path: str | Path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()
    # Drop Markdown code fences like ``` or ```html
    raw = "\n".join(line for line in raw.splitlines() if not line.strip().startswith("```"))
    # If there’s extra noise, keep only from <!DOCTYPE html> ... </html>
    m = re.search(r'<!DOCTYPE\s+html[^>]*>.*?</html\s*>', raw, flags=re.IGNORECASE | re.DOTALL)
    return m.group(0) if m else raw

# ---------- Message creation ----------
def create_html_message(
    to_addr: str,
    subject: str,
    html_path: str | Path,
    sender: str | None = None,
    list_unsub_mailto: str | None = None,
    list_unsub_url: str | None = None,
):
    html = load_clean_html(html_path)

    msg = MIMEText(html, "html")
    msg["to"] = to_addr
    msg["subject"] = subject
    if sender:
        msg["from"] = sender  # Gmail will enforce the authenticated account/alias

    # List-Unsubscribe (improves deliverability; required for some providers)
    lus = []
    if list_unsub_mailto:
        lus.append(f"<mailto:{list_unsub_mailto}>")
    if list_unsub_url:
        lus.append(f"<{list_unsub_url}>")
    if lus:
        msg["List-Unsubscribe"] = ", ".join(lus)
        # Optional: one-click unsubscribe
        msg["List-Unsubscribe-Post"] = "List-Unsubscribe=One-Click"

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    return {"raw": raw}

# ---------- Sending helpers ----------
def read_recipients(path: str | Path = "test_email_list.txt") -> list[str]:
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]

def send_html_to_list(
    service,
    subject: str,
    html_path: str | Path,
    recipients_path: str | Path = "test_email_list.txt",
    sender: str | None = None,
    list_unsub_mailto: str | None = None,
    list_unsub_url: str | None = None,
    pause_seconds: float = 0.5,
):
    recipients = read_recipients(recipients_path)
    print(f"Sending to {len(recipients)} recipient(s)…")

    for i, r in enumerate(recipients, 1):
        body = create_html_message(
            to_addr=r,
            subject=subject,
            html_path=html_path,
            sender=sender,
            list_unsub_mailto=list_unsub_mailto,
            list_unsub_url=list_unsub_url,
        )
        try:
            sent = service.users().messages().send(userId="me", body=body).execute()
            print(f"[{i}/{len(recipients)}] Sent → {r}  id={sent.get('id')}")
        except HttpError as e:
            # Basic backoff on rate/limit errors
            status = getattr(e, "status_code", None) or getattr(e, "resp", {}).status if hasattr(e, "resp") else None
            print(f"[{i}/{len(recipients)}] ERROR sending to {r}: {e}")
            if status in (403, 429, 500, 503):
                time.sleep(2.0)
        time.sleep(pause_seconds)


def extract_headline(html_path: str) -> str:
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # Try original class-based headline first
    headline = soup.find("p", class_="headline")
    if headline:
        return headline.get_text(strip=True)

    # Otherwise fall back to the first big <td> styled as headline
    td_headline = soup.find("td", style=lambda s: s and "font-size:28px" in s)
    if td_headline:
        return td_headline.get_text(strip=True)

    return "Daily Newsletter"

# ---------- Main ----------
if __name__ == "__main__":
    service = get_gmail_service()

    try:
        prof = service.users().getProfile(userId="me").execute()
        print("Authenticated as:", prof.get("emailAddress"))
    except Exception:
        pass

    html_path = "test_prompts/email_formatting_prompt/output.html"
    subject = extract_headline(html_path)
    recipients_path = "email_list/test_email_list.txt"

    send_html_to_list(
        service=service,
        subject=subject,
        html_path=html_path,
        recipients_path=recipients_path, 
        sender=None,                      
        pause_seconds=0.5,
    )

