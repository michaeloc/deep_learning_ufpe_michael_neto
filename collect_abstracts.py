import glob
import csv
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
import requests
from urllib import request, error
from requests.exceptions import HTTPError
from tqdm import tqdm

path = "dbpedia/treinamento/*.csv"
files = glob.glob(path)
dataset = []

for file in tqdm(files):
    with open(file, encoding="utf8") as f:
        reader = csv.reader(f)
        for line in reader:
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
                    for result in results["results"]["bindings"]:
                        for key, value in result.items():
                            abstract = (value['value'].replace("\n", ''))
                    # exibir a tupla no formato "entidade, label_alvo, labels, resumo"
                    tuple = [entity, label_target, labels, abstract]
                    dataset.append(tuple)
                    print(tuple)
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


