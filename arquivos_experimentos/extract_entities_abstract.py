import csv
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
from tqdm import tqdm

file_txt = "entities_AAUP.txt"               # arquivo com todas as entidades do dataset
file_csv = "entities_AAUP_output.csv"        # arquivo com as entidades já extraídas

def read_file_txt(file_txt):
    all_dataset = []
    with open(file_txt, "r") as arquivo:
        for linha in arquivo:
            linha = linha.rstrip('\n')
            all_dataset.append(linha.replace('http://dbpedia.org/resource/', ''))
    return all_dataset

def read_file_csv(file_csv):
    dataset_without = []
    with open(file_csv, encoding="utf8") as f:
        reader = csv.reader(f)
        for line in reader:
            if (line[1] != 'entity'):
                dataset_without.append(line[1])
    return dataset_without

def merge_entities(file_txt, file_csv):
    list_txt = read_file_txt(file_txt)
    list_csv = read_file_csv(file_csv)
    entities = []
    for i in range(len(list_txt)):
        if (list_txt[i] in list_csv) == False:
            entities.append(list_txt[i])
    return entities

def extract_types(entity):
    query = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> " \
            "SELECT ?type WHERE { <http://dbpedia.org/resource/" + entity + "> rdf:type ?type}"

    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    types = []
    for result in results["results"]["bindings"]:
        for key, value in result.items():
            tipo = (value['value'].replace("\n", ''))
            if (tipo[:28] == 'http://dbpedia.org/ontology/'):
                types.append(tipo[28:])
    return types

def extract_abstract(entity):
        # consulta para recuperar o resumo
        query = "PREFIX dbpedia-owl: <http://dbpedia.org/ontology/> " \
                " select * where" \
                " { <http://dbpedia.org/resource/" + entity + "> dbpedia-owl:abstract ?abstract " \
                                                              "filter(langMatches(lang(?abstract),\"en\")) }"

        # extrair o resumo para uma variável
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        for result in results["results"]["bindings"]:
            for key, value in result.items():
                abstract = (value['value'].replace("\n", ''))
                return abstract

def main(dataset):
    result = []
    for i in tqdm(range(len(dataset))):
        entidade = dataset[i]
        types = extract_types(entidade)
        abstract = extract_abstract(entidade)
        result.append([])
        result[i].append(entidade)
        result[i].append(types)
        result[i].append(abstract)
        #print(result[i])

    # gerando csv de saída...
    colunas = ['entity', 'types','abstract']
    df = pd.DataFrame(result, columns=colunas)
    df.to_csv('output_abstract_AAUP.csv')  # modificar nome

dados = merge_entities(file_txt, file_csv)
main(dados)

