from read_data import read_data
import time
import torch
from hdbscan import HDBSCAN
from bertopic import BERTopic
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
import jieba
from sentence_transformers import SentenceTransformer, models

model_path = 'bert-base-chinese'

batch_size = 32
max_len = 512
device = 'cuda' if torch.cuda.is_available() else 'cpu'
pooling_mode = 'mean'

def tokenize_zh(text):
    words = list(jieba.cut(text, cut_all=False) )
    return words

def modeling(texts, min_cluster_size = 10, min_samples = 5):
    word_embedding_model = models.Transformer(model_path, 
                                          max_seq_length=max_len)
    pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension() , pooling_mode = pooling_mode)
    sentence_model = SentenceTransformer(modules=[word_embedding_model, pooling_model] , device=device)
    vectorizer_model = CountVectorizer(ngram_range=(1, 3),
                                   tokenizer=tokenize_zh)
    hdbscan_model = HDBSCAN(min_cluster_size=min_cluster_size, 
                        min_samples=min_samples,
                        metric='euclidean', 
                        prediction_data=True)
    topic_model = BERTopic(embedding_model=sentence_model, 
                       vectorizer_model=vectorizer_model,
                       hdbscan_model=hdbscan_model,
                       top_n_words=10,
                       min_topic_size=15,
                       nr_topics='auto',
                       calculate_probabilities=True)
    topics, probabilities = topic_model.fit_transform(texts)
    #print(topic_model.get_topic_info())
    return topics, probabilities

if __name__ == '__main__':
    contents = read_data(n = 1000)
    start = time.time()
    topics, probabilities = modeling(contents)
    now = time.time()
    s = round(now - start, 1)
    print('time:', s)
    # 1000 -- 51.8s    10000 -- 372.1s
