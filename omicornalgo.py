import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import nltk
import re
import string
#nltk.download('stopwords')
stemmer = nltk.SnowballStemmer("english")
from nltk.corpus import stopwords    
stopword=set(stopwords.words('english'))

def predict(input):
    
    
    data = pd.read_csv('input/inputdata.csv')   
    data = data.dropna()

    data["text"] = data["text"].apply(clean)
    #1
    text = " ".join(i for i in data.text)
    stopwords = set(STOPWORDS)    

    #text = " ".join(i for i in data.hashtags)
    stopwords = set(STOPWORDS)    
    sentiments = SentimentIntensityAnalyzer()
    data["Positive"] = [sentiments.polarity_scores(i)["pos"] for i in data["text"]]
    data["Negative"] = [sentiments.polarity_scores(i)["neg"] for i in data["text"]]
    data["Neutral"] = [sentiments.polarity_scores(i)["neu"] for i in data["text"]]
    data = data[["text", "Positive", "Negative", "Neutral"]]
    print(data.head())

    #4
    x = sum(data["Positive"])
    y = sum(data["Negative"])
    z = sum(data["Neutral"])

    
    result =sentiment_score(x, y, z)
    return result

def clean(text):
    text = str(text).lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = [word for word in text.split(' ') if word not in stopword]
    text=" ".join(text)
    text = [stemmer.stem(word) for word in text.split(' ')]
    text=" ".join(text)
    return text

def sentiment_score(a, b, c):
    if (a>b) and (a>c):
        print("Positive 😊 ")
        result="Positive"
    elif (b>a) and (b>c):
        print("Negative 😠 ")
        result="Negative"
    else:
        print("Neutral 🙂 ")
        result="Neutral"
    return result



