import subprocess

files = [
    "test_prompts/viral_stocks_prompt/viral_stocks_prompt.py",
    "test_prompts/stock_movement_prompt/stock_movement_prompt.py",
    "test_prompts/key_catalyst_prompt/key_catalyst_prompt.py",
    "test_prompts/buzz_prompt/buzz_prompt.py",
    "test_prompts/quick_stat_prompt/quick_stat_prompt.py",
    "test_prompts/what_this_means_prompt/what_this_means_prompt.py",
    "test_prompts/education_bite_prompt/education_bite_prompt.py",
    "test_prompts/email_formatting_prompt/email_formatting_prompt.py",
]

for file in files:
    print(f"\n--- Running {file} ---\n")
    subprocess.run(["python3", file])