import openai

client = openai.OpenAI(
    base_url='http://192.168.2.206:8000/v1',
    api_key='NOT_NEED'

)
predict_ret = client.chat.completions.create(
    model='qwen2.5-7b-instruct', # 此处名称要和vllm中的served-model-name一致
    messages=[
        {'role': 'user', 'content': 'DeepVBM是什麼東西'}
    ]
)
print(
    predict_ret.choices[0].message.content
)
