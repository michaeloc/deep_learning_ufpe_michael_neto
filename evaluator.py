import pandas as pd;
import numpy as np;
import data_manager;
import model;

# parameters

# input file names
# the expected label for classification should be named "label"; for regressions should be called "rating"
# the id should be named "DBpedia_URI15"

vectors_file = 'data/cities_entities_200.txt'  # arquivo txt com os embbedings gerados anteriormente
gold_file = 'data/CitiesCompleteDataset15.tsv'

# the size of the vectors used
vec_size = 250


# classification=0;regression=1
# in case of regression, neg_mean_squared_error is used; to calculate RMSE simply calculate the root
task = 0
# model option: NB, SVM, KNN, LR, M5
modelName = "SVM"

# data manager
data = data_manager.data_manager.readData(vectors_file, gold_file, vec_size, task)
data = data.sample(frac=1).reset_index(drop=True)

# initialize the model
model = model.Model(task, modelName)
# train and print score
model.train(data)
