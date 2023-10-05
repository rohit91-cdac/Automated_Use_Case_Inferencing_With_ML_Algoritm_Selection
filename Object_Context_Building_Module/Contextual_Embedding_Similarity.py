from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pymongo import MongoClient
from sentence_transformers  import SentenceTransformer, util
from sklearn.metrics.pairwise import cosine_similarity
import os
import numpy as np
import pandas as pd

class long_description_curation:

    long_description_list = []

    def __init__(self):
        self.mongo_client = MongoClient('mongodb://localhost:27017/')
        self.db = self.mongo_client.retailDB
        self.collect_online_store_II = self.db['Online_Store_Two']

    def populate_long_document(self):

        for each_record in self.collect_online_store_II.find():
            self.long_description_list.append(each_record['description'])

        print(f"Total Length of Long Description Documents is {len(self.long_description_list)}")
        return self.long_description_list


class context_building:

    def __init__(self, long_description):
        self.long_description = long_description
        self.model = SentenceTransformer('all-MiniLM-L6-v2', device='cuda')
        self.map_topic_description = {}

    def encode_long_description(self):
        description_embeddings = self.model.encode(self.long_description)
        print(f"Length of Embeddings generated --> {description_embeddings}")
        return description_embeddings

    def get_similar_long_description(self, list_topic_text):
        representation_dict = {}
        min_index_list = []
        encode_topics = self.model.encode(list_topic_text)
        long_desc_embeddings = self.encode_long_description()
        calculate_cos_sim = [list(map(lambda x: cosine_similarity(x.reshape(1, -1), each_topic_embed.reshape(1, -1)), long_desc_embeddings))
                             for each_topic_embed in encode_topics]
        print(f"Length of Cos Sim calculated is --> {len(calculate_cos_sim)}")
        print(f"Value -> {calculate_cos_sim[0]}")
        print("Assigning the Top 3 Long Description per Topic")
        for each in calculate_cos_sim:
            each = list(map(lambda x: x[0][0], each))
            print(f" Cal Arg Partition {np.argpartition(each, -3)[-3:]}")
            min_index_list.append(np.argpartition(each, -3)[-3:])

        for each_index in range(len(list_topic_text)):
            index_list = min_index_list[each_index]
            list_map = list(map(lambda x: self.long_description[x], index_list))
            representation_dict[list_topic_text[each_index]] = list_map

        return representation_dict


if __name__ == "__main__":
    print("Initiating program to prepare contextual embedding to calculate similarity \n")
    description_curation = long_description_curation()
    get_description_list = description_curation.populate_long_document()
    print(get_description_list[0])
    similarity_obj = context_building(get_description_list)
    file_path = os.path.join(os.getcwd(), 'Context_Short_Topic.txt')
    with open(file_path, 'r') as file_read:
        list_topic_text = file_read.readlines()
    topic_to_context_map = similarity_obj.get_similar_long_description(list_topic_text=list_topic_text)
    context_df = pd.DataFrame.from_dict(topic_to_context_map, orient='index', columns=['Context_1', 'Context_2', 'Context_3'])
    print(context_df.head())




