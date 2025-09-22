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
# read viral stocks output
file_path = "test_prompts/stock_movement_prompt/output.txt"
with open(file_path, "r", encoding="utf-8") as f:
    stock_movement_context = f.read()

response = client.responses.create(
    model="gpt-4o-mini",
    tools=[{"type": "web_search"}],
    input=f"""
            For each stock mentioned in {stock_movement_context}, append a new **"Why"** line that meets ALL rules:

            DATA FRESHNESS
            - Today's date is {date}. All information (stats + sources) must be within the **past 7 days**.
            - Prefer **primary, timestamped** sources (company PR, SEC filing, earnings release, reputable news with visible date/time).
            - If no timestamped primary source exists, you may use an official platform post (X/Reddit/TikTok) that clearly falls in-window.
            - If still none, don't include the stock in the output.

            NO SPECULATION
            - **Ban** words/phrases: "likely", "possibly", "could be", "investor sentiment", "market volatility", "no major news" (unless paired with the fallback above).
            - Provide a concrete catalyst type from this whitelist when applicable: earnings, guidance, rating/price-target change, regulatory, product launch, partnership, recall, M&A, litigation, macro data, outage/incident, leadership change, buyback/dividend, unusual volume/options (with a timestamped source).

            FORMAT & LENGTH
            - Do not modify any existing text in {stock_movement_context}. Only append a single **Why** line under each listed stock.
            - Max **30 words** per Why line.
            - Include exactly **one** citation with domain and the article/post **date (UTC)** in parentheses at end, e.g.:
            Why: Rating cut to Neutral on margin risk. (reuters.com, 2025-09-18 UTC)
            - Entire response ≤ **300 words** total.

            EXAMPLE (structure only):
            1. Nvidia (NVDA) +x%
            Why: Beat EPS and raised FY guide on AI demand. (investor.nvidia.com, 2025-09-17 UTC)

            Now produce the Why lines for every stock present in {stock_movement_context}. If a stock lacks a verified, timestamped source in-window, use the fallback exactly as specified.
            """
)
output_text = response.output_text.strip()
with open("test_prompts/key_catalyst_prompt/output.txt", "w", encoding="utf-8") as f:
    f.write(output_text)

print("Key Catalyst Output Generated!")