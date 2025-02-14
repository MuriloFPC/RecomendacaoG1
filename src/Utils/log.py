from pydantic import BaseModel
import logging
import sys

class Log(BaseModel):
    def __init__(self, createFile ,**data):
        super().__init__(**data)

        if createFile:
            logging.basicConfig(
                level=logging.INFO,
                format="%(asctime)s - %(levelname)s - %(message)s",
                handlers=[
                    logging.FileHandler("api_logs.log"),  # Salvar logs em arquivo
                    logging.StreamHandler(sys.stdout)  # Mostrar logs no terminal (stdout)
            ])

        else:
            logging.basicConfig(
                level=logging.INFO,
                format="%(asctime)s - %(levelname)s - %(message)s",
                handlers=[
                    logging.StreamHandler(sys.stdout)  # Mostrar logs no terminal (stdout)
            ])

    def info(self, message):
        logging.info(message)

    def error(self, message):
        logging.error(message)