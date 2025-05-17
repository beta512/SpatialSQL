# import json.decoder

# import openai
# from utils.enums import LLM
import time

from openai import OpenAI
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key="",
    base_url=""
)

# def init_chatgpt(OPENAI_API_KEY, OPENAI_GROUP_ID, model):
#     # if model == LLM.TONG_YI_QIAN_WEN:
#     #     import dashscope
#     #     dashscope.api_key = OPENAI_API_KEY
#     # else:
#     #     openai.api_key = OPENAI_API_KEY
#     #     openai.organization = OPENAI_GROUP_ID
#     openai.api_key = OPENAI_API_KEY
#     openai.organization = OPENAI_GROUP_ID


def ask_completion(model, batch, temperature):
    response = client.Completion.create(
        model=model,
        prompt=batch,
        temperature=temperature,
        max_tokens=200,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=[";"]
    )
    response_clean = [_["text"] for _ in response["choices"]]
    return dict(
        response=response_clean,
        **response["usage"]
    )


# def ask_chat(model, messages: list, temperature, n):
#     response = client.ChatCompletion.create(
#         model=model,
#         messages=messages,
#         temperature=temperature,
#         max_tokens=200,
#         n=n
#     )
#     response_clean = [choice["message"]["content"] for choice in response["choices"]]
#     if n == 1:
#         response_clean = response_clean[0]
#     return dict(
#         response=response_clean,
#         **response["usage"]
#     )

def ask_chat(model, messages: list, temperature, n):
    completion = client.chat.completions.create(
            model = model,
            messages = messages,
            temperature = temperature,
            n = n
            )
    response_clean = [choice.message.content for choice in completion.choices]
    if n == 1:
        response_clean = response_clean[0]
    #
    return dict(
                response = response_clean,
                total_tokens = completion.usage.total_tokens
                )

def ask_llm(model: str, batch: list, temperature: float, n:int):
    n_try = 5
    n_repeat = 0
    while n_repeat < n_try:
        try:
            assert len(batch) == 1, "batch must be 1 in this mode"
            messages = [{"role": "user", "content": batch[0]}]
            response = ask_chat(model, messages, temperature, n)
            # response['response'] = [response['response']]
            break
        except Exception as e:
            n_repeat += 1
            print(f"Repeat for the {n_repeat} times for exception: {e}", end="\n")
            time.sleep(10)
            response = {"response" : ["", "", "", "", ""]}
    #
    return response

