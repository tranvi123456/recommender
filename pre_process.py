
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re

nltk.download('stopwords')
nltk.download('wordnet')  

lemma = WordNetLemmatizer()
stop_words = stopwords.words('english')

def pre_process(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    lower = [word.lower() for word in text.split()]
    stw = [word for word in lower if word not in stop_words]
    result = [lemma.lemmatize(word) for word in stw]
    results = " ".join(result)
    return results
