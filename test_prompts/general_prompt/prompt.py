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
        Scan reputable news articles on msft stock in the past week, including today. 
        Generate a short summary with a max of 300 words including:
        - Why the stock moved the direction it did
        - Buzz: Tiktok, reddit, x mentions, tailored to the younger generation
        - Stats: P/E ratio, short interest, dividend yield
        - Takeaway
        """
)

output_text = response.output_text.strip()
print(output_text)


