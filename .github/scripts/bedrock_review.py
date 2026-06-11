import os
import sys
import boto3

PR_DIFF_CONTENT = os.getenv("PR_DIFF")

def analyze_diff_with_native_bedrock(diff_content):
    print("Invoking official AWS Bedrock Runtime endpoint directly...")
    
    # Boto3 automatically figures out the correct native endpoint URL securely!
    client = boto3.client("bedrock-runtime", region_name="ap-south-1")
    
    system_prompt = (
        "Review the code as a senior software engineer. Always respond in English. "
        "Focus on: Security vulnerabilities, Bugs, Error handling, Performance, and Maintainability."
    )
    
    try:
        response = client.converse(
            modelId="amazon.nova-pro-v1:0", 
            messages=[{"role": "user", "content": [{"text": f"Review this diff:\n\n```diff\n{diff_content}\n```"}]}],
            system=[{"text": system_prompt}]
        )
        print(response['output']['message']['content']['text'])
    except Exception as e:
        print(f"Native AWS Invocation Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    analyze_diff_with_native_bedrock(PR_DIFF_CONTENT)
