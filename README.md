# SpatialSQL
Overview
=

The data and code were created for the review of the paper titled "GPT-Based Text-to-SQL for Spatial Databases". 

Datasets
=

The folder `sdbdatasets` contains the original datasets we created specifically for spatial databases, including `dataset1` and `dataset2`.<br>

In `dataset1`, there are four databases (folders): `ada`, `edu`, `tourism`, and `traffic`. Taking the folder `ada` as an example:
* The file `ada.sqlite` is an SQLite database file (We can use [spatialite-gui](http://www.gaia-gis.it/gaia-sins/windows-bin-amd64-latest/spatialite_gui-NG-5.0.0-win-amd64.7z), an open-source graphical user interface tool, to manage SQLite database files). <br>
* The file `ada.table.csv` contains geographic region descriptions for each database table, supporting both Chinese and English. <br>
* The file `QA-ada-56.txt` stores questions and corresponding SQL queries based on the `ada` database. <br>

Below is an examples from the file `QA-ada-56.txt`: <br>

     label:S Intersection
     questionCHI:河南省与湖北省的交界线长度是多少？
     evidenceCHI:
     nameCHI:河南省以'河南省'为名称表示，湖北省以'湖北省'为名称表示。
     question:What is the length of the border between Henan Province and Hubei Province?
     evidence:
     name:Henan Province is represented by the name '河南省', and Hubei Province is represented by the name '湖北省'.
     SQL:Select GLength(Intersection(a.Shape, b.Shape),1)  from provinces a inner join provinces b On Intersects(a.Shape, b.Shape) = 1 where a.name = '河南省' and b.name = '湖北省' %%% Select Sum(GLength(Intersection(a.Shape, b.Shape),1))  from cities a inner join cities b On Intersects(a.Shape, b.Shape) = 1 where a.province = '河南省' and b.province = '湖北省'
     Eval:Select GLength(Intersection(a.Shape, b.Shape),1)  from provinces a inner join provinces b On Intersects(a.Shape, b.Shape) = 1 where a.name = '河南省' and b.name = '湖北省' %%% Select Sum(GLength(Intersection(a.Shape, b.Shape),1))  from cities a inner join cities b On Intersects(a.Shape, b.Shape) = 1 where a.province = '河南省' and b.province = '湖北省' %%% Select GLength(Intersection(b.Shape, a.Shape),1)  from provinces a inner join provinces b On Intersects(a.Shape, b.Shape) = 1 where a.name = '河南省' and b.name = '湖北省' %%% Select Sum(GLength(Intersection(b.Shape, a.Shape),1))  from cities a inner join cities b On Intersects(a.Shape, b.Shape) = 1 where a.province = '河南省' and b.province = '湖北省'
     id: ada49
     
 




The meaning of each field is as follows:  


     |Field       | Description  
     |------------|-------
     |label       | For the SQL queries related to the question, 'G' denotes a general query, and 'S' represents a spatial query.
     |question    | The question in natural language. 
     |evidence    | Supporting knowledge.
     |name        | Real values of some phrases from the 'question' field in the database. 
     |questionCHI | The Chinese translation of the 'question' field.
     |evidenceCHI | The Chinese translation of the 'evidence' field.
     |nameCHI     | The Chinese translation of the 'name' field.
     |SQL         | The SQL query corresponding to the 'question' field. Due to derived columns, there may be multiple SQL queries, separated by '%%%'. 
     |Eval        | SQL queries corresponding to all results. When evaluating the predicted SQL queries with execution accuracy, results like 'GLength(Intersection(a.Shape, b.Shape), 1)' and 'GLength(Intersection(b.Shape, a.Shape), 1)' may differ. 
     |id          | The unique ID for the question.  


In `dataset2`, there are also four databases: `ada`, `edu`, `tourism`, and `traffic`.  
* The `tourism` database in `dataset2` is the same as the `tourism` database in `dataset1`.  
* The `ada`, `edu`, and `traffic` databases in `dataset2`  are derived from the corresponding databases in `dataset1`  by removing the derived columns.  
* The questions in both `dataset1`  and `dataset2`  are identical for each database.




Environment Setup
=
    

   To set up the environment, you should download the [Stanford CoreNLP](http://nlp.stanford.edu/software/stanford-corenlp-full-2018-10-05.zip), unzip it to the folder `./third_party/`, and rename `stanford-corenlp-full-2018-10-05` to `stanfordnlp`. Next, you need to launch the coreNLP server:



    install default-jre
    install default-jdk
    cd third_party/stanfordnlp
    java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000


   
   In addition,
   
   

    python -m pip install --upgrade pip
    pip install -r requirements.txt
    python nltk_downloader.py


After completing this step, several files will be automatically downloaded to the folders `punct`, `sentence-transformers`, `stopwords`, and `vector_cache`. Please refer to the images in each folder for more details. You can also refer to the installation steps in [DAIL-SQL](https://github.com/BeachWang/DAIL-SQL).
   <br><br>

Finally, to use [SpatiaLite](https://www.gaia-gis.it/gaia-sins/), we need refer to its official website.
![image](https://github.com/HuiWangAtTjnu/SSpa/blob/main/pics/pic3.png)<br>

On Windows, first download [mod_spatialite-5.1.0-win-amd64.7z](http://www.gaia-gis.it/gaia-sins/windows-bin-amd64/mod_spatialite-5.1.0-win-amd64.7z ), extract it, and add the path to the Windows' `Path` Environment Variable.

Run
======

Data Preprocess
------
This step includes copying databases from `sdbdatasets` to the corresponding folders (`experiments/dataset1_ada_edu`, `experiments/dataset1_tourism_traffic`,  `experiments/dataset2_ada_edu`, and `experiments/dataset2_tourism_traffic`) and applying required processing operations.<br>


* The folder `dataset1_ada_edu` indicates that the training set is built using data from the `tourism` and `traffic` databases in `dataset1`, and predictions are made for questions related to the `ada` and `edu` databases.
* The folder `dataset1_tourism_traffic` indicates that the training set is built using data from the `ada` and `edu` databases in `dataset1`, and predictions are made for questions related to the `tourism` and `traffic` databases.
* The folder `dataset2_ada_edu` indicates that the training set is built using data from the `tourism` and `traffic` databases in `dataset2`, and predictions are made for questions related to the ada and edu databases.
* The folder `dataset2_tourism_traffic` indicates that the training set is built using data from the `ada` and `edu` databases in `dataset2`, and predictions are made for questions related to the `tourism` and `traffic` databases.

<br>

    
    python data_preprocess.py


    

 
Prompt Generation
------
This step will generate corresponding questions (prompts) for each method (`dail_sql`, `sspa`, `sspa_geo`, `sspa_sdbms`, `sspa_tips`) across different datasets (`dataset1_ada_edu`, `dataset1_tourism_traffic`, `dataset2_ada_edu`, `dataset2_tourism_traffic`) and scenarios (shot-0, shot-1, shot-3, shot-5), and store the generated questions (prompts) in the folder `experiments/results`. 

    
    python generate_question.py --dataset dataset1 --databases ada_edu --algo sspa --shot 5



The parameter `dataset` can only be `dataset1` or `dataset2`, the parameter `databases` can only be `ada_edu` or `tourism_traffic`, the parameter `algo` can only be one of the following: `sspa`, `sspa_geo`, `ssap_tips`, `sspa_sdbms`, or `dail_sql`, the parameter `shot` can only be one of the values: `0`, `1`, `3`, or `5`<br>

The command `python generate_question.py --dataset dataset1 --databases ada_edu --algo sspa --shot 5` is used to generate questions (prompts) with a shot of `5` for the original questions in the `dataset1_ada_edu` dataset using the `sspa` method, and save the questions (prompts) in the `questions.json` file located in the `experiments/results/sspa/dataset1_ada_edu_shot_5` folder.
![image](https://github.com/HuiWangAtTjnu/SSpa/blob/main/pics/pic1.png)<br>


The following figure shows the files within the folder `dataset1_ada_edu_shot_5`, where `questions.json` is used to store the generated questions (prompts).<br>


![image](https://github.com/HuiWangAtTjnu/SSpa/blob/main/pics/pic2.png)<br>

Calling the LLM
------

   
This step involves sending the questions (prompts) generated in the previous step to the LLM in order to generate the corresponding SQL queries. 
<br>

    
    python ask_llm.py --dataset dataset1 --databases ada_edu --algo sspa --shot 5 --model gpt-4-turbo-2024-04-09


    

 
The parameter `dataset` can only be `dataset1` or `dataset2`, the parameter `databases` can only be `ada_edu` or `tourism_traffic`, the parameter `algo` can only be one of the following: `sspa`, `sspa_geo`, `ssap_tips`, `sspa_sdbms`, or `dail_sql`, the parameter `shot` can only be one of the values: `0`, `1`, `3`, or `5`, and the `model` parameter refers to the LLM being used, which in this case is `gpt-4-turbo-2024-04-09`. Additionally, you need to modify the `api_key` and `base_url` parameters in the file `llm/chatgpt.py`.<br><br>

The command `python ask_llm.py --dataset dataset1 --databases ada_edu --algo sspa --shot 5 --model gpt-4-turbo-2024-04-09` is used to send the questions (prompts) from the `questions.json` file located under the `experiments/results/sspa/dataset1_ada_edu_shot_5` folder to the LLM, and then save the predicted SQL queries to the `answers.json` file.

Evaluation
------
This step involves evaluating the predicted SQL queries using execution accuracy.<br>

    
    python eval.py --dataset dataset1 --databases ada_edu --algo sspa --shot 5


    

 
The parameter `dataset` can only be `dataset1` or `dataset2`, the parameter `databases` can only be `ada_edu` or `tourism_traffic`, the parameter `algo` can only be one of the following: `sspa`, `sspa_geo`, `ssap_tips`, `sspa_sdbms`, or `dail_sql`, the parameter `shot` can only be one of the values: `0`, `1`, `3`, or `5`.<br><br>

The command `python eval.py --dataset dataset1 --databases ada_edu --algo sspa --shot 5` is used to evaluate the SQL queries in the `answers.json` file located under the `experiments/results/sspa/dataset1_ada_edu_shot_5` folder, and then save the evaluation results to the `evaluations.json` file.

Statistics
------
We have placed all the results generated during the experiment in the `experiments/results` folder. This step will analyze the experimental results in the `experiments/results` folder and store the final statistics in the `experiments/results/statistics.txt` file. The file `experiments/results/statistics.txt` records all the data for the figures and tables presented in the paper.<br>
 
    
    python calculate.py



Reproduction
-------
For each combination of the 5 methods (`dail_sql`, `sspa`, `sspa_geo`, `sspa_sdbms`, `sspa_tips`), 4 datasets (`dataset1_ada_edu`, `dataset1_tourism_traffic`, `dataset2_ada_edu`, `dataset2_tourism_traffic`), and 4 shot values (shot-`0`, shot-`1`, shot-`3`, shot-`5`), a total of 80 cases are considered.

For example, taking the `sspa` method, `dataset1_ada_edu`, and a shot value of `5`: 
* The command `python generate_question.py --dataset dataset1 --databases ada_edu --algo sspa --shot 5` is used to generate questions (prompts), which are saved in the `questions.json` file.
* The command `python ask_llm.py --dataset dataset1 --databases ada_edu --algo sspa --shot 5 --model gpt-4-turbo-2024-04-09` sends the questions (prompts) to the LLM, and the predicted SQL queries are stored in the `answers.json` file.
* The command `python eval.py --dataset dataset1 --databases ada_edu --algo sspa --shot 5` is used to validate the SQL queries in `answers.json`, and the evaluation results are saved in the `evaluations.json` file.

![image](https://github.com/HuiWangAtTjnu/SSpa/blob/main/pics/pic4.png)<br>



Acknowledgement
------

The code is inspired by [DAIL-SQL](https://github.com/BeachWang/DAIL-SQL).


References
------

1.Dawei Gao, Haibin Wang, Yaliang Li, Xiuyu Sun, Yichen Qian, Bolin Ding and Jingren Zhou. 2023. Text-to-SQL Empowered by Large Language Models: A Benchmark Evaluation. CoRR abs/2308.15363.<br>
2.Dawei Gao, Haibin Wang, Yaliang Li, Xiuyu Sun, Yichen Qian, Bolin Ding and Jingren Zhou. 2024. Text-to-SQL Empowered by Large Language Models: A Benchmark Evaluation. Proceedings of the VLDB Endowment, 17(5), 1132–1145.<br>
    
