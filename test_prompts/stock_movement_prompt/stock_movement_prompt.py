from dotenv import load_dotenv
import os 
from openai import OpenAI

# load API keys
load_dotenv()
gpt_api_key = os.environ.get('GPT_API_KEY')

# initialize API keys
client = OpenAI(api_key = gpt_api_key)

# prompts
response = client.responses.create(
    model="gpt-4o-mini",
    tools = [{"type": "web_search"}],
    input =
        """
        Scan reputable articles regarding Tiktok, Reddit, and X stock mentions from the past week.
        Determine the top 10 trending stocks aggregated from all three social media platforms (Tiktok, Reddit, and X).

        Your output must follow these specific requirements:
            1. All information provided must be from the past week, including sources and stats.
            2. Mention the stock movement percentage, calculate using "Bloomberg Market News".
            3. Briefly summarize the key catalyst (e.g., earnings beat, recall, product launch) behind each stock's price movement. Title this section "why", limiting to 30 words per stock.
            4. Limit your entire response to at most 300 words.
            5. Format should be similar but not with the exact same information as:
                    1.  Nvidia (NVDA) +6.2%
                        Why: Earnings beat estimates by 12 percent on booming AI chip demand.
            6. Remember that all information, including sources and stats, must be from the past week.
                
        The purpose of this section is to give the reader immediate context so they aren't just seeing numbers in a vacuum.
        """
)

output_text = response.output_text.strip()
with open("test_prompts/stock_movement_prompt/output.txt", "w", encoding="utf-8") as f:
    f.write(output_text)

print("Stock Movement Output Generated!")