import pandas as pd
from transformers import AutoTokenizer, AutoModel
# from sklearn.metrics.pairwise import cosine_similarity
import torch

runNumber = 13
df_movie = pd.read_csv(str(runNumber)+'.csv')
df_movie = df_movie[df_movie['type'] == 'Movie']
# df_movie.describe(include='all')
print(len(df_movie))
numberOfMovie = len(df_movie) 


print('Number of movie is : '+ str(numberOfMovie))
print('cols:') 
print(df_movie.columns)

sentences = df_movie['description'].tolist()[0:numberOfMovie] # here i want all the data not only 20
model_name = "sentence-transformers/bert-base-nli-mean-tokens"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# initialize dictionary that will contain tokenized sentences
tokens = {'input_ids': [], 'attention_mask': []}

for sentence in sentences:
    # tokenize sentence and append to dictionary lists
    new_tokens = tokenizer.encode_plus(sentence, 
                                       max_length=512,          # 512 is the max for BERT
                                       truncation=True,         # if longer sentence
                                       padding='max_length',    # if shorter sentence
                                       return_tensors='pt')     # using pythorch
    #new_tokens will return dict with input_ids and attention_mask for each sentence
    tokens['input_ids'].append(new_tokens['input_ids'][0])              #the [0] just help with the structure thats neccecery
    tokens['attention_mask'].append(new_tokens['attention_mask'][0])    #the [0] just help with the structure thats neccecery

# reformat list of tensors into single tensor
tokens['input_ids'] = torch.stack(tokens['input_ids'])
tokens['attention_mask'] = torch.stack(tokens['attention_mask'])

outputs = model(**tokens)
embeddings = outputs.last_hidden_state
attention_mask = tokens['attention_mask'] #attention mask 1 - real token , 0 - padding token
mask = attention_mask.unsqueeze(-1).expand(embeddings.size()).float()
masked_embeddings = embeddings * mask
summed = torch.sum(masked_embeddings, 1)
summed_mask = torch.clamp(mask.sum(1), min=1e-9)

mean_pooled = summed / summed_mask
mean_pooled = mean_pooled.detach().numpy()
print(len(mean_pooled))
print(numberOfMovie)

embeddingList = ['none'] * (numberOfMovie)
for i in range(numberOfMovie):
    embeddingList[i] = ' '.join(str(e) for e in mean_pooled[i])

df_movie['embedding']= embeddingList
df_movie.to_csv('embedding'+str(runNumber)+'.csv',  encoding='utf-8')
print('done')
