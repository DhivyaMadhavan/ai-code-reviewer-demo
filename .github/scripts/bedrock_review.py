import os
import sys
import requests

PR_DIFF_CONTENT = os.getenv("PR_DIFF")

def analyze_diff_with_native_bedrock(diff_content):
    print("Invoking Bedrock Runtime endpoint via HTTPS...")

    base_url = os.environ["BEDROCK_BASE_URL"]   # e.g. https://bedrock-runtime.YOUR_REGION.amazonaws.com/model/amazon.nova-pro-v1:0/invoke
    api_key = os.environ["BEDROCK_API_KEY"]     # stored in GitHub Secrets

    system_prompt = (
        "Review the code as a senior software engineer. Always respond in English. "
        "Focus on: Security vulnerabilities, Bugs, Error handling, Performance, and Maintainability."
    )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "modelId": "openai.gpt-oss-safeguard-120b",
        "inputText": f"{system_prompt}\n\nReview this diff:\n```diff\n{diff_content}\n```"
    }

    try:
        resp = requests.post(base_url, headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()

        # Adjust depending on the Bedrock model’s response format
        review_text = data.get("outputText", "No review generated.")
        print(review_text)

    except Exception as e:
        print(f"Native HTTPS Invocation Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    analyze_diff_with_native_bedrock(PR_DIFF_CONTENT)
