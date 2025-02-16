import os
import pickle

import numpy as np

from src.Utils.train import read_all_csv_files_in_folder
from src.Utils.variables import GetVariable, script_dir


class MultiArmedBandit:
    def __init__(self, n_arms):
        """
        Inicializa o MAB com um número fixo de braços (notícias).

        :param n_arms: Número de notícias (braços) disponíveis.
        """
        self.n_arms = n_arms
        self.counts = np.zeros(n_arms)  # Número de vezes que cada braço foi escolhido
        self.values = np.zeros(n_arms)  # Recompensa média estimada para cada braço

    def select_arm(self, exploration_rate=0.1):
        if np.random.rand() < exploration_rate:
            return np.random.choice(self.n_arms)
        total_counts = np.sum(self.counts)
        if total_counts == 0:
            return np.random.choice(self.n_arms)
        ucb_values = self.values + np.sqrt(2 * np.log(total_counts) / (self.counts + 1e-5))
        return np.argmax(ucb_values)

    def update(self, chosen_arm, reward):
        """
        Atualiza a recompensa média e o contador para o braço escolhido.

        :param chosen_arm: Índice do braço escolhido.
        :param reward: Recompensa observada (ex: número de cliques).
        """
        self.counts[chosen_arm] += 1
        n = self.counts[chosen_arm]
        value = self.values[chosen_arm]
        new_value = ((n - 1) / n) * value + (1 / n) * reward
        self.values[chosen_arm] = new_value



def create_mapping(df_users,_logger):
    _logger.info('Criando mapeamento de índices das notícias...')
    all_news_ids = set()

    for history_str in df_users['history']:
        news_ids = history_str.split(', ')
        all_news_ids.update(news_ids)

    mapping_index = {news_id: idx for idx, news_id in enumerate(all_news_ids)}

    return mapping_index


def train_mab_model(df_users, mapping_index,_logger):
    _logger.info('Inicializando e treinando o modelo MAB...')

    n_arms = len(mapping_index)
    mab = MultiArmedBandit(n_arms=n_arms)

    for _, row in df_users.iterrows():
        news_ids = row['history'].split(', ')
        clicks = row['numberOfClicksHistory'].split(', ')

        if len(news_ids) != len(clicks):
            _logger.warning(f"Tamanho de history e clicks diferente para o usuário {row['userId']}. Pulando linha.")
            continue

        try:
            clicks = list(map(int, clicks))
        except ValueError as e:
            _logger.error(f"Erro ao converter clicks: {e}. Pulando linha.")
            continue

        for news_id, click_count in zip(news_ids, clicks):
            arm_index = mapping_index.get(news_id)
            if arm_index is None:
                _logger.warning(f"News ID {news_id} não encontrado no mapeamento. Pulando.")
                continue
            mab.update(arm_index, reward=click_count)

    return mab

def TrainModelMAB(_logger):
    _logger.info('Iniciando treinamento do modelo MAB...')
    df_users = read_all_csv_files_in_folder(os.path.join(script_dir,GetVariable('UserNewsPath')))

    mapping_index = create_mapping(df_users,_logger)
    mab = train_mab_model(df_users, mapping_index,_logger)
    baseOutputPath = os.path.join(script_dir,GetVariable('ModelOutputPath'),'MAB/')
    os.makedirs(baseOutputPath, exist_ok=True)
    _logger.info('Salvando modelo MAB...')
    with open(baseOutputPath + 'mab.pkl', 'wb') as f:
        pickle.dump(mab, f)
    _logger.info('Modelo MAB treinado e salvo com sucesso.')

    model_data = {
        "mab_model": "mab.pkl",
        "mapping_index": mapping_index
    }
    _logger.info('Salvando dados do modelo...')
    with open(baseOutputPath+"model_data.pkl", "wb") as f:
        pickle.dump(model_data, f)