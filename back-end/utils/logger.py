import pandas as pd
import os
from datetime import datetime
import uuid
from config import constants

class InteractionLogger:
    """ Gerencia o registro de interações do usuário em um arquivo CSV. """
    def __init__(self, log_file_path: str = constants.LOG_FILE_PATH + 'user_interactions.csv'):
        """
        Inicializa o logger e cria o arquivo de log com cabeçalho, se não existir.

        Args:
            log_file_path (str): Caminho para o arquivo CSV de logs.
        """
        self.log_file_path = log_file_path
        self.log_columns = [
            'timestamp', 'interaction_id', 'user_query', 'extracted_origin',
            'extracted_destination', 'suggested_route_code', 'suggestion_confidence',
            'assistant_response', 'user_feedback'
        ]

        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

        if not os.path.exists(self.log_file_path):
            pd.DataFrame(columns=self.log_columns).to_csv(self.log_file_path, index=False, encoding='utf-8')

    def log(self, interaction_data: dict):
        """
        Registra uma interação do usuário no arquivo CSV.

        Args:
            interaction_data (dict): Dados da interação a serem registrados.
        """

        for col in self.log_columns:
            interaction_data.setdefault(col, None)

        # Gerando ID para o modelo se localizar
        interaction_id = str(uuid.uuid4())
        interaction_data['interaction_id'] = interaction_id

        interaction_data.setdefault('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        # interaction_data.setdefault('interaction_id', str(uuid.uuid4()))

        new_log_df = pd.DataFrame([interaction_data], columns=self.log_columns)
        new_log_df.to_csv(self.log_file_path, mode='a', header=False, index=False, encoding='utf-8')

        print(f"Interaçaõ registrada com sucesso em {self.log_file_path}")

        return interaction_id