from gensim.models.ldamulticore import LdaMulticore
import pickle
import pandas as pd
from gensim import corpora
import email
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import re
import spacy
import csv
import email
nlp = spacy.load("en_core_web_sm")

stop_words = set(stopwords.words('english'))
def token_of_email(email):
    lemmas = nlp(email)
    # add NER
    return [w.lemma_ for w in lemmas if not w.lemma_.lower() in stop_words and w.lemma_.isalpha()]

with open("./data/model_lda_enron_11_passes", "rb") as pick:
    lda = pickle.load(pick)


paths = pd.read_csv("./data/paths.csv")["path"].to_list()

id2word = corpora.Dictionary.load_from_text('./data/test3_wordids.txt')

def email_of_path(path):
    with open(path, "r", encoding="windows-1252") as file:
            sample = email.message_from_file(file)
    return sample._payload

#flattened_topics = [val for sublist in lda_model.get_topics() for val in sublist]

topics = lda.show_topics(formatted=False, num_topics=50)

topics_union = [topic[1] for topic in topics]

from data.enroncorpus import tok

def topics_dist_of_email(path):
    #path = "./data" + path[1:]
    email = email_of_path(path)
    tokens = tok(email)
    bow = id2word.doc2bow(tokens)
    predict = lda.get_document_topics(bow,  minimum_probability=0)
    dict_of_predict = {key:value for key,value in predict}
    return dict_of_predict

#data = [topics_dist_of_email(path) for path in paths]

# df = pd.DataFrame(data)
# df.to_csv("distribution_test11.csv")

# df = pd.read_csv("distribution_test11.csv")
# df["paths"]=paths
# df.to_csv("dddtest11.csv")

df = pd.read_csv("./data/dddtest11.csv")

def mails_of_topic(topic_id, thresh=0.6):
    mails = df[df[str(topic_id)]>thresh]["paths"]
    mails = mails.map(lambda path: "./data" + path[1:])
    return mails
