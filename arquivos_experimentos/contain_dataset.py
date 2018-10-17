import glob
import csv
import pandas as pd
from tqdm import tqdm

path = "dbpedia/treinamento/*.csv"
files = glob.glob(path)

# dataset experiments
file_txt = "entities_AAUP.txt"
with open(file_txt, "r") as arquivo:
    dataset = []
    for linha in arquivo:
        linha = linha.rstrip('\n')
        dataset.append(linha.replace('http://dbpedia.org/resource/', ''))

print('entidades arquivo...')
print(dataset)

data_true = []
contador = 0

print('verificando se entidades do arquivo estão contidos no csv...')
for file in tqdm(files):
    classe = file[20:].replace('.csv', '') # pegar só o nome do arquivo
    with open(file, encoding="utf8") as f:
        reader = csv.reader(f)
        for line in reader:
            entity = line[1].replace('DBPEDIA_ID/', '')
            if (entity in dataset) == True: # se a entidade estiver contida no dataset inclui na lista data_true
                data_true.append([])
                data_true[contador].append(entity)
                data_true[contador].append(classe)
                contador = contador+1
                # data_true.append(entity)

print('Entidades do dataset contidas nos arquivos...')
print(data_true)

# gerando csv de saída...
colunas = ['entity', 'class_target']
df = pd.DataFrame(data_true, columns=colunas)
df.to_csv('entities_AAUP_output.csv') # modificar nome
