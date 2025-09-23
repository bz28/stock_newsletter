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
        3. Do not change any information in {education_bite_context}
        4. Do not include any information that is not in {education_bite_context}
        5. The headline should be catchy and short, namedropping and mentioning 2-3 stocks in {education_bite_context}, focused on the content in the buzz section in {education_bite_context}, specifically social media... similar to the format in these:
            - 👀 Tesla’s Mentions Jump 50%, NVIDIA AI Buzz +35%, Netflix Chatter Drops 25%
            - 👀 Tesla surges, NVIDIA steady, Netflix slides — here’s what matters today
            - TikTok Can’t Stop Talking About Tesla, NVIDIA’s AI Mentions Spike, Netflix Fades — Here’s Why
            - Tesla’s Blowing Up on TikTok, NVIDIA’s Hot, Netflix Not
        6. The newsletter must contain and dicuss all 5 stocks
        7. Must include all 5 sections of why, buzz, quick stat, what this means, and education bite
        7. Add this hyperlinked feedback form to the bottom of the email: https://docs.google.com/forms/d/e/1FAIpQLSdg5fh8xNHfpQcksArIT2la8I60U6FCs8R83hG7jJPkRZzG8w/viewform .
        8. The output should only contain the html code
        """
)


output_text = response.output_text.strip()
with open("test_prompts/email_formatting_prompt/output.html", "w", encoding="utf-8") as f:
    f.write(output_text)

print("Email Formatting Output Generated")
