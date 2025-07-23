import pandas as pd
import os

class FeedbackAgent:
    """ Registrar o feedback do usuário nos logs """
    def __init__(self, log_file_path: str = 'logs/user_interactions.csv'):
        self.log_file_path = log_file_path
        if not os.path.exists(self.log_file_path):
            raise FileNotFoundError(
                f"Arquivo de log não encontrado em {self.log_file_path}."
            )


    def add_feedback(self, interaction_id: str, feedback_text: str) -> bool:
        try:
            logs_df = pd.read_csv(self.log_file_path, dtype={'interaction_id': str})

            if interaction_id not in logs_df['interaction_id'].values:
                print(f"ID de interação {interaction_id} não encontrado nos logs.")
                return False

            logs_df.loc[logs_df['interaction_id'] == interaction_id, 'user_feedback'] = feedback_text

            logs_df.to_csv(self.log_file_path, index=False, encoding='utf-8')

            print(f"Feedback '{feedback_text}' adicionado com sucesso para a interação {interaction_id}.")
            return True
        except Exception as e:
            print(f"Erro ao adicionar feedback: {e}")
            return False