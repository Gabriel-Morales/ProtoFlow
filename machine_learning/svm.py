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
from sklearn import svm
from sklearn.metrics import classification_report

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
svm_test_size = .2

x_train, x_test, y_train, y_test = train_test_split(x, y_encoded, test_size = svm_test_size, random_state=0)
x_arr_train = np.array(x_train)
x_arr_test = np.array(x_test)
y_arr_train = np.array(y_train)
y_arr_test = np.array(y_test)

max_iterations = 1250
dual_bool = False
C_val = 1.25
penalty_type = 'l1'

#select the SVM model and set the values of it
svm_classifier = svm.LinearSVC(max_iter=max_iterations,dual=dual_bool,C=C_val,penalty=penalty_type)

#Fit the model
svm_classifier.fit(x_arr_train, y_arr_train)
svm_training_score = svm_classifier.score(x_arr_train, y_arr_train)

#Test the model and create the metrics for analysis
svm_predictions = svm_classifier.predict(x_arr_test)
svm_accuracy_score = accuracy_score(y_arr_test, svm_predictions)
svm_recall_score = recall_score(y_arr_test, svm_predictions, average = 'weighted')
svm_precision_score = precision_score(y_arr_test, svm_predictions, average = 'weighted')
svm_f1_score = f1_score(y_arr_test, svm_predictions, average = 'weighted')

#collect and print class metrics
class_metrics = classification_report(y_arr_test,svm_predictions)
print(class_metrics)

#collect metrics
metrics_file = pd.read_csv("svm_data.csv")
metrics_data = {'test_number':metrics_file['test_number'].iat[-1] + 1,
                'max_iter':max_iterations,
                'dual':dual_bool,
                'c':C_val,
                'penalty':penalty_type,
                'test_size':svm_test_size,
                'accuracy_score':svm_accuracy_score,
                'precision_score':svm_precision_score,
                'recall_score':svm_recall_score,
                'f1_score':svm_f1_score}

#log metrics to a csv file
metrics_file = metrics_file.append(metrics_data, ignore_index=True)
print(metrics_file)
#metrics_file.to_csv('svm_data.csv',index=False)

#print metrics for validation
print(f'SVM Test Size: {svm_test_size * 100}%')
print(f'SVM training score: {svm_training_score * 100}%')
print(f'SVM accuracy score: {svm_accuracy_score * 100}%')
print(f'SVM recall score: {svm_recall_score * 100}%')
print(f'SVM precision score: {svm_precision_score * 100}%')
print(f'SVM f1 score: {svm_f1_score * 100}%')

