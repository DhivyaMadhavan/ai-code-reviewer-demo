import os
import sys
import requests

PR_DIFF_CONTENT = os.getenv("PR_DIFF")

def analyze_diff_with_native_bedrock(diff_content):
    print("Invoking Bedrock Runtime endpoint via HTTPS (OpenAI-compatible)...")

    base_url = os.environ["BEDROCK_BASE_URL"]   
    api_key = os.environ["BEDROCK_API_KEY"]

    system_prompt = """
        You are a senior software engineer reviewing a code diff.
        
        Respond in English using concise Markdown.
        
        Rules:
        - Report only real issues. Do not invent problems.
        - Ignore style nitpicks unless they impact maintainability.
        - Focus on Security, Bugs, Error Handling, Performance, and Maintainability.
        - Use at most 5 findings.
        - For each finding provide:
          - Severity: Critical, Major, or Minor
          - Issue
          - Fix
        - Keep each finding to 1-2 sentences.
        - If no significant issues are found, say:
          'No major issues found. The changes look good.'
        
        Output format:
        
        ## Findings
        
        - [Major] Issue: ...
          Fix: ...
        
        - [Minor] Issue: ...
          Fix: ...
        
        ## Summary
        One sentence overall assessment.
        """  

    headers = {
        "Authorization": f"Bearer {api_key.strip()}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai.gpt-oss-safeguard-120b",  
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Review this diff:\n```diff\n{diff_content}\n```"}
        ]
    }

    try:
        resp = requests.post(f"{base_url}/chat/completions", headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()         
        
        # Extract the text depending on schema
        if "choices" in data and len(data["choices"]) > 0:
            review_text = data["choices"][0]["message"]["content"]
        else:
            review_text = "No review generated."

        print(review_text)

    except Exception as e:
        print(f"Native HTTPS Invocation Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    analyze_diff_with_native_bedrock(PR_DIFF_CONTENT)
