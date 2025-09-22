from dotenv import load_dotenv
import os 
from openai import OpenAI

# load API keys
load_dotenv()
gpt_api_key = os.environ.get('GPT_API_KEY')

# initialize API keys
client = OpenAI(api_key = gpt_api_key)

# read buzz output
file_path = "test_prompts/quick_stat_prompt/output.txt"
with open(file_path, "r", encoding="utf-8") as f:
    quick_stat_content = f.read()

# prompts
response = client.responses.create(
    model="gpt-4o-mini",
    tools = [{"type": "web_search"}],
    input =
        f"""
        Create a list of the 10 stocks mentioned in {quick_stat_content}, only keeping track of each stock's name.

        For each stock in the list created, create a report including only these specific requirements:
            1. All information provided must be from the past day, including sources and stats.
            2. From only the information provided in {quick_stat_content}, create a 1 to 2 sentence plain-English takeaway that connects the catalyst, buzz, and stat into a conclusion.
            3. Title this section "What This Means"
            4. Do not change the content in {quick_stat_content}, only add the new "Buzz" section to the existing content, where the format should be similar but not with the exact same information as:
                    1.  Nvidia (NVDA) +x%
                        Why: Earnings beat estimates by x percent on booming AI chip demand.
                        Buzz: +x% mentions on Reddit's r/stocks.
                        Quick Stat: P/E = x (market avg ~y).
                        What This Means: Investors are paying a premium for growth.
            6. Remember that all information, including sources and stats, must be from the past day.
        
        The purpose of this section is to bridge the gap between raw data and actionable understanding.
        The output should only contain the 10 stocks.
        """
)


output_text = response.output_text.strip()
with open("test_prompts/what_this_means_prompt/output.txt", "w", encoding="utf-8") as f:
    f.write(output_text)

print("What This Means Output Generated")
