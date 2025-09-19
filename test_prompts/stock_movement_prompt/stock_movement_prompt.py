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
        For each stock listed in {viral_stocks_content}, create a report including only these specific requirements:
            1. All information provided must be from the past 24 hours, including sources and stats, todays date is {date}.
            2. Determine the stock price change on {date}, using https://www.google.com/finance/beta. Only display the percentage change. Make sure that the percent change for the stock on {date} is accurate.
            3. Format should be similar but not with the exact same information as:
                    1.  Nvidia (NVDA) +x%
            4. Remember that all information, including sources and stats, must be from the past day. Remember todays date is {date}.
        """
)

output_text = response.output_text.strip()
with open("test_prompts/stock_movement_prompt/output.txt", "w", encoding="utf-8") as f:
    f.write(output_text)

print("Stock Movement Output Generated!")