import glob
import csv
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
import requests
from urllib import request, error
from requests.exceptions import HTTPError
from tqdm import tqdm
import time
import numpy as np

path = "dbpedia/treinamento/*.csv"
files = glob.glob(path)
colunas = ['entity', 'class_target', 'other_class', 'abstract']
dataset_out = []
data_frame = pd.DataFrame()

# downloaded_data = pd.read_csv('file_output.csv')
# unique_class_downloaded = np.unique(downloaded_data.class_target.values)
# print(unique_class_downloaded)
for file in tqdm(files):
    with open(file, encoding="utf8") as f:
        reader = csv.reader(f)
        i = 1
        dataset = []
        time.sleep(2)
        print(reader)
        for line in reader:
            if (line[1] != 'entity'):
                entity = line[1].replace('DBPEDIA_ID/', '')
                # remover virgulas do nome da entidade
                label_target = file[20:].replace('.csv', '')
                labels = line[2]

                # if label_target in unique_class_downloaded:

                #     print(label_target) 
                #     break
                
                # print(label_target)
                               
#               consulta para recuperar o resumo
                query = "PREFIX dbpedia-owl: <http://dbpedia.org/ontology/> " \
                        " select * where" \
                        " { <http://dbpedia.org/resource/" + entity + "> dbpedia-owl:abstract ?abstract " \
                        "filter(langMatches(lang(?abstract),\"en\")) }"

                # extrair o resumo para uma variável
                try:
                    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
                    sparql.setQuery(query)
                    sparql.setReturnFormat(JSON)
                    results = sparql.query().convert()
                    abstract = tuple()
                    for result in results["results"]["bindings"]:
                        for key, value in result.items():
                            abstract = (value['value'].replace("\n", ''))
                    # exibir a tupla no formato "entidade, label_alvo, labels, resumo"
                    tuple_ = [entity, label_target, labels, abstract]
                    dataset.append(tuple_)
                    dataset_out.append(tuple_)
                    if(i % 1000 == 0) or (i == reader.line_num):
                        colunas = ['entity', 'class_target', 'other_class', 'abstract']
                        if len(data_frame) == 0:
                            data_frame = pd.DataFrame(dataset, columns=colunas)
                        else:
                            # data_frame = pd.read_csv('file_output.csv',index_col=0)
                            data_frame2 = pd.DataFrame(dataset, columns=colunas)
                            data_frame = pd.concat([data_frame,data_frame2],ignore_index=True)
                        data_frame.to_csv('file_output_1000_example.csv')
                        break
                    i+=1
                except error.HTTPError as err:
                    if err.code == 404:
                        print('Error entity:{0}'.format(entity))
                        colunas = ['entity', 'class_target', 'other_class', 'abstract']
                        df = pd.DataFrame(dataset, columns=colunas)
                        df.to_csv('file_output_1000_example.csv')
                    else:
                        raise
                    
        #break

# gerando csv de saída...
colunas = ['entity', 'class_target', 'other_class', 'abstract']
df = pd.DataFrame(dataset_out, columns=colunas)
df.to_csv('file_output_1000_example.csv')


