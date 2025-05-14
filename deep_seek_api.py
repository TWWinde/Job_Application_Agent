from openai import OpenAI
import json
import requests
from prompts import cover_letter_prompt, summary_job_description
from read_jd import read_txt_as_single_line

def deepseek_api(prompt):
    """
    This function initializes the DeepSeek API client and sends a chat completion request.
    It prints the content of the first choice in the response.
    """
   
    client = OpenAI(api_key="sk-226d5f1482d64e0fa0231158c3246e5b", base_url="https://api.deepseek.com/v1")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a experienced writer for motivation letter"},
            {"role": "user", "content": prompt},
        ],
        stream=False,
        temperature=1.3,

    )

    print(response.choices[0].message.content)

    return response.choices[0].message.content


def call_deepseek_api(prompt, api_key):
    url = "https://api.deepseek.com/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-chat",  # 或 "deepseek-coder" / 其他支持模型
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content']
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None
    


if __name__ == "__main__":

    jd_path = "/Users/tangwenwu/Documents/GitHub/Job_Application_Agent/job_txt/PhD Position Embedded Active Inference for Autonomous Robots.txt"
    jd = read_txt_as_single_line(jd_path)
    prompt = cover_letter_prompt(jd)
    print(prompt)
    output = deepseek_api(prompt)