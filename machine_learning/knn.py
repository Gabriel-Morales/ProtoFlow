import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
import numpy as np
import csv
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.model_selection import train_test_split
from sklearn import neighbors

#Read in dataset from ml_datasets 
df = pd.read_csv("ml_datasets/consolidated_z_b_w.csv")

#Drop rows with value of "empty" as a label
df = df[df.label != 'empty']

#remove 7500 routers from the input data
df_remove = df.query("label == 'router'").sample(n=7500)
df = df.drop(df_remove.index, axis=0)
df = df.reset_index()

#Drop unused categories from input data
df.drop(['protocol', 'index', 'src_oui', 'src_mac', 'dst_oui', 'dst_mac', 'src2dst_first_seen_time_ms', 'dst2src_first_seen_time_ms', 'src2dst_last_seen_time_ms', 'dst2src_last_seen_time_ms', 'bidirectional_first_seen_time_ms', 'bidirectional_last_seen_time_ms'], axis=1, inplace=True)


#Creating x and y dataframes
y = df
x = df.iloc[:,:-1]

#Create dictionary to define device types from encoder_key.csv
dict = {}
with open("encoder_key.csv", 'r') as dict_csv:
    reader = csv.reader(dict_csv)
    dict = {rows[1]:rows[0] for rows in reader}

y_encoded = y.replace({"label":dict})
y_encoded = np.array(y_encoded['label'])

# Split up into train/test sets
knn_test_size = .4

x_train, x_test, y_train, y_test = train_test_split(x, y_encoded, test_size = knn_test_size, random_state=0)
x_arr_train = np.array(x_train)
x_arr_test = np.array(x_test)
y_arr_train = np.array(y_train)
y_arr_test = np.array(y_test)

#select the knn model and set the values of it
num_neighbors = 20
weight_type = 'uniform'
algorithm_type = 'auto'
leaf_size_val = 5
p_val = 2.0


knn_classifier = neighbors.KNeighborsClassifier()

#Fit the model
knn_classifier.fit(x_arr_train, y_arr_train)
knn_training_score = knn_classifier.score(x_arr_train, y_arr_train)

#Test the model and create the metrics for analysis
knn_predictions = knn_classifier.predict(x_arr_test)
knn_accuracy_score = accuracy_score(y_arr_test, knn_predictions)
knn_recall_score = recall_score(y_arr_test, knn_predictions, average = 'weighted')
knn_precision_score = precision_score(y_arr_test, knn_predictions, average = 'weighted')
knn_f1_score = f1_score(y_arr_test, knn_predictions, average = 'weighted')

#collect metrics
metrics_file = pd.read_csv("knn_data.csv")
metrics_data = {'test_number':metrics_file['test_number'].iat[-1] + 1,
                'test_size':knn_test_size,
                'n_neighbors':num_neighbors,
                'weights':weight_type,
                'algorithm':algorithm_type,
                'leaf_size':leaf_size_val,
                'p':p_val,
                'accuracy_score':knn_accuracy_score,
                'precision_score':knn_precision_score,
                'recall_score':knn_recall_score,
                'f1_score':knn_f1_score}

#log metrics to a csv file
metrics_file = metrics_file.append(metrics_data, ignore_index=True)
print(metrics_file)
metrics_file.to_csv('knn_data.csv',index=False)

#print metrics for validation
print(f'knn Test Size: {knn_test_size * 100}%')
print(f'knn training score: {knn_training_score * 100}%')
print(f'knn accuracy score: {knn_accuracy_score * 100}%')
print(f'knn recall score: {knn_recall_score * 100}%')
print(f'knn precision score: {knn_precision_score * 100}%')
print(f'knn f1 score: {knn_f1_score * 100}%')

