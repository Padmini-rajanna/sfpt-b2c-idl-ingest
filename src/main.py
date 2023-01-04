import pysftp
from google.cloud import storage
import os
from loguru import logger

os.environ["GCLOUD_PROJECT"] = 'v135-5339-logistic-mon-dev'
Hostname = "13.79.163.198"
Username = "00119_IDL_NL"
Password = ">F154<mkOL"
client = storage.Client(project='v135-5339-logistic-mon-dev')
bucket_name = 'sftp-idl-b2c-import'


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    logger.info(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )


def connector():
    with pysftp.Connection(host=Hostname, username=Username, password=Password) as sftp:
        print("Connection successfully established ... ")
        # Switch to a remote directory
        sftp.cwd('/IN/B2C_Order_status/')

        # Obtain structure of the remote directory '/opt'
        directory_structure = sftp.listdir_attr()
        for attr in directory_structure:
            # Print data
            logger.info(attr.filename, attr)
            # Define the remote file that you want to download

            remoteFilePath = '/IN/B2C_Order_status/' + attr.filename
            localFilePath = './' + attr.filename

            sftp.get(remoteFilePath, localFilePath)
            upload_blob(bucket_name, localFilePath, attr.filename)

        logger.info('Successful uploading of files')
