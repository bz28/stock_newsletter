from dotenv import load_dotenv
import os 
from openai import OpenAI

# load API keys
load_dotenv()
gpt_api_key = os.environ.get('GPT_API_KEY')

# initialize API keys
client = OpenAI(api_key = gpt_api_key)

# Path to the buzz output file
file_path = "test_prompts/buzz_prompt/output.txt"

# Read the content
with open(file_path, "r", encoding="utf-8") as f:
    buzz_content = f.read()

# Prompts
response = client.responses.create(
    model="gpt-4o-mini",
    tools = [{"type": "web_search"}],
    input =
        f"""
        Given {buzz_content}, search the web for each of the top 10 stocks in this report.
        Your response must include:
        - Why the stock is viral
        - Quick stats including P/E ratio, short interest, and divided yield
        - Takeaway
        Limit your entire response to at most 1000 words.
        """
)

output_text = response.output_text.strip()
with open("test_prompts/stock_movement_prompt/output.txt", "w", encoding="utf-8") as f:
    f.write(output_text)

print("Output generated")



# generate pros and cons based on articles