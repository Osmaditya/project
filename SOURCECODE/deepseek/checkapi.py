# import requests

# api_key = "sk-ca460cb204004c93aeec30e048a4f4d2"
# headers = {
#     "Authorization": f"Bearer {api_key}"
# }

# response = requests.get("https://openrouter.ai/api/v1/models", headers=headers)

# if response.status_code == 200:
#     print("✅ API Key is working!")
# else:
#     print(f"❌ API Key Error: {response.status_code} - {response.text}")


from openai import OpenAI

client = OpenAI(
    api_key="sk-ca460cb204004c93aeec30e048a4f4d2"
)

completion = client.chat.completions.create(
    model="deepseek/deepseek-r1:free",
    messages=[{"role": "user", "content": "Who is the president of America?"}]
)

print(completion.choices[0].message.content)
