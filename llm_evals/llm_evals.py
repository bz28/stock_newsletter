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
file_path = "test_prompts/education_bite_prompt/output.txt"
with open(file_path, "r", encoding="utf-8") as f:
    newsletter_content = f.read()

date = datetime.date.today()

# prompts
response = client.responses.create(
    model="gpt-4o-mini",
    tools = [{"type": "web_search"}],
    input =
        f"""
        Task: Verify all the information in {newsletter_content} is accurate.
        Resources: Use web search to verify the information.
        Output: What is accurate, inacurrate, or not certain, evaluating section by section.
        """
)


output_text = response.output_text.strip()
with open("llm_evals/output.txt", "w", encoding="utf-8") as f:
    f.write(output_text)

print("LLM Eval Generated")
