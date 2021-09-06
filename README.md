# Análise de sentimento - Comentários de produtos eletrônicos do youtube - Armazenamento no Firebase


```python
from datetime import datetime
import pandas as pd
import time
import numpy as np
import matplotlib.pyplot as plt


# import stop_words
# from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.model_selection import train_test_split, GridSearchCV
# from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
# from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
# from sklearn.datasets import make_classification
# from scikitplot.metrics import plot_confusion_matrix
from sklearn.metrics import classification_report
# from sklearn.metrics import r2_score, mean_absolute_percentage_error
from yellowbrick.regressor import ResidualsPlot

import seaborn as sns
import imblearn
from collections import Counter
from sklearn.datasets import make_classification
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline
from matplotlib import pyplot
import numpy
from scikitplot.metrics import plot_confusion_matrix

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

import warnings
warnings.filterwarnings('ignore')

import matplotlib.pyplot as plt
%matplotlib inline

from catboost import CatBoostClassifier, Pool
from wordcloud import WordCloud
```


```python
comments_site_analysis = pd.read_csv('comments_site_analysis.csv')
```


```python
phones_colleted = pd.read_csv("phones_colleted.csv")
```


```python
#default transformation
df = pd.read_csv('video_comments_final_types2.csv')
df['comment'] = df['comment'].astype(str)
df['final_type'] = df['final_type'].astype(int)
```

# 1 Exposição do problema

Observando o volume de análises de celulares eletrônicos no youtube e sua popularidade de comentários, notei a possibilidade de efetuar uma categorização dos comentários desses vídeos a fim de conseguir uma indicação sobre quais os celulares são mais bem ou mal recebidos pelo público. Trazendo uma expectativa popular sobre os mesmos. 

Temos assim como objetivo do modelo indicar quais são os comentários negativos e positivos das análises dos celulares, ou seja, seu valor de recall para comentários negativos e positivos.

O maior desafio para este processo é a forma de categorizar a base principal dos dados para o treino do meu modelo. Os comentários dos vídeos do youtube possuem somente a opção “like” que não define se o mesmo é positivo ou negativo, somente se o comentário foi aceito pela maioria ou não. Algumas tentativas de utilização de APIs para definição desta base como o google natural language api foram utilizadas, porém com resultados bastante insatisfatórios. 


# 2 Coleta dos dados

## 2.1 Levantamento dos produtos eletônicos

Foi selecionado um total de 26 celulares para a análise com base nos lançamentos de 2020 e 2021 mais populares pelas suas faixas de preços. Coletei um total de 10 mil comentários para a base de dados. 


```python
phones_colleted
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Celular</th>
      <th>Faixa de preço até</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Samsung Galaxy A10s</td>
      <td>1000</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Moto E7</td>
      <td>1000</td>
    </tr>
    <tr>
      <th>2</th>
      <td>LG K22</td>
      <td>1000</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Xiaomi Redmi 9</td>
      <td>1000</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Philco Hit Max</td>
      <td>1000</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Motorola Moto G9 Power</td>
      <td>2000</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Samsung Galaxy M31</td>
      <td>2000</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Motorola One Fusion Plus</td>
      <td>2000</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Samsung Galaxy A71</td>
      <td>2000</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Poco X3 NFC</td>
      <td>2000</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Redmi Note 9S</td>
      <td>2000</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Samsung Galaxy M51</td>
      <td>2500</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Samsung Galaxy Note 10 Lite</td>
      <td>2500</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Xiaomi Mi 10 Lite 5G</td>
      <td>2500</td>
    </tr>
    <tr>
      <th>14</th>
      <td>LG Velvet</td>
      <td>2500</td>
    </tr>
    <tr>
      <th>15</th>
      <td>iPhone SE</td>
      <td>2500</td>
    </tr>
    <tr>
      <th>16</th>
      <td>Samsung Galaxy Note 10</td>
      <td>3000</td>
    </tr>
    <tr>
      <th>17</th>
      <td>Samsung Galaxy S20</td>
      <td>3000</td>
    </tr>
    <tr>
      <th>18</th>
      <td>Galaxy S20 FE</td>
      <td>3000</td>
    </tr>
    <tr>
      <th>19</th>
      <td>Xiaomi Mi 10T Lite</td>
      <td>3000</td>
    </tr>
    <tr>
      <th>20</th>
      <td>Motorola Edge/Edge+</td>
      <td>3000+</td>
    </tr>
    <tr>
      <th>21</th>
      <td>iPhone 12</td>
      <td>3000+</td>
    </tr>
    <tr>
      <th>22</th>
      <td>ASUS ROG Phone 3</td>
      <td>3000+</td>
    </tr>
    <tr>
      <th>23</th>
      <td>Galaxy S21 Ultra</td>
      <td>3000+</td>
    </tr>
    <tr>
      <th>24</th>
      <td>Xiaomi Mi 10T/10T Pro</td>
      <td>3000+</td>
    </tr>
    <tr>
      <th>25</th>
      <td>Galaxy Z Fold 2</td>
      <td>3000+</td>
    </tr>
  </tbody>
</table>
</div>



## 2.2 Levantamento da pesquisa e filtro dos vídeos

Considerei que a melhor maneira de encontrar os reviews dos produtos é por meio da pesquisa com o título “ ‘marca + modelo’ análise" em português para vídeos enviados até 12 meses atrás e com no mínimo 50 mil visualizações. Espera-se que ao menos 5 vídeos de cada aparelho sejam analisados.

## 2.3 Coleta das informações

Como evidenciado na exposição do problema não tínhamos uma forma existente de coleta desses comentários já classificados no youtube. Para isso criou-se então um site de classificação dos comentários aberto ao público. O mesmo pode ser visualizado através do [link](https://comments-reviews-web-app.vercel.app/). A mesma tem a seguinte interface:


```python
from IPython.display import display, Image
display(Image(filename='site_example.png'))
```


    
![png](youtube-comments-types-analysis-complete-review_files/youtube-comments-types-analysis-complete-review_15_0.png)
    


A interface contem os seguintes requisitos funcionais e técnicos:

### 2.3.1 Criada em Reactjs e os dados são armazenados por meio do Firebase;

### 2.3.2 A seleção dos comentários para os usuários foi de forma aleatória e com pesos. Onde os comentários menos avaliados pelos usuários tinham um peso maior para serem trazidos com maior probabilidade antes dos mais avaliados;

### 2.3.3 Cada usuário que fez a avaliação será diferenciado pelo IP ou um timestamp da página aberta no momento a fim de contabilizar o experimento;

### 2.3.4 Um total de 10 mil comentários foram armazenados na ferramenta.

# 3.1 Preparação dos dados

Após a criação do site para a coleta de avaliações, monitorei os dados coletados e avaliados pelos usuários. Meu número final de comentários avaliados foi o evidenciado abaixo: 


```python
comments_site_analysis
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Unnamed: 0</th>
      <th>data</th>
      <th>comentarios avaliados</th>
      <th>comentarios avaliados %</th>
      <th>comentários com 2</th>
      <th>comentários com 3</th>
      <th>comentários com 1</th>
      <th>comentários com 4</th>
      <th>comentários com 5</th>
      <th>comentários com 6</th>
      <th>comentarios avaliados totais</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>06/09/2021 10:36:01</td>
      <td>4908</td>
      <td>49.08</td>
      <td>1142</td>
      <td>232</td>
      <td>3491</td>
      <td>35</td>
      <td>7</td>
      <td>1</td>
      <td>6652</td>
    </tr>
  </tbody>
</table>
</div>



Com os comentários avaliados, efetuei então a coleta dos dados. Os detalhes do mesmo utilizando a API do firebase podem ser encontrados em "5.youtube-review-comment-collect.ipynb". O mesmo não será exposto aqui a fim de condensar o processo.

Após a coleta dos dados do Firebase e sua manipulação, os seguintes dados foram coletados:


```python
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>comments_id</th>
      <th>comment-date</th>
      <th>comment-author</th>
      <th>comment</th>
      <th>comment-likes</th>
      <th>video-id</th>
      <th>video-title</th>
      <th>video-date</th>
      <th>video-link</th>
      <th>video-likes</th>
      <th>video-views</th>
      <th>video-channel</th>
      <th>video-comment-count</th>
      <th>final_type</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.UgwozCGH-HDyIES2ciF4AaABAg</td>
      <td>2020-12-20T22:44:18Z</td>
      <td>POP 0stras</td>
      <td>Uma porcaria. Comprei faz 3 meses. Muito arrep...</td>
      <td>0</td>
      <td>jSv8fxe3_KU</td>
      <td>GALAXY NOTE 10 LITE, FAZ SENTIDO COMPRAR? [Han...</td>
      <td>2020-02-19T16:00:09Z</td>
      <td>https://www.youtube.com/watch?v=jSv8fxe3_KU</td>
      <td>18773</td>
      <td>307422</td>
      <td>Canaltech</td>
      <td>1013</td>
      <td>-1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>3.Ugzuo_fNCeU10B0Iqv54AaABAg</td>
      <td>2021-04-19T01:28:56Z</td>
      <td>tout a commencé en France</td>
      <td>Assistindo com o meu a51 e agora estou querend...</td>
      <td>10</td>
      <td>6LwYbm71AJM</td>
      <td>Review GALAXY S21 ULTRA! Agora sim a SAMSUNG f...</td>
      <td>2021-04-07T22:00:01Z</td>
      <td>https://www.youtube.com/watch?v=6LwYbm71AJM</td>
      <td>5287</td>
      <td>91701</td>
      <td>Be!Tech</td>
      <td>430</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>4.UgzaPxJpaltmYRPm7WZ4AaABAg</td>
      <td>2021-06-03T22:58:59Z</td>
      <td>Tasio de Luanda Luanda</td>
      <td>Bom eu tenho problemas e com poeira água e queda</td>
      <td>0</td>
      <td>5JWFHfF4nGg</td>
      <td>SAMSUNG GALAXY M31 // um INTERMEDIÁRIO com 600...</td>
      <td>2020-07-09T21:19:36Z</td>
      <td>https://www.youtube.com/watch?v=5JWFHfF4nGg</td>
      <td>22040</td>
      <td>304881</td>
      <td>EscolhaSegura</td>
      <td>1413</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>5.Ugxg7N1mhRETPeDd0jB4AaABAg</td>
      <td>2021-03-04T02:37:38Z</td>
      <td>ᴘ ʀ ɪ ɴ ᴄ ᴇ s ᴀッ™</td>
      <td>Se no Samsung vier os emoji do iPhone eu me re...</td>
      <td>0</td>
      <td>vOVz5rPk2vU</td>
      <td>GALAXY NOTE 10 e GALAXY NOTE 10 PLUS!</td>
      <td>2019-08-07T23:00:51Z</td>
      <td>https://www.youtube.com/watch?v=vOVz5rPk2vU</td>
      <td>196838</td>
      <td>2130935</td>
      <td>Coisa de Nerd</td>
      <td>5604</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>6.Ugwxvye3XUXp-6GdwxV4AaABAg</td>
      <td>2021-03-03T20:09:55Z</td>
      <td>Eu Mesmo</td>
      <td>Smartphone gamer muito excelentente msm, mas f...</td>
      <td>0</td>
      <td>TdALKXTVZRU</td>
      <td>ROG PHONE 3: UNBOXING DO SMARTPHONE MAIS PODER...</td>
      <td>2020-07-22T15:30:08Z</td>
      <td>https://www.youtube.com/watch?v=TdALKXTVZRU</td>
      <td>62254</td>
      <td>942191</td>
      <td>Loop Infinito</td>
      <td>2266</td>
      <td>0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>4902</th>
      <td>9990.Ugz4MHAKLSZjySMHC8p4AaABAg</td>
      <td>2020-10-22T19:19:10Z</td>
      <td>Saulo Lima</td>
      <td>Entrada em cima , n gosto ! Gosto de entrada e...</td>
      <td>0</td>
      <td>uwlW-aTc5j4</td>
      <td>MOTOROLA EDGE+! O MELHOR MOTOROLA JA FEITO! Ma...</td>
      <td>2020-07-02T11:59:43Z</td>
      <td>https://www.youtube.com/watch?v=uwlW-aTc5j4</td>
      <td>11290</td>
      <td>117110</td>
      <td>Dudu Rocha</td>
      <td>835</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4903</th>
      <td>9993.Ugy9hH2G4Nq55fBuJ414AaABAg</td>
      <td>2020-12-06T20:06:26Z</td>
      <td>Andressa Tenório</td>
      <td>Sempre quis dizer isso.... assistindo do meu a...</td>
      <td>1</td>
      <td>w8ZokAmv8yE</td>
      <td>Review Samsung Galaxy A71: um celular intermed...</td>
      <td>2020-08-10T17:25:44Z</td>
      <td>https://www.youtube.com/watch?v=w8ZokAmv8yE</td>
      <td>15444</td>
      <td>257622</td>
      <td>TecMundo</td>
      <td>1155</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4904</th>
      <td>9995.UgzCH5fbhBklPp22nbd4AaABAg</td>
      <td>2021-06-29T03:21:41Z</td>
      <td>XTRAJ4DO FF 🇧🇷</td>
      <td>To doido pra ganhar o meu moto g9 play</td>
      <td>0</td>
      <td>kX2xqUDqfRA</td>
      <td>Motorola Moto G9 Play vs Moto G9 Power - QUAL ...</td>
      <td>2021-02-04T14:51:00Z</td>
      <td>https://www.youtube.com/watch?v=kX2xqUDqfRA</td>
      <td>20068</td>
      <td>290832</td>
      <td>Gesiel Taveira</td>
      <td>1108</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4905</th>
      <td>9997.Ugwu1TjlQHr-soAyagt4AaABAg</td>
      <td>2020-12-27T22:47:16Z</td>
      <td>Gu</td>
      <td>Mi 10t pro ou mi 10 pro?</td>
      <td>0</td>
      <td>MSqN27wR-gI</td>
      <td>MI 10T PRO: TOP de LINHA XIAOMI com PREÇO de I...</td>
      <td>2020-12-27T22:20:22Z</td>
      <td>https://www.youtube.com/watch?v=MSqN27wR-gI</td>
      <td>2286</td>
      <td>65595</td>
      <td>TudoCelular</td>
      <td>430</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4906</th>
      <td>9999.UgwIP04x6RP8Op4bg3R4AaABAg</td>
      <td>2021-05-25T19:08:07Z</td>
      <td>《Rodrigues》</td>
      <td>Pena q ele ñ pode amostrar os preços!;No Googl...</td>
      <td>0</td>
      <td>efbnQ2I3zIg</td>
      <td>CHEGOU! Motorola MOTO G9 POWER com FORÇA TOTAL...</td>
      <td>2020-12-10T12:00:09Z</td>
      <td>https://www.youtube.com/watch?v=efbnQ2I3zIg</td>
      <td>34967</td>
      <td>419324</td>
      <td>Gesiel Taveira</td>
      <td>1907</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
<p>4907 rows × 14 columns</p>
</div>



Onde "final_type" corresponde a classificação do comentário positivo (1), neutro(0) ou negativo(-1)

# 3.2 Transformação com técnicas de NLP

Meu objetivo aqui é padronizar meus comentários a fim de aplicar as tecnicas de criação de feature (LSA e Word2Vec). Defini funções para cada uma das etapadas da transformação, as mesmas são:

### 3.2.1. Transformar todos os comentários para letras minúculas;
### 3.2.2. Remover pontuações;
### 3.2.3. Transformar emojis para códigos. Exemplo: 
### 3.2.4. Normalização do texto em UTF-8
### 3.2.5. Remoção de stop words (excessão a palavra "não")
### 3.2.6. Estematização das palavras. Exemplo: 
### 3.2.7. Remoção de excesso de espaços (\n)


```python
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
```


```python
df['transformed_comment'] = lower_case(df['comment']) 
df['transformed_comment'] = remove_punctuation(df['transformed_comment']) 
df['transformed_comment'] = unicode_emoji(df['transformed_comment'])
df['transformed_comment'] = normalize_utf8(df['transformed_comment'])
df['transformed_comment'] = removing_stop_words(df['transformed_comment'])
df['transformed_comment'] = portuguese_stemmer(df['transformed_comment'])
df['transformed_comment'] = excess_space_remover(df['transformed_comment'])
```

    [nltk_data] Downloading package stopwords to
    [nltk_data]     C:\Users\erycm\AppData\Roaming\nltk_data...
    [nltk_data]   Package stopwords is already up-to-date!
    

# 4 Análise Exploratória

Após o tratamento das informações algumas análises foram feitas a fim de entender os dados. 


```python
df["comment-len"] = df["comment"].apply(lambda x: len(x))
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20,6))
axes[0].set_title("Histograma do tamanho de texto por comentário")
df["comment-len"].hist(ax=axes[0], bins=10)

df_grouped = df.groupby("final_type").agg({'comment-len': 'mean'}).reset_index()
df_grouped['desc'] = ["Negativo", "Neutro", "Positivo"]
df_grouped = df_grouped.rename(df_grouped['desc'])

df_grouped.plot.bar(
        y="comment-len",
        label='',
        color=['#dc3545','#ffc107','#218838'], 
        rot=1, 
        title="Media de tamanho do comentário por classificação",
        ax=axes[1])

plt.show()
```


    
![svg](youtube-comments-types-analysis-complete-review_files/youtube-comments-types-analysis-complete-review_30_0.svg)
    


Nota-se que a maioria dos comentários se encontram entre 0 à 400 caracteres. A média de tamanho por comentário positivo, negativo ou neutro é equilibrada.


```python
fig = df['final_type'].value_counts(normalize=True).plot.pie(
        autopct="%.2f",
        labels=["Positivo", "Neutro", "Negativo"],
        colors=['#218838','#ffc107','#dc3545'],
        fontsize=15,
        figsize=(10, 10),
        title="Distribuição dos comentários por classificação (%)",
        label="")

fig.axes.title.set_size(20)
```


    
![svg](youtube-comments-types-analysis-complete-review_files/youtube-comments-types-analysis-complete-review_32_0.svg)
    


Nota-se uma quantidade muito baixa de comentários negativos em nosso escopo de dados, além de uma quantidade muito grande de comentários positivos. Técnicas de balanceamento deverão ser utilizadas nesse modelo.


```python
wc = WordCloud(background_color='black', width = 3000, height = 2000, colormap='Set2', collocations=False)
#df['transformed_comment']
wc.generate(' '.join(df['transformed_comment']))

plt.axis("off")
plt.imshow(wc, interpolation="bilinear")
plt.show()
```


    
![svg](youtube-comments-types-analysis-complete-review_files/youtube-comments-types-analysis-complete-review_34_0.svg)
    


# 5. Modelagem

Através da análise exploratória, entende-se que a utilização de um método de balancemento dos dados será necessário. Para isso criei uma função genérica que aplica o método oversample aos dados que serão utilizados posteriormente.

## 5.1 Imbalance Apply


```python
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
    
    # print(sampling_strategy)

    print('Before dataset shape %s' % sorted(Counter(y_res).items()))
    ros = overMethod(sampling_strategy=sampling_strategy)
    # ros = BorderlineSMOTE()
    # sampling_strategy='minority'
    # ros = SMOTE()
    X_res, y_res = ros.fit_resample(X_res, y_res)

    print('Resampled dataset shape %s' % sorted(Counter(y_res).items()))
    print("-------------------------------------------")
    return X_res, y_res
```

## 5.2 Criando Freatures

Por meio de alguns testes e análises efetuadas em "6.youtube-comments-types-analysis.ipynb" concluiu-se que os melhores métodos de criação de freatures a serem utilizados são o LSA e Word2Vec pois os mesmos trazem os melhores resultados quando somados ao oversample. 


```python
required_columns = 'transformed_comment'
le = LabelEncoder()

X = df[required_columns]
y = le.fit_transform(df['final_type'])
```

### 5.2.1 Word2Vec


```python
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
```


```python
model.wv.save('eletronics_model.bin')
embeddings = KeyedVectors.load('eletronics_model.bin')
```


```python
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
```


```python
X_w2v.shape
```




    (4907, 100)



### 5.2.2 LSA


```python
# tfidf_v = TfidfVectorizer(ngram_range = (3, 3))
tfidf_v = TfidfVectorizer(ngram_range = (2, 3))
#matrixTFIDF= tfidf_v.fit_transform(train.question_text)
matrixTFIDF= tfidf_v.fit_transform(df[required_columns])
svd=TruncatedSVD(n_components=100, n_iter=20, algorithm='randomized')
X_lsa=svd.fit_transform(matrixTFIDF) 
```


```python
X_lsa.shape
```




    (4907, 100)



Em ambos os métodos 100 features foram criadas para a classificação dos comentários.

# 5.3 Treinando o Modelo

Para o treinamento do modelo a partir das features criadas o métodos LinearSVC trouxe o melhor resultado de recall comparado aos demais métodos utilizados em "6.youtube-comments-types-analysis.ipynb". Para a execução do oversample o método Adaptive Synthetic (ADASYN) me trouxe o melhor resultado pois o mesmo controla com melhor eficácia a replicação de outliers no meu escopo de dados em relação ao SMOTE. A estratégia utilizada para a criação de novos dados com o ADASYN foi a partir do "minority" que equilibra somente os dados de menor quantidade com os de maior quantidade, evitando qualquer alteração nos dados de categoria neutra que não são interessantes para a nossa análise. 


```python
param_grid = [
  {'C': [1, 10, 100, 1000]}
 ] 
svc = LinearSVC()

X_train_w2v, X_test_w2v, y_train_w2v, y_test_w2v = train_test_split(X_w2v, df['final_type'], test_size = .20)
X_train_w2v, y_train_w2v = overSamplDef(X_train_w2v, y_train_w2v, ADASYN, sampling_strategy='minority') #SMOTE | SMOTE
model_w2v = GridSearchCV(svc, param_grid).fit(X_train_w2v, y_train_w2v)
y_pred_w2v = model_w2v.predict(X_test_w2v)
y_pred_train_w2v = model_w2v.predict(X_train_w2v)

param_grid = [
  {'C': [1, 10, 100, 1000]}
 ] 
svc = LinearSVC()

X_train_lsa, X_test_lsa, y_train_lsa, y_test_lsa = train_test_split(X_lsa, df['final_type'], test_size = .20)
X_train_lsa, y_train_lsa = overSamplDef(X_train_lsa, y_train_lsa, ADASYN, sampling_strategy='minority') #SMOTE | SMOTE
model_lsa = GridSearchCV(svc, param_grid).fit(X_train_lsa, y_train_lsa)
y_pred_lsa = model_lsa.predict(X_test_lsa)
y_pred_train_lsa = model_lsa.predict(X_train_lsa)
```

    Before dataset shape [(-1, 191), (0, 1300), (1, 2434)]
    Resampled dataset shape [(-1, 2470), (0, 1300), (1, 2434)]
    -------------------------------------------
    Before dataset shape [(-1, 177), (0, 1290), (1, 2458)]
    Resampled dataset shape [(-1, 2502), (0, 1290), (1, 2458)]
    -------------------------------------------
    


```python
target_names = ['Negativo', 'Neutro', 'Positivo']

print("SVC - Report W2V")
print(classification_report(y_test_w2v, y_pred_w2v, target_names=target_names))

print("SVC - Report LSA")
print(classification_report(y_test_lsa, y_pred_lsa, target_names=target_names))
```

    SVC - Report W2V
                  precision    recall  f1-score   support
    
        Negativo       0.05      0.45      0.09        47
          Neutro       0.43      0.01      0.02       335
        Positivo       0.60      0.56      0.58       600
    
        accuracy                           0.36       982
       macro avg       0.36      0.34      0.23       982
    weighted avg       0.52      0.36      0.36       982
    
    SVC - Report LSA
                  precision    recall  f1-score   support
    
        Negativo       0.09      0.80      0.16        65
          Neutro       0.37      0.05      0.09       336
        Positivo       0.60      0.35      0.44       581
    
        accuracy                           0.28       982
       macro avg       0.35      0.40      0.23       982
    weighted avg       0.49      0.28      0.30       982
    
    


```python
disp = plot_confusion_matrix(y_test_w2v, y_pred_w2v)
disp.set_title('LSVC - W2V')
disp = plot_confusion_matrix(y_test_lsa, y_pred_lsa)
disp.set_title('LSVC - LSA')
```




    Text(0.5, 1.0, 'LSVC - LSA')




    
![svg](youtube-comments-types-analysis-complete-review_files/youtube-comments-types-analysis-complete-review_55_1.svg)
    



    
![svg](youtube-comments-types-analysis-complete-review_files/youtube-comments-types-analysis-complete-review_55_2.svg)
    


Após a execução do oversample e depois de treinar o modelo com LinearSVC obtivemos os valores de 69% de recall para negativos e 58% de recall para positivos em word2vec. Para o método LSA, obtivemos um valor mais elevado de recall em negativos (80%) e menor em positivos (35%), porém a fim de equilibrar nossos resultados em ambos os atributos, o word2vec é o mais efiente. 

# 5.3 Concretizando resultados

A fim entendermos qual é o resultado concreto do nosso modelo, efetuei o treino do modelo 600 vezes a fim de obter resultados mais precisos. 


```python
model_report = pd.DataFrame()
predict_w2v_traning = []
predict_lsa_traning = []

for exec in range(600):

    print("Execução ", exec, " de ", 600)

    param_grid = [
        {'C': [1, 10, 100, 1000]}
    ] 
    svc = LinearSVC()

    X_train_w2v, X_test_w2v, y_train_w2v, y_test_w2v = train_test_split(X_w2v, df['final_type'], test_size = .2)
    X_train_w2v, y_train_w2v = overSamplDef(X_train_w2v, y_train_w2v, ADASYN, sampling_strategy='minority') #SMOTE | SMOTE
    clf = GridSearchCV(svc, param_grid).fit(X_train_w2v, y_train_w2v)
    y_pred_w2v = clf.predict(X_test_w2v)

    X_train_lsa, X_test_lsa, y_train_lsa, y_test_lsa = train_test_split(X_lsa, df['final_type'], test_size = .2)
    X_train_lsa, y_train_lsa = overSamplDef(X_train_lsa, y_train_lsa, ADASYN, sampling_strategy='minority') #SMOTE | SMOTE
    clf = GridSearchCV(svc, param_grid).fit(X_train_lsa, y_train_lsa)
    y_pred_lsa = clf.predict(X_test_lsa)

    svc_w2v = classification_report(y_test_w2v, y_pred_w2v, output_dict=True)
    predict_w2v_traning.append(svc_w2v)

    svc_lsa = classification_report(y_test_lsa, y_pred_lsa, output_dict=True)
    predict_lsa_traning.append(svc_lsa)

model_w2v_report = pd.json_normalize(predict_w2v_traning)
model_lsa_report = pd.json_normalize(predict_lsa_traning)

model_w2v_report.to_csv('w2v_report2.csv', index=False)
model_lsa_report.to_csv('lsa_report2.csv', index=False)
```


```python
model_w2v_report = pd.read_csv('w2v_report2.csv')
model_lsa_report = pd.read_csv('lsa_report2.csv')
```


```python
model_w2v_report
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>accuracy</th>
      <th>-1.precision</th>
      <th>-1.recall</th>
      <th>-1.f1-score</th>
      <th>-1.support</th>
      <th>0.precision</th>
      <th>0.recall</th>
      <th>0.f1-score</th>
      <th>0.support</th>
      <th>1.precision</th>
      <th>...</th>
      <th>1.f1-score</th>
      <th>1.support</th>
      <th>macro avg.precision</th>
      <th>macro avg.recall</th>
      <th>macro avg.f1-score</th>
      <th>macro avg.support</th>
      <th>weighted avg.precision</th>
      <th>weighted avg.recall</th>
      <th>weighted avg.f1-score</th>
      <th>weighted avg.support</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.429162</td>
      <td>0.087079</td>
      <td>0.704545</td>
      <td>0.155000</td>
      <td>44</td>
      <td>0.166667</td>
      <td>0.003067</td>
      <td>0.006024</td>
      <td>326</td>
      <td>0.633058</td>
      <td>...</td>
      <td>0.637271</td>
      <td>597</td>
      <td>0.295601</td>
      <td>0.449718</td>
      <td>0.266098</td>
      <td>967</td>
      <td>0.450983</td>
      <td>0.429162</td>
      <td>0.402518</td>
      <td>967</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0.450879</td>
      <td>0.078550</td>
      <td>0.541667</td>
      <td>0.137203</td>
      <td>48</td>
      <td>0.285714</td>
      <td>0.006536</td>
      <td>0.012780</td>
      <td>306</td>
      <td>0.648649</td>
      <td>...</td>
      <td>0.657005</td>
      <td>613</td>
      <td>0.337638</td>
      <td>0.404594</td>
      <td>0.268996</td>
      <td>967</td>
      <td>0.505502</td>
      <td>0.450879</td>
      <td>0.427343</td>
      <td>967</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0.409514</td>
      <td>0.086957</td>
      <td>0.692308</td>
      <td>0.154506</td>
      <td>52</td>
      <td>0.500000</td>
      <td>0.023333</td>
      <td>0.044586</td>
      <td>300</td>
      <td>0.654917</td>
      <td>...</td>
      <td>0.611785</td>
      <td>615</td>
      <td>0.413958</td>
      <td>0.429875</td>
      <td>0.270293</td>
      <td>967</td>
      <td>0.576314</td>
      <td>0.409514</td>
      <td>0.411229</td>
      <td>967</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0.422958</td>
      <td>0.058496</td>
      <td>0.583333</td>
      <td>0.106329</td>
      <td>36</td>
      <td>0.333333</td>
      <td>0.003096</td>
      <td>0.006135</td>
      <td>323</td>
      <td>0.639669</td>
      <td>...</td>
      <td>0.638087</td>
      <td>608</td>
      <td>0.343833</td>
      <td>0.407647</td>
      <td>0.250184</td>
      <td>967</td>
      <td>0.515710</td>
      <td>0.422958</td>
      <td>0.407204</td>
      <td>967</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0.418821</td>
      <td>0.065491</td>
      <td>0.666667</td>
      <td>0.119266</td>
      <td>39</td>
      <td>0.500000</td>
      <td>0.010101</td>
      <td>0.019802</td>
      <td>297</td>
      <td>0.666667</td>
      <td>...</td>
      <td>0.629289</td>
      <td>631</td>
      <td>0.410719</td>
      <td>0.424216</td>
      <td>0.256119</td>
      <td>967</td>
      <td>0.591231</td>
      <td>0.418821</td>
      <td>0.421524</td>
      <td>967</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>595</th>
      <td>0.381593</td>
      <td>0.073227</td>
      <td>0.744186</td>
      <td>0.133333</td>
      <td>43</td>
      <td>0.500000</td>
      <td>0.006270</td>
      <td>0.012384</td>
      <td>319</td>
      <td>0.636882</td>
      <td>...</td>
      <td>0.592396</td>
      <td>605</td>
      <td>0.403370</td>
      <td>0.434725</td>
      <td>0.246038</td>
      <td>967</td>
      <td>0.566662</td>
      <td>0.381593</td>
      <td>0.380645</td>
      <td>967</td>
    </tr>
    <tr>
      <th>596</th>
      <td>0.422958</td>
      <td>0.089286</td>
      <td>0.673077</td>
      <td>0.157658</td>
      <td>52</td>
      <td>0.500000</td>
      <td>0.012698</td>
      <td>0.024768</td>
      <td>315</td>
      <td>0.652557</td>
      <td>...</td>
      <td>0.634105</td>
      <td>600</td>
      <td>0.413948</td>
      <td>0.434147</td>
      <td>0.272177</td>
      <td>967</td>
      <td>0.572572</td>
      <td>0.422958</td>
      <td>0.409993</td>
      <td>967</td>
    </tr>
    <tr>
      <th>597</th>
      <td>0.392968</td>
      <td>0.064039</td>
      <td>0.619048</td>
      <td>0.116071</td>
      <td>42</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>337</td>
      <td>0.631016</td>
      <td>...</td>
      <td>0.616188</td>
      <td>588</td>
      <td>0.231685</td>
      <td>0.407029</td>
      <td>0.244086</td>
      <td>967</td>
      <td>0.386481</td>
      <td>0.392968</td>
      <td>0.379724</td>
      <td>967</td>
    </tr>
    <tr>
      <th>598</th>
      <td>0.407446</td>
      <td>0.069652</td>
      <td>0.736842</td>
      <td>0.127273</td>
      <td>38</td>
      <td>0.307692</td>
      <td>0.012945</td>
      <td>0.024845</td>
      <td>309</td>
      <td>0.655797</td>
      <td>...</td>
      <td>0.617747</td>
      <td>620</td>
      <td>0.344380</td>
      <td>0.444553</td>
      <td>0.256622</td>
      <td>967</td>
      <td>0.521528</td>
      <td>0.407446</td>
      <td>0.409014</td>
      <td>967</td>
    </tr>
    <tr>
      <th>599</th>
      <td>0.407446</td>
      <td>0.071247</td>
      <td>0.682927</td>
      <td>0.129032</td>
      <td>41</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>320</td>
      <td>0.642105</td>
      <td>...</td>
      <td>0.622449</td>
      <td>606</td>
      <td>0.237784</td>
      <td>0.428962</td>
      <td>0.250494</td>
      <td>967</td>
      <td>0.405416</td>
      <td>0.407446</td>
      <td>0.395547</td>
      <td>967</td>
    </tr>
  </tbody>
</table>
<p>600 rows × 21 columns</p>
</div>




```python
model_lsa_report
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>accuracy</th>
      <th>-1.precision</th>
      <th>-1.recall</th>
      <th>-1.f1-score</th>
      <th>-1.support</th>
      <th>0.precision</th>
      <th>0.recall</th>
      <th>0.f1-score</th>
      <th>0.support</th>
      <th>1.precision</th>
      <th>...</th>
      <th>1.f1-score</th>
      <th>1.support</th>
      <th>macro avg.precision</th>
      <th>macro avg.recall</th>
      <th>macro avg.f1-score</th>
      <th>macro avg.support</th>
      <th>weighted avg.precision</th>
      <th>weighted avg.recall</th>
      <th>weighted avg.f1-score</th>
      <th>weighted avg.support</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.287487</td>
      <td>0.071918</td>
      <td>0.823529</td>
      <td>0.132283</td>
      <td>51</td>
      <td>0.456522</td>
      <td>0.064615</td>
      <td>0.113208</td>
      <td>325</td>
      <td>0.637982</td>
      <td>...</td>
      <td>0.463362</td>
      <td>591</td>
      <td>0.388807</td>
      <td>0.417312</td>
      <td>0.236284</td>
      <td>967</td>
      <td>0.547140</td>
      <td>0.287487</td>
      <td>0.328217</td>
      <td>967</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0.310238</td>
      <td>0.063752</td>
      <td>0.744681</td>
      <td>0.117450</td>
      <td>47</td>
      <td>0.382979</td>
      <td>0.055901</td>
      <td>0.097561</td>
      <td>322</td>
      <td>0.665768</td>
      <td>...</td>
      <td>0.509804</td>
      <td>598</td>
      <td>0.370833</td>
      <td>0.404542</td>
      <td>0.241605</td>
      <td>967</td>
      <td>0.542342</td>
      <td>0.310238</td>
      <td>0.353462</td>
      <td>967</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0.298862</td>
      <td>0.057971</td>
      <td>0.711111</td>
      <td>0.107203</td>
      <td>45</td>
      <td>0.372549</td>
      <td>0.059375</td>
      <td>0.102426</td>
      <td>320</td>
      <td>0.653846</td>
      <td>...</td>
      <td>0.492754</td>
      <td>602</td>
      <td>0.361455</td>
      <td>0.388612</td>
      <td>0.234127</td>
      <td>967</td>
      <td>0.533030</td>
      <td>0.298862</td>
      <td>0.345644</td>
      <td>967</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0.317477</td>
      <td>0.076208</td>
      <td>0.706897</td>
      <td>0.137584</td>
      <td>58</td>
      <td>0.457143</td>
      <td>0.049080</td>
      <td>0.088643</td>
      <td>326</td>
      <td>0.634518</td>
      <td>...</td>
      <td>0.511771</td>
      <td>583</td>
      <td>0.389290</td>
      <td>0.394931</td>
      <td>0.245999</td>
      <td>967</td>
      <td>0.541233</td>
      <td>0.317477</td>
      <td>0.346680</td>
      <td>967</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0.301965</td>
      <td>0.056239</td>
      <td>0.800000</td>
      <td>0.105090</td>
      <td>40</td>
      <td>0.490196</td>
      <td>0.086505</td>
      <td>0.147059</td>
      <td>289</td>
      <td>0.677233</td>
      <td>...</td>
      <td>0.477157</td>
      <td>638</td>
      <td>0.407890</td>
      <td>0.418281</td>
      <td>0.243102</td>
      <td>967</td>
      <td>0.595648</td>
      <td>0.301965</td>
      <td>0.363113</td>
      <td>967</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>595</th>
      <td>0.338159</td>
      <td>0.084453</td>
      <td>0.733333</td>
      <td>0.151463</td>
      <td>60</td>
      <td>0.500000</td>
      <td>0.067114</td>
      <td>0.118343</td>
      <td>298</td>
      <td>0.647783</td>
      <td>...</td>
      <td>0.518227</td>
      <td>609</td>
      <td>0.410745</td>
      <td>0.410768</td>
      <td>0.262678</td>
      <td>967</td>
      <td>0.567288</td>
      <td>0.338159</td>
      <td>0.372238</td>
      <td>967</td>
    </tr>
    <tr>
      <th>596</th>
      <td>0.288521</td>
      <td>0.070447</td>
      <td>0.854167</td>
      <td>0.130159</td>
      <td>48</td>
      <td>0.403846</td>
      <td>0.064220</td>
      <td>0.110818</td>
      <td>327</td>
      <td>0.651652</td>
      <td>...</td>
      <td>0.469189</td>
      <td>592</td>
      <td>0.375315</td>
      <td>0.428314</td>
      <td>0.236722</td>
      <td>967</td>
      <td>0.539004</td>
      <td>0.288521</td>
      <td>0.331174</td>
      <td>967</td>
    </tr>
    <tr>
      <th>597</th>
      <td>0.305067</td>
      <td>0.064171</td>
      <td>0.765957</td>
      <td>0.118421</td>
      <td>47</td>
      <td>0.442308</td>
      <td>0.070988</td>
      <td>0.122340</td>
      <td>324</td>
      <td>0.666667</td>
      <td>...</td>
      <td>0.496842</td>
      <td>596</td>
      <td>0.391048</td>
      <td>0.410973</td>
      <td>0.245868</td>
      <td>967</td>
      <td>0.562210</td>
      <td>0.305067</td>
      <td>0.352970</td>
      <td>967</td>
    </tr>
    <tr>
      <th>598</th>
      <td>0.289555</td>
      <td>0.053381</td>
      <td>0.789474</td>
      <td>0.100000</td>
      <td>38</td>
      <td>0.300000</td>
      <td>0.039474</td>
      <td>0.069767</td>
      <td>304</td>
      <td>0.652055</td>
      <td>...</td>
      <td>0.480808</td>
      <td>625</td>
      <td>0.335145</td>
      <td>0.403249</td>
      <td>0.216859</td>
      <td>967</td>
      <td>0.517852</td>
      <td>0.289555</td>
      <td>0.336623</td>
      <td>967</td>
    </tr>
    <tr>
      <th>599</th>
      <td>0.270941</td>
      <td>0.074013</td>
      <td>0.833333</td>
      <td>0.135952</td>
      <td>54</td>
      <td>0.416667</td>
      <td>0.029586</td>
      <td>0.055249</td>
      <td>338</td>
      <td>0.617910</td>
      <td>...</td>
      <td>0.454945</td>
      <td>575</td>
      <td>0.369530</td>
      <td>0.407640</td>
      <td>0.215382</td>
      <td>967</td>
      <td>0.517196</td>
      <td>0.270941</td>
      <td>0.297424</td>
      <td>967</td>
    </tr>
  </tbody>
</table>
<p>600 rows × 21 columns</p>
</div>




```python
print("Word2Vec Negative Recall ", model_w2v_report['-1.recall'].mean())
print("Word2Vec Positive Recall ", model_w2v_report['1.recall'].mean())
print("Word2Vec Negative Precision ", model_w2v_report['-1.precision'].mean())
print("Word2Vec Positive Precision ", model_w2v_report['1.precision'].mean())
print("------------------------------------------------")
print("LSA Negative Recall ", model_lsa_report['-1.recall'].mean())
print("LSA Positive Recall ", model_lsa_report['1.recall'].mean())
print("LSA Negative Precision ", model_lsa_report['-1.precision'].mean())
print("LSA Positive Precision ", model_lsa_report['1.precision'].mean())
```

    Word2Vec Negative Recall  0.6760651665443369
    Word2Vec Positive Recall  0.5902087091180059
    Word2Vec Negative Precision  0.07972179854547427
    Word2Vec Positive Precision  0.6387797598972071
    ------------------------------------------------
    LSA Negative Recall  0.7701296959476054
    LSA Positive Recall  0.38967991422049786
    LSA Negative Precision  0.06515107584511744
    LSA Positive Precision  0.6489308944833397
    

Para ambas as features, obtemos resultados parecidos aos executados anteriormente. Com atenção os nossos atributos principais da feature word2vec de 67% para negativos e 59% para positivos. 


```python
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(30,15))
axes[0][0].set_title("Histograma de recall para negativos em word2vec")
model_w2v_report['-1.recall'].plot.hist(ax=axes[0][0], color="#dc3545")

axes[0][1].set_title("Histograma de recall para positivos em word2vec")
model_w2v_report['1.recall'].plot.hist(ax=axes[0][1], color="#218838")

axes[1][0].set_title("Histograma de precision para negativos em word2vec")
model_w2v_report['-1.precision'].plot.hist(ax=axes[1][0], color="#dc3545")

axes[1][1].set_title("Histograma de precision para positivos em word2vec")
model_w2v_report['1.precision'].plot.hist(ax=axes[1][1], color="#218838")


```




    <AxesSubplot:title={'center':'Histograma de precision para positivos em word2vec'}, ylabel='Frequency'>




    
![svg](youtube-comments-types-analysis-complete-review_files/youtube-comments-types-analysis-complete-review_65_1.svg)
    

