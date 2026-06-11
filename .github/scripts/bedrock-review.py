import os
import sys
import boto3
from botocore.exceptions import ClientError

# 1. Capture the pre-extracted diff content from the YAML workflow
PR_DIFF_CONTENT = os.getenv("PR_DIFF") 
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# Target Amazon Bedrock Model ID
MODEL_ID = "openai.gpt-oss-safeguard-120b"

def analyze_diff_with_bedrock(diff_content):
    """Sends the pre-extracted git diff directly to Amazon Bedrock."""
    
    print(f"Invoking Amazon Bedrock model ({MODEL_ID})...")
    client = boto3.client("bedrock-runtime", region_name=AWS_REGION)
    
    # Your exact review criteria
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
    
    # Pack the diff directly into the user message payload
    messages = [
        {
            "role": "user",
            "content": [{"text": f"Please review this code change diff:\n\n```diff\n{diff_content}\n```"}]
        }
    ]
    
    try:
        response = client.converse(
            modelId=MODEL_ID,
            messages=messages,
            system=[{"text": system_prompt}],
            inferenceConfig={
                "maxTokens": 2048,
                "temperature": 0.2
            }
        )
        
        # Output the clean Markdown text directly to the runner's standard output
        review_output = response['output']['message']['content']['text']
        print(review_output)
        
    except ClientError as e:
        print(f"AWS Bedrock Client Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected invocation error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    analyze_diff_with_bedrock(PR_DIFF_CONTENT)
