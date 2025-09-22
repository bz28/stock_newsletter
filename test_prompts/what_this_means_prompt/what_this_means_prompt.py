from dotenv import load_dotenv
import os 
from openai import OpenAI
import datetime

# load API keys
load_dotenv()
gpt_api_key = os.environ.get('GPT_API_KEY')

# initialize API keys
client = OpenAI(api_key = gpt_api_key)
date = datetime.date.today()

# read buzz output
file_path = "test_prompts/quick_stat_prompt/output.txt"
with open(file_path, "r", encoding="utf-8") as f:
    quick_stat_content = f.read()

# prompts
response = client.responses.create(
    model="gpt-4o-mini",
    tools=[{"type": "web_search"}],
    input=f"""
Task
- From {quick_stat_content}, identify exactly 10 stocks (preserve order of appearance).
- Output only those 10 stocks with the original content preserved.
- Do not include any extra stocks, commentary, or prose.

Data Freshness
- Today's date is {date}.
- All information (catalysts, buzz, stats, sources) must be from the **past 24 hours**.
- If no verifiable past-24h source exists for a stock, exclude it from the output.

Formatting
- Do not alter any existing text in {quick_stat_content}.
- For each included stock, append two new sections in this order:
  What This Means: Write 1–2 plain-English sentences connecting the Why, Buzz, and Quick Stat into a clear investor takeaway.

Rules
- No speculation words: "likely", "possibly", "could be", "general sentiment".
- Each What This Means must be ≤40 words.
- Do not produce a new table or summary; only modify the existing stock entries.
- The final output must contain exactly 10 stocks with appended What This Means sections.

Example (structure only):
Nvidia (NVDA) +x%
Why: Earnings beat estimates by x percent on booming AI chip demand. (investor.nvidia.com, 2025-09-20 UTC)
Buzz: +200% Reddit mentions. (swaggystocks.com, 2025-09-21 UTC)
Quick Stat: P/E = 45 (market avg ~20).
What This Means: Strong AI demand and elevated valuation show investors are willing to pay a premium for growth.

Now, return the 10 stocks from {quick_stat_content} updated with What This Means as specified.
"""
)

output_text = response.output_text.strip()
with open("test_prompts/what_this_means_prompt/output.txt", "w", encoding="utf-8") as f:
    f.write(output_text)

print("What This Means Output Generated")
