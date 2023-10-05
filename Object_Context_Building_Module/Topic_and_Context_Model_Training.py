import nltk
from bertopic import BERTopic
from bertopic.representation import KeyBERTInspired, MaximalMarginalRelevance, PartOfSpeech
import pandas as pd
from typing import List, Set
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from itertools import chain
import string
from sentence_transformers import SentenceTransformer
from umap import UMAP
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer


def prepare_corpus(sentence_list: List[str], stopwords_list: Set):
    pattern = r"""(?x)  # set flag to allow verbose regexps
          (?:[A-Z]\.)+      # abbreviations, e.g. U.S.A.
        | \w+(?:-\w+)*      # words with optional internal hyphens
        | \$?\d+(?:\.\d+)?%?# currency and percentages, e.g. $12.40, 82%
        | \.\.\.            # ellipsis
        | [][.,;"'?():-_`]  # these are separate tokens; includes ], [
        """
    text = 'That U.S.A. poster-print costs $12.40...'
    print(nltk.regexp_tokenize(text, pattern))
    extract_string_list = [line.split(',') for line in sentence_list]
    flatten_list = list(chain.from_iterable(extract_string_list))
    corpus_tokenize_word = [nltk.regexp_tokenize(each_des, pattern) for each_des in flatten_list]
    corpus_clean = []
    for each_list in corpus_tokenize_word:
        for each_word in each_list:
            if each_word not in stopwords_list and each_word not in string.punctuation:
                corpus_clean.append(each_word)
    print(len(flatten_list))
    print(f"Sample String {flatten_list[100]}")
    print(f"Sample Word Token {corpus_tokenize_word[0]}")
    print(f"Length of original corpus {len(corpus_tokenize_word)}")
    print(f"Length of clean corpus is {len(corpus_clean)}")
    return corpus_clean


def pre_calculate_embeddings(corpus: List):
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = embedding_model.encode(corpus, show_progress_bar=True)
    return embedding_model, embeddings


def umap_dimensional_reduction():
    # Necessary Dimensionality Reduction techniques for reducing the Dimension of the Embedding
    umap_model = UMAP(n_neighbors=15, n_components=5, min_dist=0.0, metric='cosine', random_state=42)
    return umap_model


def hdbscan_clustering():
    hdbscan_model = HDBSCAN(min_cluster_size=150, metric='euclidean', cluster_selection_method='eom', prediction_data=True)
    return hdbscan_model


def default_representation():
    vectorizer_model = CountVectorizer(stop_words='english', min_df=2, ngram_range=(1, 3))
    return vectorizer_model

def fine_tune_representation():
    # KeyBert
    keybert_model = KeyBERTInspired()

    #Part of Speech
    pos_model = PartOfSpeech('en_core_web_sm')

    # MMR
    # mmr_model = MaximalMarginalRelevance(diversity=0.3)

    # All Representation Models
    representation_model = {
        "KeyBert": keybert_model
        # , "MMR": mmr_model
        # , "POS": pos_model
    }
    return representation_model


def  initiate_training(embedding_model, umap_model, hdbscan_model, vectorizer_model, representation_model, corpus, embeddings):
    topic_model = BERTopic(
        embedding_model=embedding_model,
        umap_model=umap_model,
        hdbscan_model=hdbscan_model,
        vectorizer_model=vectorizer_model,
        representation_model=representation_model,
        low_memory=True,
        # Hyperparameters
        top_n_words= 10,
        verbose=True,
        min_topic_size=40
    )

    # Train Model
    topics, probs = topic_model.fit_transform(corpus, embeddings)

    return topics, probs

def truncate_short_description_file(filename, num_docs=0.1, num_lines=0.1):
  document_corpus = []
  with open(filename, 'r') as short_file_read:
    read_file: List = short_file_read.readlines()
    print("Limiting the number of Documents")
    # Limit the Number of Lines to 70%
    if len(read_file) > 1:
      total_lines = int(len(read_file) * num_docs)
      read_file_truncated = read_file[:total_lines]
    else:
      read_file_truncated = read_file
    #Truncating each document to 70%
    print("Limiting the number of lines for each doc")
    for each_doc in read_file_truncated:
      each_doc_list = each_doc.split(',')
      each_doc_truncated = each_doc_list[0: int(len(each_doc_list) * num_lines)]
      each_doc_string = ' , '.join(each_doc_truncated)
      document_corpus.append(each_doc_string)
    return document_corpus


def load_model(model_path: str, model_folder: str):
    loaded_model = BERTopic.load(os.path.join(model_path, model_folder))
    return loaded_model


if __name__ == "__main__":
    # print("Reading Short Description File")
    # short_desc_file_path = os.path.join(os.getcwd(), 'ShortDescriptionFile.txt')
    # print("Truncating the Actual Document Corpus")
    # get_truncated_document = truncate_short_description_file(filename=short_desc_file_path)
    # stop_english = set(stopwords.words('english'))
    # print("Preparing the Corpus")
    # corpus = prepare_corpus(get_truncated_document, stop_english)
    # print("Pre-Calculating Embeddings")
    # embedding_model, embeddings = pre_calculate_embeddings(corpus=corpus)
    # print("Initiating Dimensionality Reduction Model")
    # umap_model = umap_dimensional_reduction()
    # print("Initiating HDBScan Clustering Model")
    # hdbscan_model = hdbscan_clustering()
    # print("Creating the Default Representation")
    # vectorizer_model = default_representation()
    # print("Preparing the Representation Model")
    # representation_model = fine_tune_representation()
    # print("Finally.. Initiating the Topic Modelling Training")
    # topics, probs = initiate_training(
    #     embedding_model=embedding_model,
    #     umap_model=umap_model,
    #     hdbscan_model=hdbscan_model,
    #     vectorizer_model=vectorizer_model,
    #     representation_model=representation_model,
    #     corpus=corpus,
    #     embeddings=embeddings
    # )
    # print(f"Identified Topics are {topics.get_topic_info()}")
    print("Loading the trained Model")
    loaded_model = load_model(os.getcwd(), 'retail_db_topic_model_v2')
    all_topics = loaded_model.get_topics()
    a = {k: v for k, v in sorted(all_topics.items(), key=lambda x: x[1])}
    # print(loaded_model.get_topic_info().to_dict('index'))
    get_topic_value = loaded_model.get_topic_info().to_dict('index')
    for each_topic in get_topic_value:
        if get_topic_value[each_topic]["Topic"] in range(1, 12):
            print(f"Topic_Count -> {get_topic_value[each_topic]['Count']} Topic_Name --> {get_topic_value[each_topic]['Name']}")
    print(loaded_model.get_topic(11))

