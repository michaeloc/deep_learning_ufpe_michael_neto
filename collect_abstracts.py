import glob
import csv
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
import requests
from urllib import request, error
from requests.exceptions import HTTPError
from tqdm import tqdm
import time

path = "dbpedia/treinamento/*.csv"
files = glob.glob(path)
dataset = []
colunas = ['entity', 'class_target', 'other_class', 'abstract']
data_frame = pd.DataFrame()
for file in tqdm(files):
    with open(file, encoding="utf8") as f:
        reader = csv.reader(f)
        i = 0
        time.sleep(5)
        for line in tqdm(reader):
            if (line[1] != 'entity'):
                entity = line[1].replace('DBPEDIA_ID/', '')
                # remover virgulas do nome da entidade
                label_target = file[20:].replace('.csv', '')
                labels = line[2]

                # consulta para recuperar o resumo
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
                    print(tuple)
                    if(i % 200 == 0):
                        colunas = ['entity', 'class_target', 'other_class', 'abstract']
                        if len(data_frame) == 0:
                            data_frame = pd.DataFrame(dataset, columns=colunas)
                        else:
                            data_frame2 = pd.DataFrame(dataset, columns=colunas)
                            data_frame = pd.read_csv('file_output.csv')
                            data_frame = np.concatenate([data_frame,data_frame2])

                        data_frame.to_csv('file_output.csv')
                        break
                    i+=1
                except error.HTTPError as err:
                    if err.code == 404:
                        print('Error entity:{0}'.format(entity))
                        colunas = ['entity', 'class_target', 'other_class', 'abstract']
                        df = pd.DataFrame(dataset, columns=colunas)
                        df.to_csv('file_output.csv')
                    else:
                        raise
                    
        #break

# gerando csv de saída...
colunas = ['entity', 'class_target', 'other_class', 'abstract']
df = pd.DataFrame(dataset, columns=colunas)
df.to_csv('file_output.csv')


