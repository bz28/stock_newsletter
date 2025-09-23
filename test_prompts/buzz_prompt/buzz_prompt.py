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
        For each stock in {key_catalyst_content}, create a report including only these specific requirements:
            1. {key_catalyst_content} contains exactly one Markdown table with columns:
                | Company Name (Ticker) | Percent Change | Why |
                Return **the same table** with an added **fourth column** named **Buzz** appended at the end.
                - Output **ONLY** the updated table. No headings, lists, or extra prose.
            2. The buzz section contains a summary of the most important cultural or sentiment signals from chatter on social media like Reddit, Twitter/X, and TikTok, including social mention counts, limiting to 10 words.
            3. Example:
                        Buzz: 12,000+ mentions on Reddit; AI enthusiasts are bullish. 


        The purpose of this section is to show the social temperature of the stock — hype, panic, or meme status.
        Only output the 5 most interesting stocks with buzz AND why.
        """
)


output_text = response.output_text.strip()
with open("test_prompts/buzz_prompt/output.txt", "w", encoding="utf-8") as f:
    f.write(output_text)

print("Buzz Output Generated")
