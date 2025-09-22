from dotenv import load_dotenv
import os
from openai import OpenAI
from datetime import datetime, timedelta, time
import zoneinfo

# -----------------------
# Setup
# -----------------------
load_dotenv()
gpt_api_key = os.environ.get('GPT_API_KEY')
client = OpenAI(api_key=gpt_api_key)

# Load input list
file_path = "test_prompts/viral_stocks_prompt/output.txt"
with open(file_path, "r", encoding="utf-8") as f:
    viral_stocks_content = f.read()

# -----------------------
# Time helpers (America/New_York)
# -----------------------
NY = zoneinfo.ZoneInfo("America/New_York")

def prev_business_day(d):
    # Step back one day, skip weekends
    d -= timedelta(days=1)
    while d.weekday() >= 5:  # 5=Sat, 6=Sun
        d -= timedelta(days=1)
    return d

def compute_session_date_and_status(now_et: datetime):
    """
    Returns:
      session_date: date whose close % we want
      require_market_not_closed_tag: bool, only True when it's a weekday before close+10m
    """
    weekday = now_et.weekday()  # 0=Mon ... 6=Sun
    market_close = time(16, 0)  # 4:00 pm ET (ignore rare early closes here)
    cutoff = (datetime.combine(now_et.date(), market_close, tzinfo=NY)
              + timedelta(minutes=10))

    # Weekend: always use last Friday; no MARKET_NOT_CLOSED tag
    if weekday >= 5:  # Sat/Sun
        session_date = prev_business_day(now_et.date())
        return session_date, False

    # Weekday
    if now_et < cutoff:
        # Before close+10m -> use previous business day; tag MARKET_NOT_CLOSED
        session_date = prev_business_day(now_et.date())
        return session_date, True

    # After close+10m -> use today's session; no tag
    return now_et.date(), False

now_et = datetime.now(NY).replace(microsecond=0)
session_date, need_market_not_closed = compute_session_date_and_status(now_et)

# Labels for prompt
today_label = now_et.strftime("%Y-%m-%d")         # the actual current date
session_label = session_date.strftime("%Y-%m-%d") # the session we want data for

# -----------------------
# Prompt
# -----------------------

response = client.responses.create(
    model="gpt-4o-mini",
    tools=[{"type": "web_search"}],
    input=f"""
You are a meticulous market data runner.

Inputs
- session_date (America/New_York): {session_label}
- now_et: {today_label} {now_et.strftime("%H:%M:%S")}
- TICKER LIST (preserve order; do not add/remove): {viral_stocks_content}

Task
Return the **regular-session percent change for session_date** for each input ticker. Use the exact company names and tickers as written in the input; do not normalize names.

Hard rules
- Use the **{session_label}** session’s official close % (NOT intraday).
- Exchange time zone: America/New_York.
- Early-close days exist (1:00pm ET), but you still report that day’s official close %.
- Only output `DATA_NOT_FOUND` if BOTH primary and fallback sources fail (network or page not found is not a failure—try the fallback).
- Do NOT output Friday’s % for a different date; **the session_date is already correct**.

Search & verification order (per ticker)
1) Google Finance quote page:
   - Query: site:google.com/finance "TICKER" quote
   - Accept either an explicit “% at close” for {session_label}, or derive % from “Previous close” vs. “Close” values for {session_label} (if the page shows a date context).
2) If Google is inconclusive: **Yahoo Finance Historical Data** row for {session_label}.
   - Open: site:finance.yahoo.com "TICKER" Historical Data
   - From the daily table, find the row whose DATE equals **{session_label}** (US format is fine). Use:
       prev_close = Adj Close (previous trading day row)
       close = Adj Close (row for {session_label})
       pct = round(100*(close - prev_close)/prev_close, 2)
   - If Adj Close isn’t present, use Close.
3) If the Historical table paginates, use search to open a version that shows the **daily table** and scroll (do NOT give up after one attempt).
4) Only if both fail after reasonable attempts: `DATA_NOT_FOUND`.

Ambiguity
- If a ticker has multiple listings, prefer the U.S. primary listing.
- Tickers like OPEN, META, GME, TSLA, NVDA, AAPL, AMZN, NFLX are all U.S. primary—do not return `DATA_NOT_FOUND` for these unless the historical table is truly missing the date.

Computation & rounding
- pct_change = round(100*(close_{session_date} - close_prev_day)/close_prev_day, 2)
- Include a leading +/− sign.

Output format (STRICT; one line per INPUT ticker; SAME ORDER; no blanks, no extra text):
- When found: `Company Name (TICKER) ±X.XX%`
- If (and only if) both sources fail: `Company Name (TICKER) DATA_NOT_FOUND`

Now produce the lines for {session_label}.
"""
)
output_text = response.output_text.strip()
with open("test_prompts/stock_movement_prompt/output.txt", "w", encoding="utf-8") as f:
    f.write(output_text)

print("Stock Movement Output Generated!")