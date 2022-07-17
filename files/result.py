import collections
from distutils.command.build import build
from gc import collect
from typing import Type
import pymongo 
from pymongo import MongoClient
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



client = pymongo.MongoClient("mongodb+srv://ramam:ramnight@cluster0.wy9d4.mongodb.net/?retryWrites=true&w=majority")
db = client.netflix
collection = db.movies



def clean_category_data(txt):
    array = txt.replace(",","").split()
    if 'Movies' in array:
        array.remove('Movies')
    if '&' in array:
        array.remove('&')
    return array

def check_intersection(categories1 , categories2):
    flag = False
    for cat in categories1:
        if cat in categories2:
            flag = True
    return flag


def data_distribution_pie():
    positive_data = collection.count_documents({'netflix':0})
    negative_data =  collection.count_documents({'netflix':1}) 

    numberOfRecords = positive_data + negative_data
    labels = "Similar", "Not similar"
    sizes = [positive_data, negative_data]
    explode = (0.1, 0)

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True,colors=['#E50914', 'gray'] , startangle=90)
    ax1.axis('equal')  
    plt.title('Data distribution')
    plt.xlabel(str(numberOfRecords) + ' Movies')
    plt.savefig('pie.png')
    plt.clf()

#build confusion matrix
def build_confusion_mat_for_same_genre(decisionBoundary):   
    data = collection.find({})
    truePositive = 0
    falsePositive = 0
    trueNegative = 0
    falseNegative = 0
    numberOfChecked = 0
    for i, row in enumerate(data):
        if check_intersection(clean_category_data(row['second_movie_genre']), clean_category_data(row['first_movie_genre'])):
            numberOfChecked += 1
            if row['score'] >= decisionBoundary and row['netflix'] == 1:
                truePositive += 1
            if row['score'] >= decisionBoundary and row['netflix'] == 0:
                falseNegative += 1
            if row['score'] <= decisionBoundary and row['netflix'] == 1:
                falsePositive += 1
            if row['score'] <= decisionBoundary and row['netflix'] == 0:
                trueNegative += 1

    cf_matrix = [[truePositive, falsePositive], 
    [falseNegative, trueNegative]]
    return {'TP': truePositive , 'FP': falsePositive , 'TN':trueNegative, 'FN': falseNegative, 'cf_matrix': cf_matrix}

def build_confusion_mat(decisionBoundary):   
    data = collection.find({})
    truePositive = 0
    falsePositive = 0
    trueNegative = 0
    falseNegative = 0
    numberOfChecked = 0
    for i, row in enumerate(data):
        numberOfChecked += 1
        if row['score'] >= decisionBoundary and row['netflix'] == 1:
            truePositive += 1
        if row['score'] >= decisionBoundary and row['netflix'] == 0:
            falseNegative += 1
        if row['score'] <= decisionBoundary and row['netflix'] == 1:
            falsePositive += 1
        if row['score'] <= decisionBoundary and row['netflix'] == 0:
            trueNegative += 1

    cf_matrix = [[truePositive, falsePositive], 
    [falseNegative, trueNegative]]
    return {'TP': truePositive , 'FP': falsePositive , 'TN':trueNegative, 'FN': falseNegative, 'cf_matrix': cf_matrix}

def print_cf_matrix(decisionBoundary, same_genre = False):
    #same genre build confusion matrix only if two movies have same genre
    if same_genre:
        cf_matrix = build_confusion_mat_for_same_genre(decisionBoundary)['cf_matrix']
    else:
        cf_matrix = build_confusion_mat(decisionBoundary)['cf_matrix']
    ax = sns.heatmap(cf_matrix, annot=True, cmap='Blues',  fmt='g')
    ax.set_title('Confusion Matrix for desicion boundery:'+str(decisionBoundary)+'\n\n');
    ax.xaxis.tick_top()
    ax.set_xlabel('\nPredicted Values')
    ax.set_ylabel('Actual Values ')
    ax.xaxis.set_label_position('top') 
    ax.xaxis.set_ticklabels(['True','False'])
    ax.yaxis.set_ticklabels(['True','False'])
    if same_genre:
        plt.savefig('cf_sameGenre'+str(decisionBoundary)+'.png')
    else: 
        plt.savefig('cf_'+str(decisionBoundary)+'.png') 
    ax.clear()
 
def run_over_desicion_boundry():
    for decisionBoundary in np.linspace(0,1,11):
        print_cf_matrix(decisionBoundary)
       
def get_precision_recall(decisionBoundary, same_genre = False):
    if same_genre:
        conf_mat =  build_confusion_mat_for_same_genre(decisionBoundary)
    else: 
        conf_mat =  build_confusion_mat(decisionBoundary)
    precision = conf_mat['TP']/(conf_mat['TP'] + conf_mat['FP'])
    recall = conf_mat['TP']/(conf_mat['TP'] + conf_mat['FN'])
    return {'precision': "{:.2f}".format(precision) , 'recall':"{:.2f}".format(recall)}

def line_precision_recall():
    values = np.array([0.0 , 0.2 , 0.4 , 0.6 , 0.8 , 1.0])
    precision_list = []
    recall_list = []
    for val in values: 
        precision_list.append(float(get_precision_recall(val)['precision']))
        recall_list.append(float(get_precision_recall(val)['recall']))
    plt.plot(values, precision_list, linestyle= 'dashed', color= '#E50914',label = "Precision")
    plt.plot(values, recall_list, color = 'gray', label = "Recall")
    plt.legend()
    plt.savefig('recall_pressicion_line.png') 

