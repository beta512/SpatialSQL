import os
import json
import sqlite3
import re
import argparse
from llm.chatgpt import ask_llm
# import openai
from utils.post_process import process_duplication, get_sqls

def get_table_names(db_path = None):
    spatialite_tables = ['spatial_ref_sys', 'spatialite_history', 'sqlite_sequence',
                         'geometry_columns', 'spatial_ref_sys_aux', 'views_geometry_columns',
                         'virts_geometry_columns', 'geometry_columns_statistics', 'views_geometry_columns_statistics',
                         'virts_geometry_columns_statistics', 'geometry_columns_field_infos', 'views_geometry_columns_field_infos',
                         'virts_geometry_columns_field_infos', 'geometry_columns_time', 'geometry_columns_auth',
                         'views_geometry_columns_auth', 'virts_geometry_columns_auth', 'sql_statements_log',
                         'sqlite_stat1', 'sqlite_stat3', 'SpatialIndex', 'ElementaryGeometries']
    #
    connection = sqlite3.connect(db_path)
    #
    connection.enable_load_extension(True)
    connection.execute('SELECT load_extension("mod_spatialite.dll")')
    cursor = connection.cursor()
    #
    cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
    table_names = cursor.fetchall()
    table_names = [_[0] for _ in table_names]
    #
    table_set = set(table_names)
    table_set = table_set.difference(spatialite_tables)
    table_names = list(table_set)
    #
    return table_names


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, choices=['dataset1', 'dataset2'],  required=True)
    parser.add_argument("--databases", type=str, choices=['ada_edu', 'tourism_traffic'],  required=True)
    parser.add_argument("--algo", type=str, choices=["dail_sql", "sspa", "sspa_tips", "sspa_sdbms", "sspa_geo"], default="sspa",  required=True)
    parser.add_argument("--shot", type=int, choices=[0, 1, 3, 5],  required=True)
    parser.add_argument("--model", type=str, default="gpt-4-turbo-2024-04-09")
    args = parser.parse_args()
    #
    dataset = args.dataset
    databases = args.databases
    algo = args.algo
    shot = args.shot
    model = args.model
    #
    # dataset = 'dataset1'
    # databases = 'ada_edu'
    # algo = 'sspa'
    # shot = '5'
    # model = 'gpt-4-turbo-2024-04-09'
    
    db_dir = f'./experiments/{dataset}_{databases}/databases'
    question_dir = f'./experiments/results/{algo}/{dataset}_{databases}_shot_{shot}'
    
    #
    db_dict = {}
    db_names = ['ada', 'edu', 'tourism', 'traffic']
    for db_name in db_names:
        db_dict[db_name] = set()
        table_names = get_table_names(os.path.join(db_dir, f"{db_name}/{db_name}.sqlite"))
        for table_name in table_names:
            db_dict[db_name].add(table_name)
    #
    
    
    #
    questions_json = json.load(open(os.path.join(question_dir, "questions.json"), "r", encoding = 'utf-8'))
    questions = [_["prompt"] for _ in questions_json["questions"]]
    db_ids = [_["db_id"] for _ in questions_json["questions"]]
    ids = [_["id"] for _ in questions_json["questions"]]
    #
    exceptionf = open(os.path.join(question_dir, "repetitions.json"), 'w', encoding = 'utf-8')
    exceptionf.write('[')
    #
    answerf = open(os.path.join(question_dir, "answers.json"), 'w', encoding = 'utf-8')
    answerf.write('[')
    
    n_try = 5
    answer_flag = 0
    exception_flag = 0
    for db_id, _id, question in zip(db_ids, ids, questions):
        # if _id < 'ada38':
        #     continue
        
        n_repeat = 0
        notableset = set()
        nocolumndict = {}
        #
        prompt = question
        while n_repeat < n_try:
            n_repeat += 1
            #
            res = ask_llm(model, [prompt], 0, 5)
            #
            sqls = res['response']
            processed_sqls = []
            for sql in sqls:
                sql = sql.replace("```sql", '')
                sql = sql.replace("```", '')
                sql = sql.replace('\\n', ' ')
                sql = sql.replace("\\'", "'")
                sql = sql.replace(';', "")
                sql = sql.replace('"', "'")
                sql = sql.replace('ST_', '')
                sql = sql.replace('GLength(', 'Length(')
                sql = sql.replace('Length(', 'GLength(')
                
                sql = " ".join(sql.replace("\n", " ").split())
                sql = process_duplication(sql)
                # if sql.startswith("SELECT"):
                if sql.lower().startswith("select"):
                    pass
                elif sql.startswith(" "):
                    sql = "SELECT" + sql
                else:
                    sql = "SELECT " + sql
                processed_sqls.append(sql)
            #
            result = {
                'db_id': db_id,
                'p_sqls': processed_sqls
            }
            final_sqls = get_sqls([result], 5, db_dir)
            #
            sql = final_sqls[0]
            sql_ = sql
            
            db_path = os.path.join(db_dir, f"{db_id}/{db_id}.sqlite")
            conn = sqlite3.connect(db_path)
            #
            conn.enable_load_extension(True)
            conn.execute('SELECT load_extension("mod_spatialite.dll")')

            # Connect to the database
            cursor = conn.cursor()
            try:
                cursor.execute(sql)
                break
            except Exception as e:
                tableObj = re.search(r'no\ssuch\stable:\s(?P<table>[^\s]+)', str(e))
                if tableObj:
                    table = tableObj.group('table')
                    notableset.add(table)
                #
                columnObj = re.search(r'no\ssuch\scolumn:\s((?P<table>[^\s]+)\.)?(?P<column>[^\s]+)', str(e))
                if columnObj:
                    column = columnObj.group('column')
                    table = columnObj.group('table')
                    if table is not None:
                        if table not in db_dict[db_id]:
                            tableObj = re.search(f"(?P<table>[^\s]+)\s+(As\s+)?{table}\s+", sql, re.IGNORECASE)
                            if tableObj:
                                table = tableObj['table']
                    else:
                        tableObj = re.search("from\s+(?P<table>[^\s]+)\s+", sql, re.IGNORECASE)
                        if tableObj:
                            table = tableObj['table']
                     #
                    if table not in db_dict[db_id]:
                        notableset.add(table)
                    else:
                        if table not in nocolumndict:
                            nocolumndict[table] = set()
                        nocolumndict[table].add(column)
                #
                index = question.rfind('*/')
                assert(index > 0)
                
                tips = ''
                notables = list(notableset)
                notables.sort()
                if len(notables) == 1:
                    tips += f'The table "{notables[0]}" does not exist in the database and should not be used. '
                elif len(notables) == 2:
                    tips += f'The tables "{notables[0]}" and "{notables[1]}" do not exist in the database and should not be used. '
                elif len(notables) >= 3:
                    tips += f'The tables "{notables[0]}"'
                    for i in range(1, len(notables) - 1):
                        tips += f',"{notables[i]}"'
                    tips += f' and "{notables[-1]}" do not exist in the database and should not be used. '
                #     
                for table in nocolumndict.keys():
                    nocolumns = list(nocolumndict[table])
                    if len(nocolumns) == 1:
                        tips += f'The column "{nocolumns[0]}" does not exist in the table "{table}" and should not be used. '
                    elif len(nocolumns) == 2:
                        tips += f'The columns "{nocolumns[0]}" and "{nocolumns[1]}" do not exist in the table "{table}" and should not be used. '
                    elif len(nocolumns) >= 3:
                        tips += f'The columns "{nocolumns[0]}"'
                        for i in range(1, len(nocolumns) - 1):
                            tips += f',"{nocolumns[i]}"'
                        tips += f' and "{nocolumns[-1]}" do not exist in the table "{table}" and should not be used. '
                amcolumnObj = re.search(r'ambiguous\scolumn\sname:\s(?P<amcolumn>[^\s]+)', str(e))
                if amcolumnObj:
                    tips += "Columns in multiple tables may have the same name, so ambiguity should be avoided. "
                
               
                prompt = question[:index] + tips + question[index:]
                #
                if 1 == exception_flag:
                    exceptionf.write(',\n')  
                else:
                    exceptionf.write('\n')  
                exception_flag = 1
                exceptionf.write('    {\n')
                prompt_ = prompt.replace('\n', '\\n')  
                sql_ = sql_.replace('\\n', ' ')
                exceptionf.write(f'        "sql_":"{sql_}",\n')
                exceptionf.write(f'        "error_info":"Repeat for the {n_repeat} times for exception: {e}",\n')
                exceptionf.write(f'        "db_id":"{db_id}",\n')
                exceptionf.write(f'        "id":"{_id}",\n')
                exceptionf.write(f'        "sql":"{sql}",\n')
                exceptionf.write(f'        "prompt":"{prompt_}"\n')
                exceptionf.write('    }')     
                exceptionf.flush()
                #
        #
        if 1 == answer_flag:
            answerf.write(',\n')  
        else:
            answerf.write('\n')  
        answer_flag = 1
        answerf.write('    {\n')
        answerf.write(f'        "db_id":"{db_id}",\n')
        answerf.write(f'        "id":"{_id}",\n')
        answerf.write(f'        "sql":"{sql}"\n')
        answerf.write('    }')     
        #
        answerf.flush()
    answerf.write('\n]')   
    answerf.close()  
    #
    exceptionf.write('\n]')   
    exceptionf.close()  