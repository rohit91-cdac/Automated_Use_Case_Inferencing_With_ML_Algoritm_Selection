###################################################
## Code Snippet to Get Context from Image Store ###
###################################################

import os, uuid
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import concurrent.futures
import os

base_path = "/home/buzzy/Downloads/test"

try:
    account_url = "https://funcstorrohitb.blob.core.windows.net"
    default_credential = DefaultAzureCredential()

    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient(account_url, credential=default_credential)
    print("Connection has been set")
except Exception as e:
    print(e)


def file_upload_function(file_path, file_name):
    blob_client = blob_service_client.get_blob_client(container="all-purpose/Product_Images", blob=file_name)
    with open(os.path.join(file_path, file_name), mode='rb') as data:
        blob_client.upload_blob(data=data)
    return f"{file_name} got uploaded"

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    future_to_url = {executor.submit(file_upload_function,base_path,file_name): file_name for file_name in os.listdir(base_path) }
    for future in concurrent.futures.as_completed(future_to_url):
        file_name = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            print("%s generated an exception %s" % (file_name, exc))
        else:
            print("%s file got uploaded" % file_name)