from dotenv import load_dotenv
import os 
from openai import OpenAI

# load API keys
load_dotenv()
gpt_api_key = os.environ.get('GPT_API_KEY')

# initialize API keys
client = OpenAI(api_key = gpt_api_key)

# read buzz output
file_path = "test_prompts/what_this_means_prompt/output.txt"
with open(file_path, "r", encoding="utf-8") as f:
    what_this_means_content = f.read()

# prompts
response = client.responses.create(
    model="gpt-4o-mini",
    tools = [{"type": "web_search"}],
    input =
        f"""
        Goal: For each stock mentioned (exactly those in {what_this_means_content}, original order), append a new "Education bite" line to the end of its entry. Do not alter any existing text.
       
        STRICT CONSTRAINTS
        - Do NOT add any extra sections, headers, bullet lists, notes, or text outside of {what_this_means_content}.
        - Do NOT add a preamble or quote block.
        - Your ONLY change: append exactly one "Education Bite:" line under each stock row in the table.

        Follow these rules:
            1. All information provided must be from the past day, including sources and stats.
            2. Create a short, max 20 word explainer of one key concept that is mentioned for the specific stock (EPS, P/E, guidance, short interest, dividend yield, etc.).
            3. Title this section "Education Bite"
            4. Do not change the content in {what_this_means_content}, only add the new "Quick Stat" section to the existing content, where the format should be similar but not with the exact same information as:
                    1.  Nvidia (NVDA) +x%
                        Why: Earnings beat estimates by x percent on booming AI chip demand.
                        Buzz: +x% mentions on Reddit's r/stocks.
                        Quick Stat: P/E = x.
                        What This Means: Investors are paying a premium for growth.
                        Education Bite: “P/E ratio” = Price/Earnings → how much investors pay per $1 of profit.
            5. Remember that all information, including sources and stats, must be from the past day.
        
        The purpose of this section is to define a key fundamental or technical fact in elementary terms.
        """
)


output_text = response.output_text.strip()
with open("test_prompts/education_bite_prompt/output.txt", "w", encoding="utf-8") as f:
    f.write(output_text)

print("Education Bite Output Generated")
