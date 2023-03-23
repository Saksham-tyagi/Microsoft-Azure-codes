## Script to download all the files available in a file share directory to local machine in one go

from azure.storage.fileshare import ShareClient
import os

# Set the connection string for the Azure Storage account (Change details here)
connection_string = "DefaultEndpointsProtocol=https;AccountName=myaccount;AccountKey=mykey;EndpointSuffix=core.windows.net"

# Set the file share name and directory (Change details here)
file_share_name = "FileShareName"
file_share_directory = "FileShareDirectory"

# Set the local download directory (Change details here)
local_download_directory = "/path/to/local/directory/"

# Create a ShareClient object
share_client = ShareClient.from_connection_string(connection_string, file_share_name)

# Get a reference to the file share directory
file_share_directory_client = share_client.get_directory_client(file_share_directory)

# List all the files in the directory
files_list = file_share_directory_client.list_directories_and_files()

# Iterate through each file in the list and download it
for file in files_list:
    if not file.is_directory:
        file_client = file_share_directory_client.get_file_client(file.name)
        download_path
