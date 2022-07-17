import collections
import pymongo 
import numpy as np
import pandas as pd
from pymongo import MongoClient
from regex import P
# from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats import pearsonr



def SringMoviesToArray(StrMovies):    
    array = StrMovies.replace("\\", "").replace("'","").replace('"', "").replace("[", "").replace("]","").split(",")
    removeWhiteSpace = []
    removeWhiteSpace.append(array[0])
    for i in range(1,len(array)):
        removeWhiteSpace.append(array[i][1:])
    return removeWhiteSpace

def StringEmbeddingToNumpyArray(strVal):
    return np.fromstring(strVal, dtype='f', sep=' ')

def similarty_check(movie_name1, movie_name2, df):  
    df = df.reset_index()
    df_embedding1 = str(df.loc[df['title'] == movie_name1]['embedding'].values)[2:-2]
    embedding1 = StringEmbeddingToNumpyArray(df_embedding1)
    
    df_embedding2 = str(df.loc[df['title'] == movie_name2]['embedding'].values)[2:-2]
    embedding2 = StringEmbeddingToNumpyArray(df_embedding2)
    
    corr, _ = pearsonr(embedding1, embedding2)
    return corr


def genre_check(movie_name, df):
    df = df.reset_index()
    genres = df.loc[df['title'] == movie_name]['listed_in'].values
    return str(genres)[2:-2]



def create_DB_base_csv(file_name):
    df = pd.read_csv (file_name)
    indexForDB = 0
    for index, row in df.iterrows():
        name = row['title']
        genre = row['listed_in']
        similar_movies = SringMoviesToArray(row['similar_movie'])
        for similar_mov in similar_movies:
            id = name + '$' + similar_mov
            if similar_mov in df['title'].array:
                myscore = similarty_check(name , similar_mov , df)
                second_movie_genre = genre_check(similar_mov , df)
                netflix = 1
                collection.insert_one({'_id': id, 
                'serial_id': indexForDB,
                'movie1': name,
                'movie2': similar_mov,
                'first_movie_genre': genre, 
                'second_movie_genre': second_movie_genre,
                'score': float(myscore),
                'netflix': netflix  
                })
                indexForDB += 1


def delete_duplicate_data():
    data = collection.find({})
    for doc in data:
        movie1 = doc['movie1']
        movie2 = doc['movie2']
        collection.delete_many({'movie1': movie2 , 'movie2' : movie1 })


def create_negative_DB(file_name):
    df = pd.read_csv (file_name)
    indexForDB = 0
    indexHere = 0
    for index, row in df.iterrows():
        name = row['title']
        genre = row['listed_in']
        sample = df.sample()
        sample_name = sample['title'].values[0]
        similar_movies = SringMoviesToArray(row['similar_movie'])
        if sample_name not in similar_movies:
            id = name + '$' + sample_name
            if sample_name in df['title'].array: 
                indexHere += 1
                myscore = similarty_check(name , sample_name , df)
                second_movie_genre = genre_check(sample_name , df)
                netflix = 0
                collection.insert_one({'_id': id, 
                'serial_id': indexForDB,
                'movie1': name,
                'movie2': sample_name,
                'first_movie_genre': genre, 
                'second_movie_genre': second_movie_genre,
                'score': float(myscore),
                'netflix': netflix  
                })
                indexForDB += 1
    
def sanity_check_print_duplicate_data():
    pairs = collection.find({})
    for pair in pairs:
        movie1 =  pair['movie1']
        movie2 =  pair['movie2']
        obj = collection.find({'movie1': movie2 , 'movie2':movie1})
        for item in obj:
            print(pair)
            print('vs')
            print(item)
    print('done sanity check')

#connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://ramam:ramnight@cluster0.wy9d4.mongodb.net/?retryWrites=true&w=majority")
db = client.netflix
collection = db.movies



#Clear DB before start
# collection.delete_many({})

#Create DB
# create_DB_base_csv('data.csv')
# delete_duplicate_data()
# create_negative_DB('data.csv')

# print('done')