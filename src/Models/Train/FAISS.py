import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import faiss
from sklearn.decomposition import TruncatedSVD
import pickle
import nltk
from nltk.corpus import stopwords

from src.Utils.train import read_all_csv_files_in_folder
from src.Utils.variables import GetVariable, script_dir


def TrainModel(_logger):
    _logger.info('Iniciando treinamento do modelo FAISS...')
    news_data = read_all_csv_files_in_folder(os.path.join(script_dir,GetVariable('NewsPath')))
    
    news_data["content"] = news_data["title"] + " " + news_data["body"] + " " + news_data["caption"]

    _logger.info('Iniciando vetorização do conteúdo das notícias...')
    # Baixar a lista de stop words
    nltk.download("stopwords")
    stop_words_pt = stopwords.words("portuguese")

    # Vetorização do conteúdo das notícias
    vectorizer = TfidfVectorizer(stop_words=stop_words_pt, max_features=50000)
    tfidf_matrix = vectorizer.fit_transform(news_data["content"])

    # Reduzir para 300 dimensões (ou ajuste para seu caso)
    svd = TruncatedSVD(n_components=300)
    tfidf_reduced = svd.fit_transform(tfidf_matrix)

    _logger.info('Iniciando criação do índice FAISS...')
    # Criar índice FAISS com a matriz reduzida
    index = faiss.IndexFlatL2(tfidf_reduced.shape[1])
    index.add(tfidf_reduced.astype("float32"))

    baseOutputPath = os.path.join(script_dir,GetVariable('ModelOutputPath'),'FAISS/')

    os.makedirs(baseOutputPath, exist_ok=True)
    _logger.info('Salvando modelo FAISS...')
    faiss.write_index(index, baseOutputPath + "faiss_index.bin")

    news_index = {news_data.iloc[i]["page"]: i for i in range(len(news_data))}

    news_name = {news_data.iloc[i]["page"]: news_data.iloc[i]["url"] for i in range(len(news_data))}

    _logger.info('Salvando dados do modelo...')
    # Criar um dicionário com o índice FAISS e o vetor TF-IDF
    model_data = {
        "faiss_index": "faiss_index.bin",
        "vectorizer": vectorizer,  # TfidfVectorizer treinado
        "news_index": news_index,  # Dicionário {news_id: índice}
        "tfidf_reduced_faiss": tfidf_reduced,
        "news_name": news_name
    }
    with open(baseOutputPath+"model_data.pkl", "wb") as f:
        pickle.dump(model_data, f)