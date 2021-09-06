# Análise de sentimento - Comentários de Análises de Celulares no Youtube

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
   
![png](youtube-comments-types-analysis-complete-review_files/youtube-comments-types-analysis-complete-review_15_0.png)
    
A interface contem os seguintes requisitos funcionais e técnicos:

### 2.3.1 Criada em Reactjs e os dados são armazenados por meio do Firebase;
### 2.3.2 A seleção dos comentários para os usuários foi de forma aleatória e com pesos. Onde os comentários menos avaliados pelos usuários tinham um peso maior para serem trazidos com maior probabilidade antes dos mais avaliados;
### 2.3.3 Cada usuário que fez a avaliação será diferenciado pelo IP ou um timestamp da página aberta no momento a fim de contabilizar o experimento;
### 2.3.4 Um total de 10 mil comentários foram armazenados na ferramenta.

# 3.1 Preparação dos dados

Após a criação do site para a coleta de avaliações, monitorei os dados coletados e avaliados pelos usuários. Meu número final de comentários avaliados foi o evidenciado abaixo: 

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
### 3.2.3. Transformar emojis para códigos. Exemplo: 🙇 para :pessoa_fazendo_reverencia:
### 3.2.4. Normalização do texto em UTF-8
### 3.2.5. Remoção de stop words (excessão a palavra "não")
### 3.2.6. Estematização das palavras. Exemplo: "comprar" para "compr" 
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

    Before dataset shape [(-1, 184), (0, 1311), (1, 2430)]
    Resampled dataset shape [(-1, 2402), (0, 1311), (1, 2430)]
    -------------------------------------------
    Before dataset shape [(-1, 196), (0, 1309), (1, 2420)]
    Resampled dataset shape [(-1, 2406), (0, 1309), (1, 2420)]
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
    
        Negativo       0.10      0.67      0.17        58
          Neutro       0.64      0.02      0.04       315
        Positivo       0.65      0.60      0.62       609
    
        accuracy                           0.42       982
       macro avg       0.46      0.43      0.28       982
    weighted avg       0.61      0.42      0.41       982
    
    SVC - Report LSA
                  precision    recall  f1-score   support
    
        Negativo       0.07      0.83      0.13        46
          Neutro       0.56      0.06      0.11       317
        Positivo       0.66      0.42      0.52       619
    
        accuracy                           0.32       982
       macro avg       0.43      0.44      0.25       982
    weighted avg       0.60      0.32      0.37       982
    
    
![svg](youtube-comments-types-analysis-complete-review_files/youtube-comments-types-analysis-complete-review_55_1.svg)
![svg](youtube-comments-types-analysis-complete-review_files/youtube-comments-types-analysis-complete-review_55_2.svg)
    
Após a execução do oversample e depois de treinar o modelo com LinearSVC obtivemos os valores de 67% de recall para negativos e 60% de recall para positivos em word2vec. Para o método LSA, obtivemos um valor mais elevado de recall em negativos (80%) e menor em positivos (35%), porém a fim de equilibrar nossos resultados em ambos os atributos, o word2vec é o mais efiente. 

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
    
![svg](youtube-comments-types-analysis-complete-review_files/youtube-comments-types-analysis-complete-review_65_1.svg)
    

