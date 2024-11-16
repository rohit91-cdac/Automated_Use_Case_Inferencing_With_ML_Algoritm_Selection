
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.base import BaseEstimator, TransformerMixin
import logging
from sklearn.preprocessing import LabelEncoder


class FeatureSet(TransformerMixin, BaseEstimator):

    def __init__(self):
        pass

    def fit(self, X, Y=None):
        return X.iloc[:, 0:512]

    def transform(self, X):
        return np.array(X)


class LabelEncoderTransform(TransformerMixin, BaseEstimator):

    def __init__(self):
        self.le = LabelEncoder()

    def fit(self, X, Y=None):
        self.le.fit(X.iloc[:-1])
        return X

    def transform(self, X):
        return self.le.transform(X[:-1])


def universal_sentence_encoder(use_case_df: pd.DataFrame):
    module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
    model = hub.load(module_url)
    logging.info("module %s loaded" % module_url)

    def embed(input_sent):
        return model(input_sent)

    use_case_list = list(use_case_df['Use_Cases'])
    sentence_embeddings = embed(use_case_list).numpy()
    logging.info(f"Total Number of generated Embeddings are {len(sentence_embeddings)}")
    logging.info(f"Total Number of Use-Case {len(use_case_df)}")
    logging.info(f"Length of single embedding {len(sentence_embeddings[0])}")
    return pd.DataFrame(sentence_embeddings, columns=list(range(0, 512)))


def model_data_prepare(use_case_df: pd.DataFrame):
    get_embedded_data = universal_sentence_encoder(use_case_df)
    get_labels = use_case_df[['ML_Algo']]
    concat_feat_label = pd.concat([get_embedded_data, get_labels], axis = 1)
    concat_feat_label.to_csv("Embedding_Data.csv")
    combine_feat_label = FeatureUnion(
        [
            ("Feature_Combine", FeatureSet()),
            ("Label_Encoder", LabelEncoderTransform())
        ]
    )
    get_transformed_data = combine_feat_label.fit_transform(concat_feat_label)
    print(get_transformed_data)
    return get_embedded_data


if __name__ == "__main__":
    FORMAT = "%(asctime)s %(levelname)-8s %(message)s"
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)
    logging.info("Initializing Fast Text Model")
    logging.info("Reading the Data File for Processing")
    use_case_data_file = pd.read_csv("/media/buzzy/Rohit_Hard_/"
                                     "Automated_Use_Case_Inferencing_With_ML_Algoritm_Selection/"
                                     "Object_Context_Building_Module/Use_Case_Sampling/"
                                     "BERT-NER-dev/Final_Use_Case_List_With_Algo_Label.csv")
    logging.debug(use_case_data_file.head())
    sentence_embeds = universal_sentence_encoder(use_case_df=use_case_data_file)
    get_transformed_data = model_data_prepare(use_case_df=use_case_data_file)


