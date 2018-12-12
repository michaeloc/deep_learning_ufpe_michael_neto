import numpy as np
import csv

file_embeddings = 'cities_embeddings_400w2v_layer_duplicated_250fc1.npy' # caminho do arquivo de embeddings
file_txt = 'data/cities_sg_200_4.txt' # caminho do arquivo com as entidades do experimento

data = np.load(file_embeddings)

# capturar a url de cada entidade
with open(file_txt, "r") as file:
    entities = []
    for line in file:
        entity_line = line.split('\t')
        entities.append(entity_line[0])

dataset = []
for i in range(len(entities)):
    tuple = []
    entity_search = entities[i].replace('http://dbpedia.org/resource/', 'dbo:')
    entity = entities[i]
    embedding = data.item().get(entity_search)
    if (embedding is not None):
        tuple.append(entity)
        for j in range(len(embedding)):
            tuple.append(embedding[j])
        dataset.append(tuple)

arquivo_saida = 'cities_entities_3.txt' # nome do arquivo de saída
with open(arquivo_saida, "w") as output:
    writer = csv.writer(output, lineterminator='\n', delimiter='\t')
    writer.writerows(dataset)



