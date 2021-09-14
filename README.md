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

- Criada em Reactjs e os dados são armazenados por meio do Firebase;

- A seleção dos comentários para os usuários foi de forma aleatória e com pesos. Onde os comentários menos avaliados pelos usuários tinham um peso maior para serem trazidos com maior probabilidade antes dos mais avaliados;

- Cada usuário que fez a avaliação será diferenciado pelo IP ou um timestamp da página aberta no momento a fim de contabilizar o experimento;

- Um total de 10 mil comentários foram armazenados na ferramenta.

# 3.1 Preparação dos dados

Após a criação do site para a coleta de avaliações, monitorei os dados coletados e avaliados pelos usuários. Meu número final de comentários avaliados foi o evidenciado abaixo: 

<div>
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
      <th>4901</th>
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
      <th>4902</th>
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
      <th>4903</th>
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
      <th>4904</th>
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
      <th>4905</th>
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
<p>4906 rows × 14 columns</p>
</div>

Onde "final_type" corresponde a classificação do comentário positivo (1), neutro(0) ou negativo(-1)

# 3.2 Transformação com técnicas de NLP

Meu objetivo aqui é padronizar meus comentários a fim de aplicar as tecnicas de criação de feature (LSA e Word2Vec). Defini funções para cada uma das etapadas da transformação, as mesmas são:

- Transformar todos os comentários para letras minúculas;

- Remover pontuações;

- Transformar emojis para códigos. Exemplo: 

- Normalização do texto em UTF-8

- Remoção de stop words (excessão a palavra "não")

- Estematização das palavras. Exemplo: 

- Remoção de excesso de espaços (\n)


```python
def remove_punctuation(dfText, exception = {}):

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

                for sentence in exception:

                    # print(token,':',sentence)

                    if token == sentence:

                        new_review = new_review +" "+exception[sentence]+" "

                    else:

                        new_review = new_review + " "

        

        tokenized_docs_no_punctuation.append(new_review)

    return tokenized_docs_no_punctuation



def unicode_emoji(dfText, remove=False):

    import emoji

    for emoj in emoji.UNICODE_EMOJI['pt']:

        if remove:

            dfText = dfText.str.replace(emoj,' ', regex=False)

        else:

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

    # stopwords.remove('não')



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
exception = {'!': ':exclamacao:', '?': ':interrogacao:'}

df['transformed_comment'] = lower_case(df['comment']) 
df['transformed_comment'] = remove_punctuation(df['transformed_comment'], exception) 
df['transformed_comment'] = unicode_emoji(df['transformed_comment'], False)
df['transformed_comment'] = normalize_utf8(df['transformed_comment'])
df['transformed_comment'] = removing_stop_words(df['transformed_comment'])
df['transformed_comment'] = portuguese_stemmer(df['transformed_comment'])
df['transformed_comment'] = excess_space_remover(df['transformed_comment'])
```

# 4 Análise Exploratória

Após o tratamento das informações algumas análises foram feitas a fim de entender os dados. 

## 4.1 Exclamação e Interrogação são importantes para a análise


```python
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(15,4))

exclamation = df['final_type'].loc[df['comment'].str.find('!') != -1].value_counts()/df['final_type'].value_counts()*100
exclamation = pd.DataFrame([round(exclamation[-1],2),round(exclamation[1],2),round(exclamation[0],2)], index=['Negativo', 'Positivo', 'Neutro'])

interrogation = df['final_type'].loc[df['comment'].str.find('?') != -1].value_counts()/df['final_type'].value_counts()*100
interrogation = pd.DataFrame([round(interrogation[-1],2),round(interrogation[1],2),round(interrogation[0],2)], index=['Negativo', 'Positivo', 'Neutro'])

exclamation[0].plot.bar(

    # color=['#dc3545','#ffc107','#218838'],

    color=['#dc3545','#218838','#ffc107'],

    ax=ax[0],

    rot=1)

interrogation[0].plot.bar(

    # color=['#dc3545','#ffc107','#218838'],

    color=['#dc3545','#218838','#ffc107'],

    ax=ax[1],

    rot=1)



ax[0].get_yaxis().set_ticks([])
ax[0].grid(False)

ax[1].get_yaxis().set_ticks([])
ax[1].grid(False)

ax[0].set(frame_on=False) 
ax[1].set(frame_on=False) 

ax[0].set_title("Percentual de exclamação (!) por comentário (%)", fontsize=14, color='#4f4e4e', y=1.12)
ax[0].bar_label(ax[0].containers[0], padding=2, fontsize=12, color='#4f4e4e')

ax[1].set_title("Percentual de Interrogação (?) por comentário (%)", fontsize=14, color='#4f4e4e', y=1.12)
ax[1].bar_label(ax[1].containers[0], padding=2, fontsize=12, color='#4f4e4e')
```
 
![svg](youtube-comments-types-analysis-complete-review_files/youtube-comments-types-analysis-complete-review_31_1.svg)
  
Nota-se que a quantidade de comentários com exclamação é maior para os negativo e consideravelmente menos para neutros, além disso o percentual de interrogação para neutros é bastanta alto também e muito baixo para negativos. Os dois serão considerados nas features do modelo. 

## 4.2 Emotes podem ser relevantes para a análise

```python
emojis_type = []
emojis_count = []
emojis = []
types = [-1, 0, 1]

for emoj in emoji.UNICODE_EMOJI['pt']:
    emojisCont = df['comment'].loc[df['final_type'] == ty].str.count(emoj)
    for ty in types:

        emojisCont = df['comment'].loc[df['final_type'] == ty].str.count(emoj).sum()
        emojis_count.append(emojisCont)
        emojis_type.append(ty)
        emojis.append(emoj)

emoji_data = {'count': emojis_count, 'type': emojis_type}
emoji_data = pd.DataFrame(emoji_data, index=emojis)

emoji_data['count'].loc[(emoji_data['type'] == -1)].sort_values(ascending=False)[:10]
emoji_data['count'].loc[(emoji_data['type'] == 0)].sort_values(ascending=False)[:10]
emoji_data['count'].loc[(emoji_data['type'] == 1)].sort_values(ascending=False)[:10]

negative = emoji_data['count'].loc[(emoji_data['type'] == -1)].sort_values(ascending=False)[:10].reset_index()
negative['Negativo'] = negative['index'] + ' ' + negative['count'].astype(str)

neutro = emoji_data['count'].loc[(emoji_data['type'] == 0)].sort_values(ascending=False)[:10].reset_index()
neutro['Neutro'] = neutro['index'] + ' ' + neutro['count'].astype(str)

positive = emoji_data['count'].loc[(emoji_data['type'] == 1)].sort_values(ascending=False)[:10].reset_index()
positive['Positivo'] = positive['index'] + ' ' + positive['count'].astype(str)

types_emojis = {'Negativo' :negative['Negativo'], 'Neutro': neutro['Neutro'], 'Positivo': positive['Positivo']}
types_emojis = pd.DataFrame(types_emojis)

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
      <th>Negativo</th>
      <th>Neutro</th>
      <th>Positivo</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>😂 9</td>
      <td>🤣 42</td>
      <td>😂 84</td>
    </tr>
    <tr>
      <th>1</th>
      <td>😭 7</td>
      <td>😂 24</td>
      <td>😍 79</td>
    </tr>
    <tr>
      <th>2</th>
      <td>🤣 6</td>
      <td>👏 23</td>
      <td>👏 75</td>
    </tr>
    <tr>
      <th>3</th>
      <td>♂️ 5</td>
      <td>🏻 16</td>
      <td>🤣 40</td>
    </tr>
    <tr>
      <th>4</th>
      <td>🤦 5</td>
      <td>👍 15</td>
      <td>😭 39</td>
    </tr>
    <tr>
      <th>5</th>
      <td>🤔 3</td>
      <td>🤔 12</td>
      <td>❤️ 32</td>
    </tr>
    <tr>
      <th>6</th>
      <td>🤦🏾 2</td>
      <td>😍 12</td>
      <td>😁 28</td>
    </tr>
    <tr>
      <th>7</th>
      <td>🏾 2</td>
      <td>😠 10</td>
      <td>🥰 26</td>
    </tr>
    <tr>
      <th>8</th>
      <td>🤷 2</td>
      <td>👎 9</td>
      <td>👍 25</td>
    </tr>
    <tr>
      <th>9</th>
      <td>😔 2</td>
      <td>😅 9</td>
      <td>🏼 23</td>
    </tr>
  </tbody>
</table>
</div>




```python
emojis_line_count = []

for comment in df['comment']:

    hasEmoji = False
    for emoj in emoji.UNICODE_EMOJI['pt']:
        if emoj in comment:
            hasEmoji = True
    emojis_line_count.append(hasEmoji)

df['has_emoji'] = emojis_line_count
```

```python
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10,5))

emojis_percent = df['final_type'].loc[df['has_emoji']].value_counts()/df['final_type'].value_counts()*100
emojis_percent = pd.DataFrame([round(emojis_percent[1],2),round(emojis_percent[-1],2),round(emojis_percent[0],2)], index=['Positivo', 'Negativo', 'Neutro'])

emojis_percent[0].plot.barh(

    color=['#218838','#dc3545','#ffc107'],

    ax=ax,

    rot=1)

ax.set_title("Percentual de comentários com emojis (%)", fontsize=16, color='#4f4e4e')
ax.bar_label(ax.containers[0], padding=2, fontsize=12, color='#4f4e4e')
```
    
![svg](youtube-comments-types-analysis-complete-review_files/youtube-comments-types-analysis-complete-review_36_1.svg)
    
Apesar da pequena a quantidade de emojis por comentários, os emojis entre as classificações são de maioria distintos e podem ser relevantes como features.

## 4.3 Quantidade muito baixa de comentários negativos

Nota-se uma quantidade muito baixa de comentários negativos em meu escopo de dados, além de uma quantidade muito grande de comentários positivos. Técnicas de balanceamento de classes serão utilizadas nesse modelo.

```python
import seaborn as sns

f_type = df['final_type'].value_counts(normalize=True).reset_index()
f_type['type'] = ['Positivo', 'Neutro', 'Negativo']
f_type = f_type.drop('index', 1)

plt.rcParams['figure.dpi'] = 100
sns.set(style="whitegrid")

fig, ax = plt.subplots(figsize=(12,4))
sns.barplot(data=f_type, x="type", y="final_type", palette=['#218838','#ffc107','#dc3545'])

plt.xlabel('Classificação', size=10, color='#4f4e4e')
plt.ylabel('')
plt.title('Distribuição dos comentários por classificação (%)', size=15, color='#4f4e4e')
plt.yticks([], [])
plt.text(x=0, y=0.01, s="61.93", 
                 color='white', fontsize=15, horizontalalignment='center')
plt.text(x=1, y=0.01, s="33.14", 
                 color='white', fontsize=15, horizontalalignment='center')
plt.text(x=2, y=0.01, s="4.93", 
                 color='white', fontsize=15, horizontalalignment='center')
sns.despine(left=True)
```

![svg](youtube-comments-types-analysis-complete-review_files/youtube-comments-types-analysis-complete-review_40_0.svg)
    
```python
wc = WordCloud(background_color='black', width = 3000, height = 2000, colormap='Set2', collocations=False)

#df['transformed_comment']

wc.generate(' '.join(df['transformed_comment']))

plt.axis("off")
plt.imshow(wc, interpolation="bilinear")
plt.show()
```
    
![svg](youtube-comments-types-analysis-complete-review_files/youtube-comments-types-analysis-complete-review_41_0.svg)
    
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

Por meio de alguns testes e análises efetuadas em [6.youtube-comments-types-analysis.ipynb](https://github.com/ErycM/electronics-sentiment-analysis-on-youtube-comments/blob/main/6.youtube-comments-types-analysis.ipynb) concluiu-se que os melhores métodos de criação de freatures a serem utilizados são o LSA e Word2Vec pois os mesmos trazem os melhores resultados quando somados ao oversample. 

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
model.wv.save('src/eletronics_model.bin')
embeddings = KeyedVectors.load('src/eletronics_model.bin')
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

X_w2v = word2vec_doc_vec
```

```python
X_w2v.shape
```
(4906, 100)



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
(4906, 100)



Em ambos os métodos 100 features foram criadas para a classificação dos comentários.

# 5.3 Treinando o Modelo

Para o treinamento do modelo a partir das features criadas o métodos LinearSVC trouxe o melhor resultado de recall comparado aos demais métodos utilizados em [6.youtube-comments-types-analysis.ipynb](https://github.com/ErycM/electronics-sentiment-analysis-on-youtube-comments/blob/main/6.youtube-comments-types-analysis.ipynb). Para a execução do oversample o método Adaptive Synthetic (ADASYN) me trouxe o melhor resultado pois o mesmo controla com melhor eficácia a replicação dos dados em regiões com maior densidade da minha amostra minoritária, evitando replicações desnecessárias em outliers. A estratégia utilizada para a criação de novos dados com o ADASYN foi a partir do "minority" que equilibra somente os dados de menor quantidade com os de maior quantidade, evitando qualquer alteração nos dados de categoria neutra que não são interessantes para a análise. 

```python
param_grid = [
  {'C': [1, 10, 100, 1000]}
 ] 

svc = SVC()

X_train_w2v, X_test_w2v, y_train_w2v, y_test_w2v = train_test_split(X_w2v, df['final_type'], test_size = .20)
X_train_w2v, y_train_w2v = overSamplDef(X_train_w2v, y_train_w2v, ADASYN, sampling_strategy='minority') 
model_w2v = GridSearchCV(svc, param_grid).fit(X_train_w2v, y_train_w2v)
y_pred_w2v = model_w2v.predict(X_test_w2v)
y_pred_train_w2v = model_w2v.predict(X_train_w2v)

param_grid = [

  {'C': [1, 10, 100, 1000]}

 ] 

svc = SVC()

X_train_lsa, X_test_lsa, y_train_lsa, y_test_lsa = train_test_split(X_lsa, df['final_type'], test_size = .20)
X_train_lsa, y_train_lsa = overSamplDef(X_train_lsa, y_train_lsa, ADASYN, sampling_strategy='minority') 
model_lsa = GridSearchCV(svc, param_grid).fit(X_train_lsa, y_train_lsa)
y_pred_lsa = model_lsa.predict(X_test_lsa)
y_pred_train_lsa = model_lsa.predict(X_train_lsa)
```
    Before dataset shape [(-1, 188), (0, 1294), (1, 2442)]
    Resampled dataset shape [(-1, 2436), (0, 1294), (1, 2442)]
    -------------------------------------------
    Before dataset shape [(-1, 204), (0, 1284), (1, 2436)]
    Resampled dataset shape [(-1, 2455), (0, 1284), (1, 2436)]
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
    
        Negativo       0.09      0.65      0.15        54
          Neutro       0.25      0.00      0.01       331
        Positivo       0.62      0.60      0.61       597
    
        accuracy                           0.40       982
       macro avg       0.32      0.42      0.26       982
    weighted avg       0.47      0.40      0.38       982
    
    SVC - Report LSA
                  precision    recall  f1-score   support
    
        Negativo       0.06      0.58      0.11        38
          Neutro       0.34      0.17      0.22       341
        Positivo       0.61      0.44      0.51       603
    
        accuracy                           0.35       982
       macro avg       0.33      0.40      0.28       982
    weighted avg       0.49      0.35      0.39       982
      
```python
disp = plot_confusion_matrix(y_test_w2v, y_pred_w2v)
disp.set_title('LSVC - W2V')

disp = plot_confusion_matrix(y_test_lsa, y_pred_lsa)
disp.set_title('LSVC - LSA')
```
    
![svg](youtube-comments-types-analysis-complete-review_files/youtube-comments-types-analysis-complete-review_62_1.svg)    
![svg](youtube-comments-types-analysis-complete-review_files/youtube-comments-types-analysis-complete-review_62_2.svg)
    
Após a execução do oversample e depois de treinar o modelo com LinearSVC obtivemos os valores de aproximadamente 65% de recall para negativos e 60% de recall para positivos em word2vec. Para o método LSA, obtivemos um valor mais elevado de recall em negativos (80%) e menor em positivos (35%), porém a fim de equilibrar nossos resultados em ambos os atributos, o word2vec é o mais efiente. 

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
    X_train_w2v, y_train_w2v = overSamplDef(X_train_w2v, y_train_w2v, ADASYN, sampling_strategy='minority') 
    clf = GridSearchCV(svc, param_grid).fit(X_train_w2v, y_train_w2v)
    y_pred_w2v = clf.predict(X_test_w2v)

    X_train_lsa, X_test_lsa, y_train_lsa, y_test_lsa = train_test_split(X_lsa, df['final_type'], test_size = .2)
    X_train_lsa, y_train_lsa = overSamplDef(X_train_lsa, y_train_lsa, ADASYN, sampling_strategy='minority') 
    clf = GridSearchCV(svc, param_grid).fit(X_train_lsa, y_train_lsa)
    y_pred_lsa = clf.predict(X_test_lsa)

    svc_w2v = classification_report(y_test_w2v, y_pred_w2v, output_dict=True)
    predict_w2v_traning.append(svc_w2v)

    svc_lsa = classification_report(y_test_lsa, y_pred_lsa, output_dict=True)
    predict_lsa_traning.append(svc_lsa)

model_w2v_report = pd.json_normalize(predict_w2v_traning)
model_lsa_report = pd.json_normalize(predict_lsa_traning)

model_w2v_report.to_csv('src/w2v_report.csv', index=False)
model_lsa_report.to_csv('src/lsa_report2.csv', index=False)
```
    Execução  0  de  600
    Before dataset shape [(-1, 190), (0, 1309), (1, 2425)]
    Resampled dataset shape [(-1, 2462), (0, 1309), (1, 2425)]
    -------------------------------------------
    .
    .
    .
    .
    -------------------------------------------
    Execução  599  de  600
    Before dataset shape [(-1, 195), (0, 1317), (1, 2412)]
    Resampled dataset shape [(-1, 2360), (0, 1317), (1, 2412)]
    -------------------------------------------

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




    
![svg](youtube-comments-types-analysis-complete-review_files/youtube-comments-types-analysis-complete-review_72_1.svg)
    

