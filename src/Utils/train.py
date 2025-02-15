import os
import pandas as pd

def read_all_csv_files_in_folder(folder_path):
    # List to hold DataFrames
    dataframes = []

    # Iterate over all files in the folder
    for file in os.listdir(folder_path):
        if file.endswith('.csv'):
            file_path = os.path.join(folder_path, file)
            # Read the CSV file and append the DataFrame to the list
            df = pd.read_csv(file_path)
            dataframes.append(df)

    # Concatenate all DataFrames into a single DataFrame
    combined_df = pd.concat(dataframes, ignore_index=True)
    return combined_df

def import_data(file_path, file_names):

    # Constrói os caminhos completos
    file_paths = [os.path.join(file_path, f) for f in file_names]

    # Verifica se os arquivos existem
    for fp in file_paths:
        if not os.path.exists(fp):
            raise FileNotFoundError(f"Arquivo não encontrado: {fp}")

    dataframes = []
    header = None  # Inicializa a variável header

    # Itera sobre os caminhos completos (file_paths), não sobre file_names
    for i, fp in enumerate(file_paths):
        if i == 0:
            # Lê o primeiro arquivo com header
            df = pd.read_csv(fp)
            header = df.columns
        else:
            # Lê arquivos subsequentes ignorando o header original e usando o header do primeiro
            df = pd.read_csv(
                fp,
                skiprows=1,
                header=None,
                names=header,
                low_memory=False
            )
        dataframes.append(df)

    # Concatena e limpa os dados
    df_concat = pd.concat(dataframes, ignore_index=True)
    df = df_concat.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    if ('history' in df.columns):
        df = df.dropna(subset=['history', 'numberOfClicksHistory'])
        df = df[df['history'].str.strip() != '']
        df = df[df['numberOfClicksHistory'].str.strip() != '']

    return df
