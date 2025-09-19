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
file_path = "test_prompts/viral_stocks_prompt/output.txt"
with open(file_path, "r", encoding="utf-8") as f:
    viral_stocks_content = f.read()

# prompts
response = client.responses.create(
    model="gpt-4o-mini",
    tools = [{"type": "web_search"}],
    input =
        f"""
        Create a list of the 10 stocks mentioned in {viral_stocks_content}, only keeping track of each stock's name.

        For each stock in the list created, create a report including only these specific requirements:
            1. All information provided must be from the past week, including sources and stats, todays date is {date}.
            2. Determine the stock price change for the past day using https://www.google.com/finance/beta. Only display the percentage change.
            3. Briefly summarize the key catalyst (e.g., earnings beat, recall, product launch) behind each stock's price movement. Title this section "why", limiting to 30 words per stock.
            4. Limit your entire response to at most 300 words.
            5. Format should be similar but not with the exact same information as:
                    1.  Nvidia (NVDA) +x%
                        Why: Earnings beat estimates by x percent on booming AI chip demand.
            6. Remember that all information, including sources and stats, must be from the past day. Remember todays date is {date}.
                
        The purpose of this section is to give the reader immediate context so they aren't just seeing numbers in a vacuum.
        """
)

output_text = response.output_text.strip()
with open("test_prompts/stock_movement_prompt/output.txt", "w", encoding="utf-8") as f:
    f.write(output_text)

print("Stock Movement Output Generated!")