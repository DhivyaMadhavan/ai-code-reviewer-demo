import os
import sys
from openai import OpenAI

# 1. Capture the pre-extracted diff content from the runner environment
PR_DIFF_CONTENT = os.getenv("PR_DIFF") 

# 2. Configure target Model, Base URL, and the injected secret key
MODEL_ID = "openai.gpt-oss-safeguard-120b" 
CUSTOM_BASE_URL = "https://bedrock-runtime.ap-south-1.amazonaws.com/openai/v1"
SECRET_KEY = os.getenv("BEDROCK_SECRET_KEY")

def analyze_diff_with_openai_sdk(diff_content):
    """Sends the pre-extracted git diff to the Bedrock OpenAI gateway."""
    
    if not SECRET_KEY:
        print("Error: BEDROCK_SECRET_KEY environment variable is missing.", file=sys.stderr)
        sys.exit(1)
        
    print(f"Invoking Bedrock gateway endpoint at: {CUSTOM_BASE_URL}...")
    
    # Initialize using your mapped secret token key natively
    client = OpenAI(
        base_url=CUSTOM_BASE_URL,
        api_key=SECRET_KEY
    )
    
    system_prompt = (
        "Review the code as a senior software engineer. Always respond in English. "
        "Focus heavily on:\n"
        "- Security vulnerabilities\n"
        "- Bugs and correctness issues\n"
        "- Error handling\n"
        "- Performance issues\n"
        "- Maintainability\n\n"
        "Provide concise, specific, and highly actionable review comments using clear GitHub Markdown formatting."
    )
    
    try:
        response = client.chat.completions.create(
            model=MODEL_ID,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Please review this code change diff:\n\n```diff\n{diff_content}\n```"}
            ],
            temperature=0.2,
            max_tokens=2048
        )
        
        # Stream text directly out to the runner's standard console pipeline
        print(response.choices.message.content)
        
    except Exception as e:
        print(f"Endpoint Invocation Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    analyze_diff_with_openai_sdk(PR_DIFF_CONTENT)
