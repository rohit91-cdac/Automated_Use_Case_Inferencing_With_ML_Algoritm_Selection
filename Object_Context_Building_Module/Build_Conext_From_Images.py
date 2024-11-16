import ultralytics
from ultralytics import YOLO
import numpy as np
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.identity import DefaultAzureCredential
import asyncio
import aiohttp
from aiohttp import ClientSession
import os
import time
from tqdm import tqdm
from itertools import chain


ultralytics.checks()

storage_account_url = "https://funcstorrohitb.blob.core.windows.net"
container_name = "all-purpose"

def get_blob_client(account_url):
    try:
        default_credential = DefaultAzureCredential()
        # Create the BlobServiceClient object
        blob_service_client = BlobServiceClient(account_url, credential=default_credential)
        print("Connection has been set")
    except Exception as e:
        print(e)
    return blob_service_client


def append_blobs_list(blob_service_client: BlobServiceClient, container_name):
    product_image_list_urls = []
    container_client = blob_service_client.get_container_client(container=container_name)
    print("Gettng List of Blobs")
    blob_list = container_client.list_blobs(prefix="/Product_Images",timeout=20)
    for each_blob in blob_list:
        print(f"Adding Blob --> {each_blob.name}")
        product_image_list_urls.append(f"{storage_account_url}/{container_name}/{each_blob.name}")
    return product_image_list_urls

async def infer_from_images(model, url: str):
    print(f"Inferring Labels for Image -> {url.split('/')[-1]}")
    results = model.predict(url)
    top_5_indexes = results[0].probs.top5
    list_names = [results[0].names[i] for i in top_5_indexes]
    return list_names


async def get_top_5_prediction(model, urls):
    """Prediction of top image result"""
    async with ClientSession() as session:
        keyword_list = []
        async_task_list = []
        for each_url in urls:
            async_task_list.append(infer_from_images(model=model, url=each_url))
    return await asyncio.gather(*async_task_list)


if __name__ == "__main__":
    start = time.perf_counter()
    blob_client = get_blob_client(account_url=storage_account_url)
    product_image_url = append_blobs_list(blob_service_client=blob_client, container_name=container_name)
    print(f"Total number of imaged to be inferred for is --> {len(product_image_url)}")
    print(f"Initializing the model yolov8n-cls.pt")
    model = YOLO("yolov8n-cls.pt")
    parent_dir = os.getcwd()
    os.chdir(os.path.join(os.getcwd(),"Temp_Folder/test"))
    product_image_url_test=["https://funcstorrohitb.blob.core.windows.net/all-purpose/Product_Images/1000472.jpg",
    "https://funcstorrohitb.blob.core.windows.net/all-purpose/Product_Images/1000609.jpg","https://funcstorrohitb.blob.core.windows.net/all-purpose/Product_Images/1000807.jpg"]
    get_list_keywords = asyncio.run(get_top_5_prediction(model=model, urls=product_image_url))
    get_list_keywords_flattten = set(list(chain.from_iterable(get_list_keywords)))
    print("Writing the inferred top 5 classes to a text file")
    with open(os.path.join(parent_dir,'Image_Context_File'),'w') as context_file:
        context_string = ' , '.join(get_list_keywords_flattten)
        context_file.write(context_string)
    print(f"Total time take to complete the process --> {time.perf_counter() - start}")




