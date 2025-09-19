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
        Scan reputable articles regarding Tiktok, Reddit, and X stock mentions from the past day.
        Identify the top 10 most viral stocks in the past 24 hours across social media platforms like Reddit, X, and Tiktok. Todays date is {date}.

        For each stock, consider:
        - Mentions: Frequency of discussion across Reddit, X (Twitter), TikTok, and news.
        - Engagement: Likes, comments, shares, and repost ratios on these mentions.
        - Velocity: Speed of growth in mentions and engagement (sudden spikes).
        - Search Interest: Google Trends or equivalent search data changes.
        - Trading Buzz: Unusual trading activity (options spikes, abnormal volume).

        Only output a list of the name of the top 10 most viral stocks in the past 24 hours from todays date, {date}, ranked by overall virality, nothing else.   
        """
)

output_text = response.output_text.strip()
with open("test_prompts/viral_stocks_prompt/output.txt", "w", encoding="utf-8") as f:
    f.write(output_text)

print("Viral Stocks Output Generated!")