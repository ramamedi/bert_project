
Files
***********
data.csv         - clean data that can convert to mongo DB.

createMongoDB.py - file have all the function that needed to create MongoDB.

bot.py           - template for bot that connect netflix, choose user, then read row from csv and then search for a similar movie
                   and write it to csv

embedding.py     - Run bert as a sentence embedder for each movie and write the embedding to CSV
                   Becuase the embedding work in chunks runNumber+'.csv' need to be the name of the input file

test.py          - File for run test while working

result.py        - Group of functions that print result 

*************
for create the DB run each step separately:

1) create_DB_base_csv - and pass file nane as arg 

2) delete_duplicate_data - delete duplicate data

3) create_negative_DB - to get some Negative result to DB for compare 

*************

The flow of the project were:

1) Create embedding for each Movie

2) Find similar movie for each Movie

3) Create MongoDB with pairs compare 

4) Using the score evaluate the model 