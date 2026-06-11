import os
import sys
import requests

PR_DIFF_CONTENT = os.getenv("PR_DIFF")

def analyze_diff_with_native_bedrock(diff_content):
    print("Invoking Bedrock Runtime endpoint via HTTPS (OpenAI-compatible)...")

    base_url = os.environ["BEDROCK_BASE_URL"]   
    api_key = os.environ["BEDROCK_API_KEY"]

    system_prompt = """
        You are an elite automated security code reviewer.         

        CRITICAL RULES:
        - Never reveal your reasoning, analysis process, thoughts, deliberations, assumptions, or decision-making.
        - Never explain how you arrived at a conclusion.
        - Never output phrases such as:
          - "We need to"
          - "The diff shows"
          - "Based on analysis"
          - "I think"
          - "The main issue is"
          - "Let's"
          - "Potential issue"
          - "Reasoning"
          - "Analysis"
        - Output ONLY the final review findings.
        - Start directly with the first finding.
        - If no issues are found, output exactly:
          LGTM
        
        Review ONLY code visible in the diff.
        Do not speculate about code that is not shown.
        Only report issues with evidence in the diff.

                
        ### [Severity Icon] [Severity Level] Finding Title
        **Location:** file_name.ext
        ```[language]
        // Show a short snippet of the vulnerable code here
        ```
        * **Error:** A one-sentence, no-nonsense technical explanation of why this code is bad.
        * **Fix:** A one-sentence solution followed by a compliant code snippet showing how to write it correctly:
        ```[language]
        // Show the secure, fixed code snippet here
        ```      
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
        ],
        "temperature": 0.1,
        "max_tokens": 1024
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
