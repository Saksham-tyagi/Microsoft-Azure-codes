## This code Migrate/copies all the files from fileshare directory to a blob container

import time
from azure.storage.blob import BlobClient
from azure.storage.fileshare import ShareClient
from azure.core.exceptions import ResourceNotFoundError, ServiceRequestError


## Both Account name and Access key can be found in Access Keys tab in a Storage account, add them here
## goto storage account-> Security + networking -> Access Keys)
account_name = 'Provide Storage account name'
storage_account_access_key = "Provide storage account access key"

## Add name of file share in place of example
file_share_name = 'Example'

## Add fileshare directory name here (like dir_name = dir1)
## And if you have subdirectories inside you can add (like this dir_name = dir1/dir2)
dir_name = 'dir1/dir2'

## Add Container name like (container_name = sample-container)
## And if you also want to use sub folders, you can add like (container_name = 'sample-container/folder1')
container_name = 'sample-container/folder1'

# Creating a Dynamic Connection String using account_name and storage_account_access_key
connection_string = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={storage_account_access_key};EndpointSuffix=core.windows.net"

## Add Sas Token from Azure Storage account
## (goto storage account-> Security + networking -> Shared access signature)
sas_token = "sas token"

try:
    
    # Creating a Share Client
    file_client_listFiles = ShareClient.from_connection_string(connection_string, share_name=file_share_name)
    print(f"File share url :- {file_client_listFiles.url}")

    # Iterating in directory using for loop
    for item in list(file_client_listFiles.list_directories_and_files(dir_name)):

        # Storing the name of the file in a variable
        fileshare_file_name =  item["name"]
        print(f"File Name :- {fileshare_file_name}")

        # Creating a url for the file
        file_share_url = f"{file_client_listFiles.url}/{dir_name}/{fileshare_file_name}{sas_token}"
        print(f"file_share_url:- {file_share_url}")

        # Create the client object using the storage URL and the credential
        blob_client = BlobClient.from_connection_string(conn_str=connection_string, container_name=container_name, blob_name=fileshare_file_name)
        print(f"Blob Container Url :- {blob_client.url}")

        # Starting the copy from file share (source) to blob conatiner (destination)
        blob_client.start_copy_from_url(file_share_url)

        # Display the copy status.
        while True:
            
            properties = blob_client.get_blob_properties()
            copy_props = properties.copy
            if copy_props["status"] == 'pending':
                print(f"Copy status: {copy_props['status']}")
                time.sleep(4.0)
            elif copy_props["status"] == 'success':
                print(f"Copy status: {copy_props['status']}")
                print(f"File Name :- {fileshare_file_name}, Copied Successfully.")
                break 
            else:
                print(f"Copy status: {copy_props['status']}")
                break
        
        print(f"Copy progress: {copy_props['progress']}")
        print(f"Completion time: {copy_props['completion_time']}")
        print(f"Total bytes: {properties.size}")            

except ResourceNotFoundError as ex:
    print(f"ResourceNotFoundError: {ex.message}")

except ServiceRequestError as ex:
    print(f"ServiceRequestError: {ex.message}")
