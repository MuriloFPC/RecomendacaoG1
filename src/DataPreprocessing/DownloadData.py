import os
import gdown
import zipfile

from src.Utils.log import Log


def DownloadDataFromGoogleDrive(logger=Log):
    # URL of the file on Google Drive
    url = 'https://drive.google.com/uc?id=13rvnyK5PJADJQgYe-VbdXb7PpLPj7lPr'

    # Path where you want to save the downloaded file
    output_path = os.path.join(script_dir,'Data')
    ouuput_path_file = os.path.join(output_path,'Data.zip')

    if os.path.exists(ouuput_path_file):
        logger.info("Zip já existe, retornando")
        return

    # Download the file
    gdown.download(url, output_path, quiet=False)

    # Unzip the file
    with zipfile.ZipFile(ouuput_path_file, 'r') as zip_ref:
        zip_ref.extractall(ouuput_path_file)