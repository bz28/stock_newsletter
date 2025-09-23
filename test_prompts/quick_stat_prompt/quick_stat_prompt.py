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

STRICT CONSTRAINTS:
- Do NOT add any extra sections, headers, bullet lists, summaries, or text outside of {buzz_content}.
- Do NOT add a preamble, company profile, or market quote block.
- Do NOT add any notes or disclaimers after the table.
- Your ONLY modification: append exactly one "Quick Stat:" line under each stock row in the table.

## Metric Selection Logic (IMPORTANT)
Step A — Align to "Why":
- If the stock’s **Why** mentions or implies one of these themes, choose the corresponding metric:

  • Earnings beat/miss, EPS guidance, profitability, buybacks that affect EPS  →  **EPS** (ttm or most recent fiscal; show period if given)
  • Valuation call (upgrade/downgrade on multiple, “rich/cheap,” “re-rating,” price target based on multiples)  →  **P/E** (or forward P/E if clearly labeled by source)
  • Dividend news (initiation, increase, ex-date, yield commentary)  →  **Dividend yield (%)**
  • Short squeeze, heavy shorting, borrow fees, high days-to-cover  →  **Short interest (% of float)**  (include the “as of” date)
  • Revenue growth / topline focus, “early-stage scale,” “sales multiple,” product demand without profit focus  →  **Price-to-Sales**

- If multiple themes apply, use the **first matching** in the list above.

Step B — If no theme matches:
- Randomly pick **one** metric from the allowed set, but **promote variety** across the list:
  • Prefer a metric not yet used for prior stocks in this run.
  • Do not repeat the same metric more than twice in a row unless Step A forces it.

## Allowed metrics (choose exactly one):
1) P/E 
2) EPS 
3) Dividend yield (%)
4) Short interest (%)
5) Price-to-Sales

## Data Freshness Policy
- "Buzz" in {buzz_content} may be ≤24h, but "Quick Stat" uses the latest reliable snapshot (NOT necessarily ≤24h).
- Fundamental/technical "Quick Stat" is acceptable if the source clearly shows a date within the last 12 months.
- For short interest (biweekly), accept the latest published date and include it.

## Allowed Sources (prefer in this order; use at least one):
- Company IR or SEC (10-K/10-Q/earnings release)
- Nasdaq.com, NYSE.com
- Yahoo Finance (finance.yahoo.com), Morningstar, FT Markets, LSEG/Refinitiv, S&P Global, MarketWatch profile page
- FINRA or exchange short interest pages

If a metric differs slightly across sources, prefer the more authoritative (SEC/IR > exchange > major finance portals).

## Fallback (MANDATORY)
- You MUST try sources in the allowed list (in priority order) until one metric is verified.
- Only if **no** metric can be verified from **any** allowed source, output exactly:
  Quick Stat: No verified metric available (after checking allowed sources).

## Strict Output Format
- Append **exactly one line** per stock, directly under its existing entry:
  Quick Stat: [Metric Name] = [Value].
- Examples:
  Quick Stat: P/E = 22.4.
  Quick Stat: Short interest = 15.2%.
  Quick Stat: Dividend yield = 2.75%.

## Formatting & Scope
- Keep every original heading/Why/Buzz line in {buzz_content} unchanged.
- Preserve the original list length (exactly those stocks in {buzz_content}, same order, no additions/deletions).
- Do NOT use “past 7d” language; include explicit “as of” date only where required (short interest).

Now process {buzz_content} using the rules above and append one "Quick Stat" line per stock.
"""
)

output_text = response.output_text.strip()
with open("test_prompts/quick_stat_prompt/output.txt", "w", encoding="utf-8") as f:
    f.write(output_text)

print("Quick Stat Output Generated")
