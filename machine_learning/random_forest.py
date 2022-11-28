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
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

#Read in dataset from ml_datasets 
df = pd.read_csv("ml_datasets/consolidated_z_b_w.csv")

#df2 is unencrypted data
df2 = pd.read_csv("ml_datasets/unswiotan18_labelled_classified_formatted.csv")

df.reset_index(drop=True,inplace=True)
df2.reset_index(drop=True,inplace=True)

#merge encrypted and unencrypted dataframes
df = pd.concat([df,df2])
#Drop rows with value of "empty" as a label
df = df[df.label != 'empty']

#remove 7500 routers from the input data

df_remove = df.query("label == 'router'").sample(n=7500)
df = df.drop(df_remove.index, axis=0)

#Drop unused categories from input data
df.drop(['protocol', 'src_oui', 'src_mac', 'dst_oui', 'dst_mac', 'src2dst_first_seen_time_ms', 'dst2src_first_seen_time_ms', 'src2dst_last_seen_time_ms', 'dst2src_last_seen_time_ms','bidirectional_first_seen_time_ms','bidirectional_last_seen_time_ms','dst2src_transmission_rate_bytes_ms'], axis=1, inplace=True)

#df.to_csv('test.csv')
df = df.dropna()
#df.to_csv('dropnatest.csv')
df = df.sample(frac=1).reset_index(drop=True)

#Creating x and y dataframes
y = df
x = df.iloc[:,:-1]

#Create dictionary to define device types from encoder_key.csv
dict = {}
    #with open("encoder_key.csv", 'r') as dict_csv:
    #    reader = csv.reader(dict_csv)
    #    dict = {rows[1]:rows[0] for rows in reader}

y_encoded = y.replace({"label":dict})
y_encoded = np.array(y_encoded['label'])

# Split up into train/test sets
rfc_test_size = .2

x_train, x_test, y_train, y_test = train_test_split(x, y_encoded, test_size = rfc_test_size, random_state=0)
x_arr_train = np.array(x_train)
x_arr_test = np.array(x_test)
y_arr_train = np.array(y_train)
y_arr_test = np.array(y_test)

#select the RFC model and set the values of it
rfc_max_depth = 11
rfc = RandomForestClassifier(max_depth=rfc_max_depth, random_state=0)

#Fit the model
rfc.fit(x_arr_train, y_arr_train)
rfc_training_classification_correctness = rfc.score(x_arr_train, y_arr_train)

#Test the model and create the metrics for analysis
rfc_predictions = rfc.predict(x_arr_test)
rfc_accuracy_score = accuracy_score(y_arr_test, rfc_predictions)
rfc_recall_score = recall_score(y_arr_test, rfc_predictions, average = 'weighted')
rfc_precision_score = precision_score(y_arr_test, rfc_predictions, average = 'weighted')
rfc_f1_score = f1_score(y_arr_test, rfc_predictions, average = 'weighted')

#collect and print class metrics
class_metrics = classification_report(y_arr_test,rfc_predictions)
print(class_metrics)

#collect metrics
metrics_file = pd.read_csv("random_forest_data.csv")
metrics_data = {'test_number':metrics_file['test_number'].iat[-1] + 1,
                'test_size':rfc_test_size,
                'max_depth':rfc_max_depth,
                'accuracy_score':rfc_accuracy_score,
                'precision_score':rfc_precision_score,
                'recall_score':rfc_recall_score,
                'f1_score':rfc_f1_score}

#log metrics to a csv file
metrics_file = metrics_file.append(metrics_data, ignore_index=True)
#metrics_file.to_csv('random_forest_data.csv',index=False)

#print metrics for validation
print(f'RFC Max Depth: {rfc_max_depth}')
print(f'RFC Test Size: {rfc_test_size * 100}%')
print(f'RFC correctness classification: {rfc_training_classification_correctness * 100}%')
print(f'RFC accuracy score: {rfc_accuracy_score * 100}%')
print(f'RFC recall score: {rfc_recall_score * 100}%')
print(f'RFC precision score: {rfc_precision_score * 100}%')
print(f'RFC f1 score: {rfc_f1_score * 100}%')

