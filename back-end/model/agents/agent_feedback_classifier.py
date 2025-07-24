import pandas as pd
import os
from config import constants

class FeedbackClassifierAgent:
    """ ANalisa se o audio é um feedback se esta solicitando uma rota """
    def __init__(self, log_file_path: str = constants.LOG_FILE_PATH + 'user_interactions.csv'):
        self.log_file_path = log_file_path

        if not os.path.exists(self.log_file_path):
            raise FileNotFoundError(
                f"Arquivo de log não encontrado em {self.log_file_path}."
            )


    def process_feedback_text(self, interaction_id: str, feedback_text: str):
        """ processa o feedback de audio para uma interação específica"""
        print("Audio de feedback capturado com sucesso.")

        intent = self._classify_intent(feedback_text)
        self._handle_intent(interaction_id, intent, feedback_text)


    def _classify_intent(self, text: str) -> str:
        """ Versão melhorada do classificador de intenção. """
        text_lower = text.lower()

        # --- Feedbacks Positivos/De Conclusão ---
        if any(keyword in text_lower for keyword in ["certo", "obrigado", "valeu", "beleza", "funcionou", "cheguei", "desci", "estou no ponto", "deu certo"]):
            return "feedback_positivo_concluido"

        # --- Feedbacks de Problema durante a viagem ---
        if any(keyword in text_lower for keyword in ["atrasou", "demorou", "atrasado", "lotado", "cheio"]):
            return "feedback_problema_viagem"

        # --- Feedbacks de Rota Incorreta ---
        if any(keyword in text_lower for keyword in ["errada", "errado", "não era essa", "ruim"]):
            return "feedback_rota_incorreta"

        # --- Detecção de Nova Solicitação (deve vir por último) ---
        if any(keyword in text_lower for keyword in ["quero ir", "como eu chego", "como faço para ir", "preciso ir", "qual ônibus"]):
            return "nova_solicitacao"

        return "feedback_generico"


    def _handle_intent(self, interaction_id: str, intent: str, feedback_text: str):
        """ Atualiza o log com base na intenção classificada """
        try:
            logs_df = pd.read_csv(self.log_file_path, dtype={'interaction_id': str})

            if interaction_id not in logs_df['interaction_id'].values:
                print(f"ID de interação {interaction_id} não encontrado nos logs.")
                return

            if intent == "nova_solicitacao":
                print(f"🔄 Nova solicitação detectada: '{feedback_text}'.")
                # Aqui sinalizamos que uma nova busca deve ser iniciada.
                # O LlamaThinking tratará disso.
            else:
                feedback_final = f"{intent}: {feedback_text}"
                logs_df.loc[logs_df['interaction_id'] == interaction_id, 'user_feedback'] = feedback_final
                logs_df.to_csv(self.log_file_path, index=False, encoding='utf-8')
                print(f"Feedback '{feedback_final}' adicionado com sucesso para a interação {interaction_id}.")
        except Exception as e:
            print(f"Erro ao processar feedback: {e}")