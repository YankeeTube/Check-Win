from newspaper import Article
from konlpy.tag import Kkma
from konlpy.tag import Twitter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize
import numpy as np

class auto_post():

    def __init__(self):
        self.twitter = Twitter()
        self.kkma = Kkma()

    def newsdata(self):
        url = "http://www.boannews.com/media/view.asp?idx=58586&mkind=1&kind=1"
        data = Article(url)
        data.download()
        data.parse()
        data = data.text.split("\n")
        sentences = self.kkma.sentences(data[2]) # 문장단위
        for idx in range(0, len(sentences)):
            if len(sentences[idx]) <= 10:
                sentences[idx - 1] += (' ' + sentences[idx])
                sentences[idx] = ''
        return sentences

if __name__ == '__main__':
    ap = auto_post()
    print(ap.newsdata())