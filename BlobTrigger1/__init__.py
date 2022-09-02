import logging
import os
import azure.functions as func
from azure.core.exceptions import ResourceNotFoundError, ServiceRequestError
from azure.storage.blob import BlobClient, BlobLeaseClient


def main(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")
    # Get environment variables 
    source_conn_string = os.environ["source_conn_string"]
    dest_conn_string = os.environ["dest_conn_string"]
    sas_token = os.environ["sas_token"]
    # Assign container names
    source_container_name = "samples-workitems"
    dest_container_name = "outcontainer"

    # Get the blob_name from the event
    blob_name = myblob.name.split("/")[-1]

    try:
        # Create a BlobClient representing the source blob.
        source_blob = BlobClient.from_connection_string(source_conn_string, source_container_name, blob_name)

        # Lease the source blob for the copy operation
        # to prevent another client from modifying it.
        lease = BlobLeaseClient(source_blob)
        # lease.acquire()

        # Get the source blob's properties and display the lease state.
        source_props = source_blob.get_blob_properties()
        print("Lease state: " + source_props.lease.state)

        # Create a BlobClient representing the
        # destination blob with a unique name.
        dest_blob = BlobClient.from_connection_string(dest_conn_string, dest_container_name, blob_name + "-Copy")
        
        # Start the copy operation.
        dest_blob.start_copy_from_url(source_blob.url+sas_token)

        # Get the destination blob's properties to check the copy status.
        properties = dest_blob.get_blob_properties()
        copy_props = properties.copy

        # Display the copy status.
        print("Copy status: " + copy_props["status"])
        print("Copy progress: " + copy_props["progress"])
        print("Completion time: " + str(copy_props["completion_time"]))
        print("Total bytes: " + str(properties.size))

        if (source_props.lease.state == "leased"):
            # Break the lease on the source blob.
            lease.break_lease()

            # Update the destination blob's properties to check the lease state.
            source_props = source_blob.get_blob_properties()
            print("Lease state: " + source_props.lease.state)

    except ResourceNotFoundError as ex:
        print("ResourceNotFoundError: ", ex.message)

    except ServiceRequestError as ex:
        print("ServiceRequestError: ", ex.message)