import os

from pymongo import MongoClient
import time


if __name__ == "__main__":
    content_list_I = []
    content_list_II = []
    client = MongoClient('mongodb://localhost:27017/')
    db = client.retailDB
    collect_online_store_I = db['Online_Store_One']
    collect_online_store_II = db['Online_Store_Two']
    current_time = time.perf_counter()
    for each_collection in [collect_online_store_I, collect_online_store_II]:
        if each_collection.name == 'Online_Store_One':
            for each_document in each_collection.find():
                content_list_I.append(each_document['description'])
        elif each_collection.name == 'Online_Store_Two':
            for each_document in each_collection.find():
                content_list_II.append(each_document['description'])

    print(f"Total time taken to parse all the Description Metadata is {time.perf_counter() - current_time}")
    print(f"Length of Online Store I descriptions {len(content_list_I)}")
    with open(os.path.join(os.getcwd(), 'ShortDescriptionFile.txt'), 'w') as retail_out_I:
        context_I = ' , '.join(content_list_I)
        retail_out_I.write(context_I)
        print("Context File I Written")
    with open(os.path.join(os.getcwd(), 'LongDescriptionFile.txt'), 'w') as retail_out_II:
        context_II = ' , '.join(content_list_II)
        retail_out_II.write(context_II)
        print("Context File II Written")
    print(f"Length of Online Store II descriptions {len(content_list_II)}")

