import argparse
import json
import os
# import pickle
from pathlib import Path
import sqlite3
from tqdm import tqdm
# import random
import shutil
from utils.linking_process import SpiderEncoderV2Preproc
from utils.pretrained_embeddings import GloVe
from utils.datasets.spider import load_tables
# from dataset.process.preprocess_kaggle import gather_questions


def schema_linking_producer(test, train, table, db, dataset_dir, compute_cv_link=True):

    # load data
    test_data = json.load(open(os.path.join(dataset_dir, test), encoding='utf-8'))
    train_data = json.load(open(os.path.join(dataset_dir, train), encoding='utf-8'))

    # load schemas
    schemas, _ = load_tables([os.path.join(dataset_dir, table)])

    # Backup in-memory copies of all the DBs and create the live connections
    for db_id, schema in tqdm(schemas.items(), desc="DB connections"):
        sqlite_path = Path(dataset_dir) / db / db_id / f"{db_id}.sqlite"
        source: sqlite3.Connection
        with sqlite3.connect(str(sqlite_path)) as source:
            #
            source.enable_load_extension(True)
            source.execute('SELECT load_extension("mod_spatialite.dll")')
            #
            dest = sqlite3.connect(':memory:')
            #
            dest.enable_load_extension(True)
            dest.execute('SELECT load_extension("mod_spatialite.dll")')
            #
            dest.row_factory = sqlite3.Row
            source.backup(dest)
        schema.connection = dest

    word_emb = GloVe(kind='42B', lemmatize=True)
    linking_processor = SpiderEncoderV2Preproc(dataset_dir,
            min_freq=4,
            max_count=5000,
            include_table_name_in_column=False,
            word_emb=word_emb,
            fix_issue_16_primary_keys=True,
            compute_sc_link=True,
            compute_cv_link=compute_cv_link)

    # build schema-linking
    for data, section in zip([test_data, train_data],['test', 'train']):
        for item in tqdm(data, desc=f"{section} section linking"):
            db_id = item["db_id"]
            schema = schemas[db_id]
            to_add, validation_info = linking_processor.validate_item(item, schema, section)
            if to_add:
                linking_processor.add_item(item, schema, section, validation_info)

    # save
    linking_processor.save()


def bird_pre_process(bird_dir, with_evidence=False):
    new_db_path = os.path.join(bird_dir, "databases")
    if os.path.exists(new_db_path):
        shutil.rmtree(new_db_path)
    src = os.path.join(bird_dir, 'train/train_databases/')
    shutil.copytree(src, new_db_path)
    #
    temp_db_path = os.path.join(bird_dir, "temp_databases")
    if os.path.exists(temp_db_path):
        shutil.rmtree(temp_db_path)
    src = os.path.join(bird_dir, 'dev/dev_databases/')
    shutil.copytree(src, temp_db_path)
    #
    dirs = os.listdir(temp_db_path)
    for _dir in dirs:
        shutil.move(os.path.join(temp_db_path, _dir), new_db_path)
    #
    shutil.rmtree(temp_db_path)
    # if not os.path.exists(new_db_path):
    #     os.system(f"cp -r {os.path.join(bird_dir, 'train/train_databases/*')} {new_db_path}")
    #     os.system(f"cp -r {os.path.join(bird_dir, 'dev/dev_databases/*')} {new_db_path}")

    def json_preprocess(data_jsons):
        new_datas = []
        for data_json in data_jsons:
            ### Append the evidence to the question
            if with_evidence and len(data_json["evidence"]) > 0:
                data_json['question'] = (data_json['question'] + " " + data_json["evidence"]).strip()
            question = data_json['question']
            tokens = []
            for token in question.split(' '):
                if len(token) == 0:
                    continue
                if token[-1] in ['?', '.', ':', ';', ','] and len(token) > 1:
                    tokens.extend([token[:-1], token[-1:]])
                else:
                    tokens.append(token)
            data_json['question_toks'] = tokens
            data_json['query'] = data_json['SQL']
            new_datas.append(data_json)
        return new_datas

    output_dev = 'dev.json'
    output_train = 'train.json'
    with open(os.path.join(bird_dir, 'dev/dev.json'), encoding='utf-8') as f:
        data_jsons = json.load(f)
        # wf = open(os.path.join(bird_dir, output_dev), 'w')
        wf = open(os.path.join(bird_dir, output_dev), 'w', encoding='utf-8')
        json.dump(json_preprocess(data_jsons), wf, ensure_ascii = False, indent=4)
    with open(os.path.join(bird_dir, 'train/train.json'), encoding='utf-8') as f:
        data_jsons = json.load(f)
        # wf = open(os.path.join(bird_dir, output_train), 'w')
        wf = open(os.path.join(bird_dir, output_train), 'w', encoding='utf-8')
        json.dump(json_preprocess(data_jsons), wf, ensure_ascii = False, indent=4)
    # os.system(f"cp {os.path.join(bird_dir, 'dev/dev.sql')} {bird_dir}")
    # os.system(f"cp {os.path.join(bird_dir, 'train/train_gold.sql')} {bird_dir}")
    src = os.path.join(bird_dir, 'dev/dev.sql')
    shutil.copy(src, bird_dir)

    src = os.path.join(bird_dir, 'train/train_gold.sql')
    shutil.copy(src, bird_dir)
    #
    tables = []
    with open(os.path.join(bird_dir, 'dev/dev_tables.json'), encoding='utf-8') as f:
        tables.extend(json.load(f))
    with open(os.path.join(bird_dir, 'train/train_tables.json'), encoding='utf-8') as f:
        tables.extend(json.load(f))
    with open(os.path.join(bird_dir, 'tables.json'), 'w', encoding='utf-8') as f:
        json.dump(tables, f, indent=4)

def copy_databases(bird_dir, dataset_dir, db1, db2):
    for db in [db1, db2]:
        db_path = f'{bird_dir}/dev/dev_databases/{db}'
        if os.path.exists(db_path):
            shutil.rmtree(db_path)
        src = f'{dataset_dir}/{db}'
        shutil.copytree(src, db_path)
    #
    for db in ['ada', 'edu', 'tourism', 'traffic']:
        if db in [db1, db2]:
            continue
        db_path = f'{bird_dir}/train/train_databases/{db}'
        if os.path.exists(db_path):
            shutil.rmtree(db_path)
        src = f'{dataset_dir}/{db}'
        shutil.copytree(src, db_path)


if __name__ == '__main__':
    datasets_dir = './sdbdatasets'
    bird_dev = 'dev.json'
    bird_train = 'train.json'
    bird_table = 'tables.json'
    bird_db = 'databases'
    #
    bird_dir = './experiments/dataset1_ada_edu'
    dataset_dir = f'{datasets_dir}/dataset1'
    copy_databases(bird_dir, dataset_dir, 'ada', 'edu')
    bird_pre_process(bird_dir, with_evidence=True)
    schema_linking_producer(bird_dev, bird_train, bird_table, bird_db, bird_dir, compute_cv_link=False)
    #
    bird_dir = './experiments/dataset1_tourism_traffic'
    dataset_dir = f'{datasets_dir}/dataset1'
    copy_databases(bird_dir, dataset_dir, 'tourism', 'traffic')
    bird_pre_process(bird_dir, with_evidence=True)
    schema_linking_producer(bird_dev, bird_train, bird_table, bird_db, bird_dir, compute_cv_link=False)
    #
    bird_dir = './experiments/dataset2_ada_edu'
    dataset_dir = f'{datasets_dir}/dataset2'
    copy_databases(bird_dir, dataset_dir, 'ada', 'edu')
    bird_pre_process(bird_dir, with_evidence=True)
    schema_linking_producer(bird_dev, bird_train, bird_table, bird_db, bird_dir, compute_cv_link=False)
    #
    bird_dir = './experiments/dataset2_tourism_traffic'
    dataset_dir = f'{datasets_dir}/dataset2'
    copy_databases(bird_dir, dataset_dir, 'tourism', 'traffic')      
    bird_pre_process(bird_dir, with_evidence=True)
    schema_linking_producer(bird_dev, bird_train, bird_table, bird_db, bird_dir, compute_cv_link=False)
    #
    print('Finished~')
