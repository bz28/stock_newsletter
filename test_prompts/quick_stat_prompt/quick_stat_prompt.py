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
    tools = [{"type": "web_search"}],
    input =
        f"""
        Create a list of the 10 stocks mentioned in {buzz_content}, only keeping track of each stock's name.

        For each stock in the list created, create a report including only these specific requirements:
            1. All information provided must be from the past week, including sources and stats.
            2. Discuss one digestible number that matters (P/E ratio, EPS, dividend yield, short interest).
            3. Title this section "Quick Stat"
            5. Add this section to the existing format in {buzz_content}, where the format should be similar but not with the exact same information as:
                    1.  Nvidia (NVDA) +6.2%
                        Why: Earnings beat estimates by 12 percent on booming AI chip demand.
                        Buzz: +40% mentions on Reddit's r/stocks.
                        Quick Stat: P/E = 45 (market avg ~25).
            6. Remember that all information, including sources and stats, must be from the past week.
        
        The purpose of this section is to drop a key fundamental or technical fact, without overwhelming.
        """
)


output_text = response.output_text.strip()
with open("test_prompts/quick_stat_prompt/output.txt", "w", encoding="utf-8") as f:
    f.write(output_text)

print("Quick Stat Output Generated")
