from dotenv import load_dotenv
import os 
from openai import OpenAI

# load API keys
load_dotenv()
gpt_api_key = os.environ.get('GPT_API_KEY')

# initialize API keys
client = OpenAI(api_key = gpt_api_key)

# read buzz output
file_path = "test_prompts/buzz_prompt/output.txt"
with open(file_path, "r", encoding="utf-8") as f:
    buzz_content = f.read()

# prompts
response = client.responses.create(
    model="gpt-4o-mini",
    tools=[{"type": "web_search"}],
    input=f"""
Goal: For each stock mentioned (exactly those in {buzz_content}, original order), append a new "Quick Stat" line to the end of its entry. Do not alter any existing text.

Data freshness policy:
- "Buzz" in {buzz_content} may be ≤24h, but "Quick Stat" uses the latest reliable snapshot (NOT necessarily ≤24h).
- Fundamental/technical "Quick Stat" is acceptable if the source clearly shows a date within the last 12 months.
- For short interest (which is biweekly), accept the latest published date.

Allowed metrics:
1) P/E (ttm or forward) 
2) EPS (ttm)
3) Dividend yield (%)
4) Short interest (% of float or shares short as % of float) — include the "as of" date
5) Price-to-Sales (ttm)
6) Expense ratio (for ETFs only)

Allowed sources (prefer in this order; use at least one):
- Company IR or SEC (10-K/10-Q/earnings release)
- Nasdaq.com, NYSE.com
- Yahoo Finance (finance.yahoo.com), Morningstar, FT Markets, LSEG/Refinitiv, S&P Global, MarketWatch profile page
- FINRA or exchange short interest pages

If a metric differs slightly across sources, prefer the more authoritative (SEC/IR > exchange > major finance portals). Include the **as-of date** that the source shows (quarter-end, filing date, “as of” label, etc.).

STRICT OUTPUT FORMAT (exactly one line per stock, appended to its existing entry):
Quick Stat: [Metric Name] = [Value][, optional benchmark/context] (as of YYYY-MM-DD; source: domain.tld).

Examples:
Quick Stat: P/E (ttm) = 22.4 (market avg ~24.5) (as of 2025-09-19; source: finance.yahoo.com).
Quick Stat: Short interest = 15.2% of float (as of 2025-09-13; source: nasdaq.com).
Quick Stat: Dividend yield = 2.75% (as of 2025-09-20; source: marketwatch.com).

Fallback rules (MANDATORY):
- You MUST attempt sources in the allowed list until one metric is found following the order above.
- Only if you cannot verify ANY metric from ANY allowed source, output exactly:
  Quick Stat: No verified metric available (after checking allowed sources).
- Do NOT use "past 7d" language. Do NOT omit the (as of YYYY-MM-DD; source: …) tail when a metric is present.

Formatting & scope:
- Keep every original heading/Why/Buzz line in {buzz_content} unchanged.
- Append exactly one "Quick Stat:" line under each stock.
- Preserve the original list length (exactly those 10 stocks in {buzz_content}, no additions/deletions).
"""
)
output_text = response.output_text.strip()
with open("test_prompts/quick_stat_prompt/output.txt", "w", encoding="utf-8") as f:
    f.write(output_text)

print("Quick Stat Output Generated")
