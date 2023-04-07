# Nextcloud Talk Bot: File Operations

NextcloudFileOperations is designed to interact with a Nextcloud server, providing functionality to list, upload, and delete files in a user's Nextcloud folder.

## Initialization:

To create an instance of the NextcloudTalkExtractor class, you will need the following information:

- base_url: The base URL for the Nextcloud server.
- username: The username for the Nextcloud user account.
- password: The password for the Nextcloud user account.
- nc_remote_folder: (Optional) The path of the remote folder on the Nextcloud server.
- local_folder: (Optional) The path of the local folder on the user's machine.
- remote_file: (Optional) The name of the remote file in the Nextcloud folder.

    
## Methods:

1. list_files_in_nextcloud_folder()
    Purpose: Lists all files in a Nextcloud folder
    Returns: A list containing names of the files in the folder.

2. send_local_file_to_nextcloud_folder()
    Purpose: Uploads local files to a specified Nextcloud folder. 
    This method iterates through all the files in the local folder, uploads each file to the specified Nextcloud folder, 
    and deletes the local file upon successful upload.

3. delete_remote_file_in_nextcloud()
    Purpose: Deletes a remote file in the specified Nextcloud folder. 
    This method sends a DELETE request to the Nextcloud server to remove the remote file located in the user's specified folder.