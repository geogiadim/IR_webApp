from nltk.tokenize import word_tokenize
from greek_stemmer import GreekStemmer  # https://github.com/alup/python_greek_stemmer
import pandas as pd
import unicodedata
import numpy as np
from numpy import dot
from numpy.linalg import norm
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer


np.set_printoptions(threshold=np.inf)
df = pd.read_csv("./Files/Greek_Parliament_Proceedings_1989_2020_DataSample.csv")
stemmer = GreekStemmer()
global_names = df['member_name'].unique()
global_parties = df['political_party'].unique()


def get_df():
    return df


def remove_stopwords_and_stem(stop_words, speech_one):
    word_tokens = word_tokenize(speech_one)
    filtered_sentence = [w for w in word_tokens if (not w.lower() in stop_words) and w.isalnum()]

    speech_temp = []
    for w in filtered_sentence:
        # https://stackoverflow.com/a/62899722
        d = {ord('\N{COMBINING ACUTE ACCENT}'): None}
        word = unicodedata.normalize('NFD', w).upper().translate(d)
        speech_temp.append(stemmer.stem(word))

    return speech_temp


def count_words(s):
    counter = Counter(s)
    common_words = (counter.most_common())
    return common_words


def build_index():
    inverted_index = {}
    for doc, s in enumerate(df['processed_speech']):
        common_words = count_words(s)
        for w in common_words:
            word = w[0]
            if word not in inverted_index.keys():
                inverted_index[word] = [doc]
            else:
                inverted_index[word].append(doc)
    return inverted_index


# k represents top-k results
def make_query(stop_words, tfidf_vectorizer, tfidf_matrix, query, inverted_index):
    processed_query = remove_stopwords_and_stem(stop_words, query)
    unique_words = set(processed_query)
    if any([w in inverted_index for w in processed_query]):
        relevant_docs = set()
        cos_sim_list = []
        # print([processed_query])
        tfidf_query = tfidf_vectorizer.transform([processed_query])
        ready_query = tfidf_query.toarray()[0]
        for query_word in unique_words:
            # Calculating document vectors
            if query_word in inverted_index:
                for doc in inverted_index[query_word][1:]:  # first element is the idf
                    relevant_docs.add(doc)
        for doc in relevant_docs:
            cos_sim_list.append([doc, cosine_similarity(ready_query, tfidf_matrix[doc])])
        results = sorted(cos_sim_list, key=lambda item: item[1], reverse=True)[:]
        return results
    return


def cosine_similarity(query, doc):
    cos_sim = dot(query, doc) / (norm(query) * norm(doc))
    return cos_sim


def main(query):
    # import nltk
    # nltk.download('punkt')
    # reading and store stop words
    stop_words_list = []
    with open('./Files/stopwords.txt', 'r', encoding='utf8') as filestream:
        for line in filestream:
            stop_words_list.append(line.lstrip().rstrip())
    stop_words = set(stop_words_list)

    # create new column in dataframe. Each row is a processed speech
    df['processed_speech'] = [remove_stopwords_and_stem(stop_words, i) for i in df['speech']]
    df['year'] = [df['sitting_date'][y][-4:] for y in range(df.shape[0])]  # new column year

    # init tfidf vectorizer
    tfidf_vectorizer = TfidfVectorizer(tokenizer=lambda i: i, lowercase=False,
                                       smooth_idf=False)  # https://stackoverflow.com/a/31338009

    # 2d array. columns are each unique word. rows are speeches
    # values are weights of each word
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['processed_speech'])
    tfidf_matrix = tfidf_matrix.toarray()

    inv_index = build_index()

    return make_query(stop_words, tfidf_vectorizer, tfidf_matrix, query, inv_index)
