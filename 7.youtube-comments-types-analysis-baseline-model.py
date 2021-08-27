#!/usr/bin/env python
# coding: utf-8

# # Análise de sentimento - Comentários de produtos eletrônicos do youtube - Armazenamento no Firebase

# In[62]:


from datetime import datetime
import pandas as pd
import time
import numpy as np


import stop_words
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.model_selection import train_test_split, GridSearchCV, KFold
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC, LinearSVC
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.datasets import make_classification
from scikitplot.metrics import plot_confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import r2_score, mean_absolute_percentage_error
from yellowbrick.regressor import ResidualsPlot

import seaborn as sns
import imblearn
from collections import Counter
from sklearn.datasets import make_classification
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline
from numpy import where


from imblearn.over_sampling import RandomOverSampler
from imblearn.over_sampling import SMOTE 
# from imblearn.over_sampling import SMOTENC
# from imblearn.over_sampling import SMOTEN
from imblearn.over_sampling import ADASYN 
from imblearn.over_sampling import BorderlineSMOTE
from imblearn.over_sampling import KMeansSMOTE
from imblearn.over_sampling import SVMSMOTE 

from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm

from gensim.models import Word2Vec
from gensim.models import KeyedVectors
from sklearn.decomposition import LatentDirichletAllocation,TruncatedSVD
import nltk
from nltk.corpus import stopwords
import re

from catboost import CatBoostClassifier, Pool


# In[30]:


df = pd.read_csv('video_comments_final_types.csv')
df['final_type'].value_counts()


# In[31]:

# # Data Transform

# In[32]:


#default transformation
df['comment'] = df['comment'].astype(str)
df['final_type'] = df['final_type'].astype(int)


# In[33]:


def remove_punctuation(dfText):
    import re
    import string
    regex = re.compile('[%s]' % re.escape(string.punctuation)) #see documentation here: http://docs.python.org/2/library/string.html

    tokenized_docs_no_punctuation = []

    for review in dfText:
        # new_review = []
        new_review = ""
        for token in review:
            new_token = regex.sub(u'', token)
            if not new_token == u'':
                #new_review.append(new_token)
                new_review = new_review + new_token
            else:
                new_review = new_review + " "
        
        tokenized_docs_no_punctuation.append(new_review)
    return tokenized_docs_no_punctuation

def unicode_emoji(dfText):
    import emoji
    for emoj in emoji.UNICODE_EMOJI['pt']:
        dfText = dfText.str.replace(emoj, ' '+emoji.UNICODE_EMOJI['pt'][emoj]+' ', regex=False)
    return dfText

def normalize_utf8(dfText):
    return dfText.str.normalize("NFKD").str.encode("ascii", errors="ignore").str.decode("utf8")

def removing_stop_words(dfText):
    import nltk
    nltk.download('stopwords')
    stopwords = nltk.corpus.stopwords.words('portuguese') # removing stop words
    
    stopwords.append('q')
    stopwords.append('pra')
    stopwords.append('td')
    stopwords.remove('não')

    stopwords = pd.DataFrame(stopwords, columns=['normalized'])
    stopwords['normalized'] = stopwords['normalized'].str.normalize("NFKD").str.encode("ascii", errors="ignore").str.decode("utf8")

    stopword_data = []
    for idx,review in enumerate(dfText):
        new_phrase = ""
        for word in review.split(" "):
            # print(word)
            if  not stopwords['normalized'].str.match('^'+word+'$').any():
                new_phrase = new_phrase + " " + word

        stopword_data.append(new_phrase)

    return stopword_data

def portuguese_stemmer(dfText):
    # #!pip install git+git://github.com/snowballstem/pystemmer
    import Stemmer
    stemmer = Stemmer.Stemmer('portuguese')

    stemmer_docs = []
    for phrase in dfText:
        stemmer_docs.append(' '.join(stemmer.stemWords(phrase.split(" "))))

    return stemmer_docs

def excess_space_remover(dfText):
    all_commnets_list = dfText.to_list()

    for i in range(len(all_commnets_list)):
        all_commnets_list[i] = re.sub(r"\s+", " ", all_commnets_list[i])

    return all_commnets_list

def lower_case(dfText):
    return dfText.str.lower()


# In[34]:


df['transformed_comment'] = lower_case(df['comment']) 
df['transformed_comment'] = remove_punctuation(df['transformed_comment']) 
df['transformed_comment'] = unicode_emoji(df['transformed_comment'])
df['transformed_comment'] = normalize_utf8(df['transformed_comment'])
df['transformed_comment'] = removing_stop_words(df['transformed_comment'])
df['transformed_comment'] = portuguese_stemmer(df['transformed_comment'])
df['transformed_comment'] = excess_space_remover(df['transformed_comment'])


# # Imbalance Apply

# In[35]:


def overSamplDef(X_res, y_res, overMethod, sampling_strategy='auto'):
    from collections import Counter
    from imblearn.over_sampling import RandomOverSampler
    from imblearn.over_sampling import SMOTE 
    # from imblearn.over_sampling import SMOTENC
    from imblearn.over_sampling import SMOTEN
    from imblearn.over_sampling import ADASYN 
    from imblearn.over_sampling import BorderlineSMOTE
    from imblearn.over_sampling import KMeansSMOTE
    from imblearn.over_sampling import SVMSMOTE 
    
    print(sampling_strategy)

    print('Before dataset shape %s' % sorted(Counter(y_res).items()))
    ros = overMethod(sampling_strategy=sampling_strategy)
    # ros = BorderlineSMOTE()
    # sampling_strategy='minority'
    # ros = SMOTE()
    X_res, y_res = ros.fit_resample(X_res, y_res)

    print('Resampled dataset shape %s' % sorted(Counter(y_res).items()))
    print("-------------------------------------------")
    return X_res, y_res


# # Create Freatures

# In[36]:


# required_columns = 'comment'
required_columns = 'transformed_comment'
le = LabelEncoder()

X = df[required_columns]
y = le.fit_transform(df['final_type'])


# ## Word2Vec

# In[37]:


all_commnets_list = df[required_columns].to_list()

tokenized_words = []

for i in range(len(all_commnets_list)):
    #tokenize the text to list of sentences
    tokenized_sentence = nltk.sent_tokenize(all_commnets_list[i])
    #tokenize the list of sentences to list of words
    tokenized = [nltk.word_tokenize(sentence) for sentence in tokenized_sentence]
    #remove the stop words from the text
    for y, _ in enumerate(tokenized):
        tokenized_words.append([word for word in tokenized[y]])

all_commnets_list = tokenized_words

model = Word2Vec(all_commnets_list, min_count=1)


# In[38]:


model.wv.save('eletronics_model.bin')
# import fasttext.util
embeddings = KeyedVectors.load('eletronics_model.bin')


# In[39]:


word2vec_doc_vec = pd.DataFrame()
for phrase in all_commnets_list:
  temp = pd.DataFrame()

  for word in phrase:
    try:
      word_vec = embeddings[word]
      temp = temp.append(pd.Series(word_vec), ignore_index = True)
    except:
      pass
  doc_vector = temp.mean()
  word2vec_doc_vec = word2vec_doc_vec.append(doc_vector, ignore_index = True)

word2vec_doc_vec.shape
X_w2v = word2vec_doc_vec


# tfidf_v = TfidfVectorizer(ngram_range = (3, 3))
tfidf_v = TfidfVectorizer(ngram_range = (2, 3))
#matrixTFIDF= tfidf_v.fit_transform(train.question_text)
matrixTFIDF= tfidf_v.fit_transform(df[required_columns])
svd=TruncatedSVD(n_components=100, n_iter=20, algorithm='randomized')
X_lsa=svd.fit_transform(matrixTFIDF) 



# model_report = pd.DataFrame()
# predict_w2v_traning = []
# predict_lsa_traning = []

# for exec in range(100):
#     param_grid = [
#         {'C': [1, 10, 100, 1000]}
#     ] 
#     svc = LinearSVC()

#     X_train_w2v, X_test_w2v, y_train_w2v, y_test_w2v = train_test_split(X_w2v, df['final_type'], test_size = .2)
#     X_train_w2v, y_train_w2v = overSamplDef(X_train_w2v, y_train_w2v, ADASYN, sampling_strategy='minority') #SMOTE | SMOTE
#     clf = GridSearchCV(svc, param_grid).fit(X_train_w2v, y_train_w2v)
#     y_pred_w2v = clf.predict(X_test_w2v)

#     X_train_lsa, X_test_lsa, y_train_lsa, y_test_lsa = train_test_split(X_lsa, df['final_type'], test_size = .2)
#     X_train_lsa, y_train_lsa = overSamplDef(X_train_lsa, y_train_lsa, ADASYN, sampling_strategy='minority') #SMOTE | SMOTE
#     clf = GridSearchCV(svc, param_grid).fit(X_train_lsa, y_train_lsa)
#     y_pred_lsa = clf.predict(X_test_lsa)

#     svc_w2v = classification_report(y_test_w2v, y_pred_w2v, output_dict=True)
#     predict_w2v_traning.append(svc_w2v)

#     svc_lsa = classification_report(y_test_lsa, y_pred_lsa, output_dict=True)
#     predict_lsa_traning.append(svc_lsa)

# model_w2v_report = pd.json_normalize(predict_w2v_traning)
# model_lsa_report = pd.json_normalize(predict_lsa_traning)

# model_w2v_report.to_csv('w2v_report.csv', index=False)
# model_lsa_report.to_csv('lsa_report.csv', index=False)


