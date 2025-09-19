from dotenv import load_dotenv
import os 
from openai import OpenAI
import datetime

# load API keys
load_dotenv()
gpt_api_key = os.environ.get('GPT_API_KEY')

# initialize API keys
client = OpenAI(api_key = gpt_api_key)

# read stock movement output
file_path = "test_prompts/key_catalyst_prompt/output.txt"
with open(file_path, "r", encoding="utf-8") as f:
    key_catalyst_content = f.read()

date = datetime.date.today()

# prompts
response = client.responses.create(
    model="gpt-4o-mini",
    tools = [{"type": "web_search"}],
    input =
        f"""
        Create a list of the 10 stocks mentioned in {key_catalyst_content}, only keeping track of each stock's name.

        For each stock in the list created, create a report including only these specific requirements:
            1. All information provided must be from the past day, including sources and stats.
            2. Summarize the most important cultural or sentiment signals from chatter on social media like Reddit, Twitter/X, and TikTok, including social mention counts, limiting to 50 words.
            3. Title this section "Buzz"
            4. Do not change the content in {key_catalyst_content}, only add the new "Buzz" section to the existing content, where the format should be similar but not with the exact same information as:
                    1.  Nvidia (NVDA) +x%
                        Why: Earnings beat estimates by x percent on booming AI chip demand.
                        Buzz: +x% mentions on Reddit's r/stocks.
            5. Remember that all information, including sources and stats, must be from the past day. Remember todays date is {date}.
        
        The purpose of this section is to show the social temperature of the stock — hype, panic, or meme status.
        """
)


output_text = response.output_text.strip()
with open("test_prompts/buzz_prompt/output.txt", "w", encoding="utf-8") as f:
    f.write(output_text)

print("Buzz Output Generated")
