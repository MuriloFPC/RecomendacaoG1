import os
import pickle

import pandas as pd

from src.Utils.log import Log
import faiss
from src.Api.models import RecomentationRequest, NewsRecommended
from src.Utils.train import read_all_csv_files_in_folder
from src.Utils.variables import GetVariable, script_dir

baseOutputPath = os.path.join(script_dir,GetVariable('ModelOutputPath'))
#load model
with open(baseOutputPath + "FAISS/model_data.pkl", "rb") as f:
    model_data_faiss = pickle.load(f)

index = faiss.read_index(os.path.join(script_dir,GetVariable('ModelOutputPath'),"FAISS",model_data_faiss["faiss_index"]))
vectorizer = model_data_faiss["vectorizer"]
news_index = model_data_faiss["news_index"]
tfidf_reduced_faiss = model_data_faiss["tfidf_reduced_faiss"]
news_name = model_data_faiss["news_name"]

with open(baseOutputPath + "MAB/model_data.pkl", "rb") as f:
    model_data_mab = pickle.load(f)

with open(baseOutputPath + "MAB/" + model_data_mab["mab_model"], "rb") as f:
    mab_model = pickle.load(f)

mapping_index = model_data_mab["mapping_index"]

logs = Log(False)

df_users = read_all_csv_files_in_folder(os.path.join(script_dir,GetVariable('UserNewsPath')))
df_news = read_all_csv_files_in_folder(os.path.join(script_dir,GetVariable('NewsPath')))

# Explodir a coluna 'history' para ter uma linha por news_id
df_users_exploded = df_users.assign(history=df_users['history'].str.split(', ')).explode('history')

df_joined = pd.merge(
    df_users_exploded,
    df_news,
    left_on='history',
    right_on='page',
    how='left'
)

def GetLastedNews(qt_recomedation:int) -> list[NewsRecommended]:
    logs.info("Recuperando as últimas notícias")
    logs.info("Notícias recuperadas com sucesso")
    return [NewsRecommended( Id="IdNews1",Url="Nova Noticia 1",RecomentadionSource="UltimasNoticias"), NewsRecommended(Id="IdNews2",Url="Nova Noticia 2",RecomentadionSource="UltimasNoticias")]

def GetPredictionByFaiss(request: RecomentationRequest, qt_recommendation: int) -> list[NewsRecommended]:
    if not request.newsId:
        logs.info("Nenhuma notícia informada")
        return {}

    # Verificar se a notícia existe no índice
    read_index = news_index.get(request.newsId)
    if read_index is None:
        logs.error(f"Notícia não encontrada. NewsID: {request.newsId}")
        return {}

    # Pegar o vetor da notícia
    read_vector = tfidf_reduced_faiss[read_index].reshape(1, -1)

    # Buscar as notícias mais similares no FAISS
    distances, indices = index.search(read_vector, qt_recommendation + 2)

    # Criar dicionário de recomendações {news_id: score}
    recommendations = {list(news_index.keys())[i]: news_name[list(news_index.keys())[i]] for _, i in enumerate(indices[0])}

    recommendations.pop(request.newsId, None)

    recommendations = dict(list(recommendations.items())[:2])
    recommendationsFinal = [NewsRecommended(Id=k, Url=v, RecomentadionSource="FAISS") for k, v in recommendations.items()]

    logs.info(f"Recomendações geradas para {request.newsId}: {recommendations}")

    return recommendationsFinal if recommendationsFinal else {}

def GetPredictionByMab(request: RecomentationRequest, qt_recommendation: int) -> list[NewsRecommended]:
    user_exists = df_users['userId'].eq(request.userId).any()

    if not user_exists:
        print(f"Usuário com ID {request.userId} não encontrado.")
        return

    user_history_str = df_users[df_users['userId'] == request.userId]['history'].iloc[0]
    history_ids = user_history_str.split(', ')
    user_data = df_joined[df_joined['userId'] == request.userId]

    if not user_data.empty:
        history_titles = user_data['title'].tolist()
    else:
        news_id_to_title = df_news.set_index('page')['title'].to_dict()
        history_titles = [news_id_to_title.get(news_id, "Título não encontrado")
                          for news_id in history_ids]

    news_id_to_title = df_news.set_index('page')['title'].to_dict()

    user_indices = [mapping_index.get(news_id, -1) for news_id in history_ids]

    available_arms = [
        idx for idx in mapping_index.values()
        if idx not in user_indices and idx != -1
    ]

    recommended_arms = sorted(
        available_arms,
        key=lambda x: mab_model.values[x],
        reverse=True
    )[:qt_recommendation]

    inverse_mapping = {v: k for k, v in mapping_index.items()}
    recommended_news_ids = [inverse_mapping[idx] for idx in recommended_arms]

    recommended_titles = [news_id_to_title.get(news_id, "Título não encontrado")
                          for news_id in recommended_news_ids]

    return [NewsRecommended(Id=k, Url=v, RecomentadionSource="MAB") for k, v in zip(recommended_news_ids, recommended_titles)]

