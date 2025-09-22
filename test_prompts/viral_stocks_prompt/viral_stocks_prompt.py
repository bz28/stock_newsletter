from dotenv import load_dotenv
import os 
from openai import OpenAI
from datetime import datetime, timedelta, timezone
import zoneinfo


# load API keys
load_dotenv()
gpt_api_key = os.environ.get('GPT_API_KEY')

# initialize API keys
client = OpenAI(api_key = gpt_api_key)

PT = zoneinfo.ZoneInfo("America/Los_Angeles")
window_end = datetime.now(PT).replace(microsecond=0)
window_start = window_end - timedelta(hours=24)
date_label = window_end.strftime("%Y-%m-%d")

response = client.responses.create(
    model="gpt-4o-mini",
    tools=[{"type": "web_search"}],
    input=f"""
        You are ranking viral **publicly traded common stocks** for the past 24 hours.

        Primary window (strict):
        - Start: {window_start.astimezone(timezone.utc).isoformat()} UTC
        - End:   {window_end.astimezone(timezone.utc).isoformat()} UTC

        Retrieval:
        - Use web_search with a recency focus on the last 2 days.
        - Prefer sources with visible timestamps. If a page has no timestamp but is an **official platform artifact** (a Reddit/X/TikTok post URL) created within the window, accept it.
        - Accept reputable aggregators that report **platform-linked** items (e.g., SwaggyStocks, ApeWisdom, QuiverQuant) **only as corroboration**, not as the sole source.

        Eligibility:
        - Only listed stocks (no ETFs/crypto/private/index, like SPY). Resolve ticker ↔ company (US primary listing if ambiguous).
        - Each candidate needs ≥1 primary citation within the window (a platform post or a timestamped article) OR ≥2 secondary aggregator citations that each link out to primary posts.

        Signals (compute where available; if unavailable, use 0 for that signal—do **not** discard the candidate):
        - Mentions: count across Reddit/X/TikTok/news within the window.
        - Engagement: likes/comments/shares/reposts for sample posts in the window.
        - Velocity: change rate vs earlier items within the same window (or steepness over time in the window).
        - Search Interest: Google Trends or equivalent in the window (if missing → 0).
        - Trading Buzz: unusual options or share volume cited by reputable sources in the window (if missing → 0).

        Scoring:
        - Normalize each available signal to 0-1 per candidate.
        - Virality score = mean of available signals (ignore missing ones rather than forcing 0 if this would make everything 0).
        - Tie-breakers: higher velocity, then higher engagement.

        Output rules (strict):
        - Return only a ranked list, one per line: `1. TICKER — Company Name`
        - Exactly top 25 if possible; otherwise return as many as qualify (≥5). No prose, no dates, no citations.
        - Deduplicate by issuer (e.g., keep GOOGL over GOOG if both appear).
        - Exclude entries without any supporting evidence found.

        Now produce the list for the past 24 hours ending {date_label}.
        """
)
output_text = response.output_text.strip()
with open("test_prompts/viral_stocks_prompt/output.txt", "w", encoding="utf-8") as f:
    f.write(output_text)

print("Viral Stocks Output Generated!")