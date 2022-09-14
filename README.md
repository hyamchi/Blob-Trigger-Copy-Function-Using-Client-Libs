# Blob-Triggered-Azure-Function V2
### Copy a blob with Client libraries
This function gets triggered when a new blob is created in the source container and makes a copy of the new blob in the destination container with the help of **Client Libraries**. 

My blog about this project:

https://medium.com/@yamchi/python-blob-triggered-azure-function-to-copy-a-newly-created-blob-to-a-backup-container-5f5a82a24ad4

# Local Testing:
Initially install the requirements and then start the function:
```
$ pip install -r requirements.txt 
$ func start
```
You should have a `local.settings.json` file in the root dir of the project and specify the values for connection strings and AzurewebJobsStorage:
![Untitled4](https://user-images.githubusercontent.com/84933778/188228950-2aee732a-b37b-4bdf-95c0-d3c4b0372a57.png)


To get the connection string for an Azure Storage Account go to the storage account and from the left pane select “Access Keys” and then click on “Show” and copy the value.
![Untitled1](https://user-images.githubusercontent.com/84933778/187779260-a68254d2-00e7-4cac-9b54-14b75e5068dc.png)
### Troubleshoot 1:
For any certificate problem, refer to the following links:
https://stackoverflow.com/questions/27835619/urllib-and-ssl-certificate-verify-failed-error/42334357#42334357:~:text=On%20Windows%2C%20Python%20does%20not%20look%20at%20the%20system%20certificate%2C%20it%20uses%20its%20own%20located%20at%20%3F%5Clib%5Csite%2Dpackages%5Ccertifi%5Ccacert.pem.

https://pypi.org/project/pip-system-certs/

### Troubleshoot 2:
If you had an authorization problem, you most probably need SAS Token for the copy process. 

# Testing The Function in Azure:
To test the function in Azure, you need to store the connection values in the Function App's `Application Settings`:
![Untitled3](https://user-images.githubusercontent.com/84933778/187781361-e9f60fc0-0c82-4eb9-9df1-43253145da96.png)

For more info refer to the following links:

https://azuresdkdocs.blob.core.windows.net/$web/python/azure-storage-blob/12.0.0/azure.storage.blob.html#


