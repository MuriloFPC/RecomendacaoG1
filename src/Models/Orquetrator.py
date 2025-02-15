from src.DataPreprocessing.DownloadData import DownloadDataFromGoogleDrive
from src.Models.Train.MultiArmedBandit import TrainModelMAB
from src.Utils.log import Log
from src.Models.Train.FAISS import TrainModel as TrainModelFAISS

_logger = Log(True)


DownloadDataFromGoogleDrive(_logger)
TrainModelFAISS(_logger)
TrainModelMAB(_logger)
