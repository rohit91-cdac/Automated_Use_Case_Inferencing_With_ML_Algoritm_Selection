#####################################################################
## This Script maps the most approprate object from Image Context ###
## to the Context From Short Desccription                         ###
#####################################################################
import os.path
from itertools import chain
from sentence_transformers import SentenceTransformer, util
from bertopic import BERTopic
import torch


def load_model(model_path: str, model_folder: str):
    loaded_model = BERTopic.load(os.path.join(model_path, model_folder))
    return loaded_model


if __name__ == "__main__":
    print("Reading the File Describing the Object File")
    with open(os.path.join(os.getcwd(), "Image_Context_File"), 'r') as image_context:
        all_object_file = image_context.readlines()
        all_object_list = list(map(lambda x: x.split(','), all_object_file))
        all_object_master_list = list(chain.from_iterable(all_object_list))
        print(f"Total length of Object List Is --> {len(all_object_master_list)}")
    print("Loading Sentence Transformer MOdel")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("Encoding Model Objects")
    image_object_embeddings = model.encode(all_object_master_list)
    print("Length of Image Encoded Objects: \n")
    print(len(image_object_embeddings))
    print("Loading the Custom Trained Topic Model")
    loaded_model = load_model(os.getcwd(), 'retail_db_topic_model_v2')
    get_topic_value = loaded_model.get_topic_info().to_dict('index')
    # Removing -1 and 0 Topic Cluster
    get_topic_value = {k: v for k, v in get_topic_value.items() if get_topic_value[k]['Topic'] not in [-1, 0]}
    get_topic_value = {k: {"Topic": get_topic_value[k]['Topic'],
                           "Count": get_topic_value[k]['Count'],
                           "Name": set(get_topic_value[k]['Name'].replace('_', ' ').split(" ")[1:])} for k, v in
                       get_topic_value.items()}
    get_topic_value = {k: {"Topic": get_topic_value[k]['Topic'],
                           "Count": get_topic_value[k]['Count'],
                           "Name": ' '.join([word for word in get_topic_value[k]['Name'] if not word.isdigit()])} for
                       k, v in get_topic_value.items() if len(get_topic_value[k]['Name']) > 3}

    file_path = os.path.join(os.getcwd(), 'Context_Short_Topic.txt')
    for each_topic in get_topic_value:
        if get_topic_value[each_topic]["Topic"] in range(1, 23):
            topic_document_list = get_topic_value[each_topic]['Name'].split(" ")
            print(f"Encoding Topic Document --> {topic_document_list}")
            encode_topic_document = model.encode(list(topic_document_list))
            sim_score_list_tensor = list(map(lambda x: util.cos_sim(image_object_embeddings, x), encode_topic_document))
            object_model_topics = " ".join(list(map(lambda x: all_object_master_list[torch.argmax(x).item()],
                                                    sim_score_list_tensor))).strip()
            print(object_model_topics)
            with open(file_path, 'a') as file_append:
                file_append.write(object_model_topics)
                file_append.write("\n")


