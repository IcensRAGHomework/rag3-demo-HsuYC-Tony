import io
import os
import csv
import datetime
import chromadb
import pandas as pd
import traceback

from chromadb.utils import embedding_functions

from model_configurations import get_model_configuration

gpt_emb_config = get_model_configuration('text-embedding-ada-002')

dbpath = "./"

def get_chromadb_id():
    count = 1
    today = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    ids = f"{today}{count:04}"
    return ids

def chromadb_add(metadata, text, total_count=1):
    print('===== Add from vector database =====')

    chroma_client = chromadb.PersistentClient(path=dbpath)
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key = gpt_emb_config['api_key'],
        api_base = gpt_emb_config['api_base'],
        api_type = gpt_emb_config['openai_type'],
        api_version = gpt_emb_config['api_version'],
        deployment_id = gpt_emb_config['deployment_name']
    )
    collection = chroma_client.get_or_create_collection(
        name="TRAVEL",
        metadata={"hnsw:space": "cosine"},
        embedding_function=openai_ef)

    id = get_chromadb_id()
    ids =[]
    for i in range(total_count):
        ids.append(f"{id[:-4]}{int(id[-4:]) + i:04}")

    collection.add(
        documents=text,
        metadatas=metadata,
        ids=ids
    )

def process_text_data(file_name, fname, ftype, faddress, ftel, fcity, ftown ,fdate, content_list, metadatas, total_count, ftext):
    metadata_template = {
        "file_name": file_name,
        "name": fname,
        "type": ftype,
        "address": faddress,
        "tel": ftel,
        "city": fcity,
        "town": ftown,
        "date": int(datetime.datetime.strptime(fdate, "%Y-%m-%d").timestamp())
    }

    metadatas.append(metadata_template.copy())
    content_list.append(ftext)
    total_count += 1

    return total_count

def init_chromadb():
    content_list = []
    metadatas = []
    total_count = 0

    file_name = 'COA_OpenData.csv'
    with open(file_name, 'r', encoding='utf-8-sig') as file:
        csv_content = file.read()

    csv_buffer = io.StringIO(csv_content)
    csv_reader = csv.DictReader(csv_buffer)

    for row in csv_reader:
        fname = row['Name']
        ftype = row['Type']
        faddress = row['Address']
        ftel = row['Tel']
        ftext = row['HostWords']
        fcity = row['City']
        ftown = row['Town']
        fdate = row['CreateDate']

        total_count = process_text_data(file_name, fname, ftype, faddress, ftel, fcity, ftown, fdate, content_list, metadatas, total_count, ftext)
    
    chromadb_add(metadatas, content_list, total_count)

def generate_hw01():
    print('   ')
    pass

def generate_hw02(question, city, store_type, start_date, end_date):
    pass

def generate_hw03(question, store_name, new_store_name, city, store_type):
    pass

if __name__ == '__main__':
    try:
        file_name = 'chroma.sqlite3'
        if not os.path.exists(file_name):
            init_chromadb()

        # hw01
        result = generate_hw01()
        result_count = result.count()
        print(result_count)

        # hw02
        question = '我想要找有關茶餐點的店家'
        city = ["宜蘭縣", "新北市"]
        store_type = ["美食"]
        start_date = datetime.datetime(2024, 4, 1)
        end_date = datetime.datetime(2024, 5, 1)

        result_names = generate_hw02(question, city, store_type, start_date, end_date)
        print(result_names)
        
        # hw03
        question = '我想要找南投縣的田媽媽餐廳，招牌是蕎麥麵'
        store_name = '耄饕客棧'
        new_store_name = '田媽媽（耄饕客棧）'
        city = ["南投縣"]
        store_type = ["美食"]
        result_names = generate_hw03(question, store_name, new_store_name, city, store_type)
        print(result_names)

        print('End')
    except Exception as e:
        traceback_info = traceback.format_exc()
        print(traceback_info)
        #print(e)
