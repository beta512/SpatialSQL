"""
Generate questions for LLMs and save it as a task
"""
import argparse
import os
import sys
import json
from prompt.prompt_builder import prompt_factory
from utils.data_builder import load_data
# from utils.enums import REPR_TYPE, EXAMPLE_TYPE, SELECTOR_TYPE, LLM
from utils.enums import LLM
from utils.utils import cost_estimate

from tqdm import tqdm



PATH_DATA = "experiments/"
# PATH_DATA = "dataset/"

sys.path.append("./")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, choices=['dataset1', 'dataset2'],  required=True)
    parser.add_argument("--databases", type=str, choices=['ada_edu', 'tourism_traffic'],  required=True)
    parser.add_argument("--algo", type=str, choices=["dail_sql", "sspa", "sspa_tips", "sspa_sdbms", "sspa_geo"], default="sspa",  required=True)
    parser.add_argument("--shot", type=int, choices=[0, 1, 3, 5],  required=True)
    args = parser.parse_args()
    #
    dataset = args.dataset
    databases = args.databases
    algo = args.algo
    shot = args.shot
    #
    # dataset = 'dataset1'
    # databases = 'ada_edu'
    # algo = 'sspa'
    # shot = 5

    dataset_name = f'{dataset}_{databases}'
    #
    data = load_data(dataset_name, PATH_DATA)

    # Read all tables into a dict
    databases = data.get_databases()

    # select the prompt
    prompt = prompt_factory('SQL', shot, 'QA', 'EUCDISQUESTIONMASK')(data=data, tokenizer='gpt-4-turbo')
    # prompt = prompt_factory(args.prompt_repr, args.k_shot, args.example_type, args.selector_type)(data=data, tokenizer=args.tokenizer)

    # format all questions
    questions = list()
    token_cnt = 0

    # choose split
    # func_name = f"get_{args.split}_json"
    # cross_domain = args.split == "train"
    split = 'test'
    func_name = f"get_{split}_json"
    cross_domain = split == "train"
    
    max_seq_len = 2048
    max_ans_len = 200
    scope_factor = 100
    for question_json in tqdm(getattr(data, func_name)()):
        if algo == 'sspa' or algo == 'sspa_tips':
            question_format = prompt.format(f'{PATH_DATA}/{dataset_name}',
                                        1, #是否包含数据库前缀
                                        1, #是否包含范围描述
                                        target=question_json,
                                        max_seq_len=max_seq_len,
                                        max_ans_len=max_ans_len,
                                        scope_factor=scope_factor,
                                        cross_domain=cross_domain)
        elif algo == 'sspa_sdbms':
            question_format = prompt.format(f'{PATH_DATA}/{dataset_name}',
                                        0, #是否包含数据库前缀
                                        1, #是否包含范围描述
                                        target=question_json,
                                        max_seq_len=max_seq_len,
                                        max_ans_len=max_ans_len,
                                        scope_factor=scope_factor,
                                        cross_domain=cross_domain)
        elif algo == 'sspa_geo':
            question_format = prompt.format(f'{PATH_DATA}/{dataset_name}',
                                        1, #是否包含数据库前缀
                                        0, #是否包含范围描述
                                        target=question_json,
                                        max_seq_len=max_seq_len,
                                        max_ans_len=max_ans_len,
                                        scope_factor=scope_factor,
                                        cross_domain=cross_domain)
        elif algo == 'dail_sql':
            question_format = prompt.format(f'{PATH_DATA}/{dataset_name}',
                                        0, #是否包含数据库前缀
                                        0, #是否包含范围描述
                                        target=question_json,
                                        max_seq_len=max_seq_len,
                                        max_ans_len=max_ans_len,
                                        scope_factor=scope_factor,
                                        cross_domain=cross_domain)
        else:
            break
        question_format['id'] = question_json['id']
        questions.append(question_format)
        
        token_cnt += question_format["prompt_tokens"]

    # cost estimated
    token_cnt = float(token_cnt) / len(questions)
    print(f"Total {len(questions)} questions, {token_cnt} tokens per prompt, {token_cnt / len(questions)} tokens per question")
    
    # n_total_tokens = len(questions) * args.max_ans_len + token_cnt
    n_total_tokens = len(questions) * max_ans_len + token_cnt
    cost_gpt_35_turbo = cost_estimate(n_total_tokens, LLM.GPT_35_TURBO)
    cost_text_davinci_003 = cost_estimate(n_total_tokens, LLM.TEXT_DAVINCI_003)
    example_quality = prompt.get_example_quality()
    # example_quality_each = prompt.get_example_quality_for_each()
    pattern_similarity = prompt.get_pattern_similarity()
    print(f"Example quality: {example_quality}")
    print(f"Estimated cost for {LLM.GPT_4}: {cost_gpt_35_turbo*20}")
    print(f"Estimated cost for {LLM.GPT_35_TURBO}: {cost_gpt_35_turbo}")
    print(f"Estimated cost for {LLM.TEXT_DAVINCI_003}: {cost_text_davinci_003}")

    # save questions
    task = {
        # "args": vars(args),
        "args": 'vars(args)',
        "costs": {
            "prompt_tokens_per_prompt": token_cnt,
            "gpt-4": cost_gpt_35_turbo*20,
            "gpt-3.5-turbo": cost_gpt_35_turbo,
            "text-davinci-003": cost_text_davinci_003,
            "example_quality": example_quality,
            "pattern_similarity": pattern_similarity,
            # "example_quality_for_each": example_quality_each
        },
        "questions": questions
    }
    # dataset-1-shot-1-ada-edu
    # path_generate = f"dataset/process/{data_type.upper()}-{split.upper()}_{prompt.name}_CTX-{max_ans_len}_ANS-{max_seq_len}"
    path_generate = f"./experiments/results/{algo}/{dataset_name}_shot_{shot}"
    # path_generate = f"dataset/process/{args.data_type.upper()}-{args.split.upper()}_{prompt.name}_CTX-{args.max_ans_len}_ANS-{args.max_seq_len}"
        
    os.makedirs(path_generate, exist_ok=True)
    json.dump(task, open(os.path.join(path_generate, "questions.json"), "w", encoding = 'utf-8'), ensure_ascii = False, indent=4)
    