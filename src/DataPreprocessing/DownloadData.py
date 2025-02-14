import os
import gdown
import zipfile

from src.Utils.log import Log


def DownloadDataFromGoogleDrive(logger=Log):
    # URL of the file on Google Drive
    url = 'https://drive.google.com/uc?id=13rvnyK5PJADJQgYe-VbdXb7PpLPj7lPr'

    # Path where you want to save the downloaded file
    output_path = '../../Data/data.zip'

    if not os.path.exists('../../Data'):
        os.makedirs('../../Data')

    if os.path.exists(output_path):
        logger.info("Zip já existe, retornando")
        return

    # Download the file
    gdown.download(url, output_path, quiet=False)

    # Unzip the file
    with zipfile.ZipFile(output_path, 'r') as zip_ref:
        zip_ref.extractall('../../Data')