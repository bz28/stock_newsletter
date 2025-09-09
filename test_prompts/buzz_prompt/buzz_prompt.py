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
        Briefly mention the reason behind each stock's virality, limiting to 30 words per stock.
        Limit your entire response to at most 500 words.
        """
)

output_text = response.output_text.strip()
with open("test_prompts/buzz_prompt/output.txt", "w", encoding="utf-8") as f:
    f.write(output_text)

print("Output generated")