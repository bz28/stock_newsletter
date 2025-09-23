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

STRICT CONSTRAINTS
- Do NOT add any extra sections, headers, bullet lists, notes, or text outside of {buzz_content}.
- Do NOT add a preamble or quote block.
- Your ONLY change: append exactly one "Quick Stat:" line under each stock row in the table.

THEME → METRIC (ALIGNMENT FIRST)
Pick ONE metric that directly supports the stock’s "Why". Use this priority per theme. If the Why matches multiple themes, use the first matching theme.
1) Earnings/beat/miss/guidance/profitability → choose one of:
   • EPS (TTM or most recent quarter; label clearly as TTM or Q# FY#), OR
   • Revenue YoY %, OR
   • Operating margin % (or Gross margin %), OR
   • EPS surprise vs consensus (% or $) if explicitly available.
   — Do NOT use raw Net income in $ for this theme. If you use net income, it must be **YoY % change**, not an absolute $.
2) Valuation/rerating/multiple talk → P/E (label ttm/forward), EV/Sales, EV/EBITDA, Price/Book, PEG, FCF yield % (label).
3) Dividend/capital return → Dividend yield %, Payout ratio %, 5y dividend CAGR %.
4) Short squeeze/positioning → Short interest % of float (with “as of” date), Days-to-cover, Utilization %, Borrow fee %.
5) Topline demand/scale → Revenue YoY %, ARR (with period), Bookings growth %, Backlog (only if **explicitly mentioned** in Why and ≤12 months old).
6) Technical/price action → 50-DMA/200-DMA distance %, RSI, Beta, Avg daily volume, ATR (label).

If no theme match is clear, pick any **verifiable** metric that increases variety (avoid EPS if used for the prior stock and not forced by theme).

VARIETY (WITHOUT BREAKING ALIGNMENT)
- Do not output **EPS** for more than two stocks in a row unless the Why for each clearly centers on earnings.
- When multiple aligned metrics are available, prefer one not used for the previous stock.

FRESHNESS RULES
- Quarterly/earnings metrics: use **MRQ** or the most recent official quarter. If MRQ not available, the immediately prior quarter. Include period .
- Annual TTM/ratio metrics: OK if clearly labeled (e.g., “TTM”).
- Short interest: latest published date .
- Segment/product metrics (e.g., iPhone revenue, cloud revenue): only if (a) segment is referenced in the **Why**, and (b) the period is **≤ 12 months** old. Otherwise, reject and pick another aligned metric.
- Reject stale metrics older than allowed windows above.

SOURCE RULES
- Allowed sources (priority): Company IR/SEC filings (10-K/10-Q/8-K/ER/presentation/fact sheet) → Exchange/FINRA → Nasdaq.com/NYSE.com → Major finance portals (Yahoo Finance, Morningstar, FT Markets, LSEG/Refinitiv, S&P Global, MarketWatch).
- **Do NOT use Macrotrends** or blogs/wiki/unsourced aggregators.
- Include the source name and period/date. Never invent numbers. If you cannot verify, use the fallback.

FALLBACK (MANDATORY)
- If no compliant metric is found after checking credible sources: 
  Quick Stat: No verified metric available (after checking credible sources).

OUTPUT FORMAT (one line per stock, appended directly under its row)
- Quick Stat: [Metric Name] = [Value][ unit/label ].
- Examples:
  Quick Stat: EPS (MRQ) = $2.31 .
  Quick Stat: Revenue YoY = +21.0% .
  Quick Stat: P/E (ttm) = 30.3× .
  Quick Stat: Short interest = 12.9% of float.

SELF-CHECK BEFORE FINALIZING (REQUIRED)
For each stock, verify:
- Alignment: the chosen metric matches the Why theme above (earnings theme must NOT use raw net income $).
- Freshness: period/date satisfies the windows; segment stats ≤12 months and only if segment appears in Why.
- Source: allowed + included in the line; no Macrotrends.
- Variety: not producing EPS for 3+ consecutive stocks unless Why forces it.

If any check fails, select a different compliant metric and revalidate before output.

Now process {buzz_content} strictly under these rules and append one "Quick Stat" line per stock.
"""
)

output_text = response.output_text.strip()
with open("test_prompts/quick_stat_prompt/output.txt", "w", encoding="utf-8") as f:
    f.write(output_text)

print("Quick Stat Output Generated")
