import pandas as pd;
import numpy as np;

class data_manager:
    def __init__(self):
        print("initiated")

    @staticmethod
    def createHeaders(vec_size):
        headers = ['id']
        for i in range(0, vec_size):
            headers.append(i)
        return headers

    @staticmethod
    def readData(vectors_file, gold_file,vec_size, task):
        vectors = pd.read_csv(vectors_file, "\t", names=data_manager.createHeaders(vec_size))

        fields = ['DBpedia_URI15', 'label']
        if task==1:
            fields = ['DBpedia_URI15', 'rating']
        gold = pd.read_csv(gold_file, "\t", usecols=fields, encoding='latin1')
        gold.rename(columns={'DBpedia_URI15': 'id'}, inplace=True)
        if task == 1:
            gold.rename(columns={'rating': 'label'}, inplace=True)
        merged = gold.merge(vectors, on='id', how='inner')
        return merged
