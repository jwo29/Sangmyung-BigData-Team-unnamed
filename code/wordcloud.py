import pandas as pd
from wordcloud import WordCloud
from PIL import Image
import numpy as np
import nltk

cheonan_df = pd.io.parsers.read_csv("../csv/cheonan_bus_tweet_result.csv")
seoul_df = pd.io.parsers.read_csv("../csv/seoul_bus_tweet_result.csv")

cheonan_sliceData = cheonan_df.loc[:,"tweet"]
seoul_sliceData = seoul_df.loc[:,"tweet"]

nltk.download('punkt')
stopwords = ['지금', '어떤', '고','즉', '안','오', '나', '이', '있', '하', '것', '들', '그', '되', '수', '이', '보', '않', '없', '나', '사람', '주', '아니', '등', '같', '우리', '때', '년', '가', '한', '지', '대하', '오', '말', '일', '그렇', '위하']

cheonan_text = ""
seoul_text = ""

# cheonan
for line in cheonan_sliceData:
    for word in nltk.tokenize.word_tokenize(line):
        if word not in stopwords:
            cheonan_text += line.replace('부산버스', '').replace('천안 버스', '').replace('천안버스', '').replace('ㅋ', '').replace('ㅠ', '').replace('ㅎ', '').replace('ㅜ', '').replace('ㄱ', '').replace('ㅡ', '').replace('ㄷ', '')
# seoul
for line in seoul_sliceData:
    line = line.replace('서울버스', '').replace('서울 버스', '').replace('인천', '').replace('해', '').replace('함', '').replace('어떤', '').replace('그냥', '').replace('너무', '').replace('그러면', '').replace('때문에', '').replace('기념', '').replace('생일', '').replace('영탁 생일', '').replace('ㅋ', '').replace('ㅠ', '').replace('ㅎ', '').replace('ㅜ', '').replace('ㄱ', '').replace('ㅡ', '').replace('ㄷ', '')+" "
    for word in nltk.tokenize.word_tokenize(line):
        if word not in stopwords:
            seoul_text += word+" "
            
cheonan_wordcloud = WordCloud(font_path='NanumGothic-Regular.ttf', 
                      max_words=200, 
                      width=800, 
                      height=600,  
                      max_font_size=150).generate(cheonan_text)

seoul_wordcloud = WordCloud(font_path='NanumGothic-Regular.ttf', 
                      max_words=200, 
                      width=800, 
                      height=600,  
                      max_font_size=150).generate(seoul_text)


cheonan_wordcloud.to_file('..image/cheonan_wordcloud.png') 
seoul_wordcloud.to_file('..image/seoul_wordcloud.png')
