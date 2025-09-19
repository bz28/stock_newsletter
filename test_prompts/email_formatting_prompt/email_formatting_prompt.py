from dotenv import load_dotenv
import os 
from openai import OpenAI

# load API keys
load_dotenv()
gpt_api_key = os.environ.get('GPT_API_KEY')

# initialize API keys
client = OpenAI(api_key = gpt_api_key)

# read buzz output
file_path = "test_prompts/education_bite_prompt/output.txt"
with open(file_path, "r", encoding="utf-8") as f:
    education_bite_context = f.read()
# read email formatting html
email_format_template = "test_prompts/email_formatting_prompt/format_example.html"
with open(email_format_template, "r", encoding="utf-8") as f:
    email_formatting_template = f.read()


# prompts
response = client.responses.create(
    model="gpt-4o-mini",
    input =
        f"""
        Following the format in {email_formatting_template}, format all the content in {education_bite_context}.
        Follow these specific requirements:
        1. Remove the headers of Market Movers (Winners) and (Losers), instead putting all information in 1 big section.
        2. Include all the information in {education_bite_context}
        3. Do not include any information that is not in {education_bite_context}
        4. Replace the headline with a catchy short headline focused on buzz in {education_bite_context}, similar to the headline used in the formatting in {email_formatting_template}
        5. The output should only contain the html code
        """
)


output_text = response.output_text.strip()
with open("test_prompts/email_formatting_prompt/output.txt", "w", encoding="utf-8") as f:
    f.write(output_text)

print("Email Formatting Output Generated")
