import pandas as pd
import time
import json
import re
import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

# Importe os componentes necessários do seu projeto
# from model.client import LlamaClient
from model.main_assistant import BusSenseAssistant
from config import constants
from model.intent_svm import IntentSVM  # importa o classificador SVM


class ModelEvaluator:
    """
    Classe para avaliar o desempenho do modelo de IA do BusSense.
    Testa classificação de intenção, extração de entidade e latência,
    e salva os resultados em arquivos.
    """
    def __init__(self, test_data_path: str):
        """
        Inicializa o avaliador.

        Args:
            test_data_path (str): Caminho para o arquivo CSV com os dados de teste.
        """
        print("Iniciando a avaliação do modelo...")
        try:
            self.test_df = pd.read_csv(test_data_path)
            print(f"Dados de teste carregados com sucesso de '{test_data_path}'. Total de {len(self.test_df)} casos de teste.")
        except FileNotFoundError:
            print(f"ERRO: O arquivo de dados de teste '{test_data_path}' não foi encontrado.")
            exit()

        self.assistant = BusSenseAssistant(routes_data_path=constants.DATA_FILE_PATH + 'llm_generated_routes.csv')
        self.latencies = []
        self.results_log = []

        self.intent_svm = IntentSVM(model_path="/home/matheusg/Documents/UNASP/BusSense/back-end/model/intent_svm.pkl", threshold=0.55)
        # self.intent_svm = IntentSVM(model_path="/home/matheusg/Documents/UNASP/BusSense/back-end/model/intent_svm.pkl", threshold=0.90)


    def _run_single_prediction(self, method_to_call, text):
        """ Roda uma única predição e mede sua latência. """
        start_time = time.time()
        result = method_to_call(text)
        end_time = time.time()
        self.latencies.append(end_time - start_time)
        return result

    def evaluate_intent_classification(self):
        """
        Avalia a acurácia da classificação de intenção usando SVM + fallback LLM.
        """
        print("\n--- Iniciando Avaliação: Classificação de Intenção (SVM + LLM) ---")
        intent_df = self.test_df[['text', 'expected_intent']].dropna()

        y_true = intent_df['expected_intent'].tolist()
        y_pred = []

        for index, row in intent_df.iterrows():
            text = row['text']
            true_intent = row['expected_intent']

            # --- (1) PREDIÇÃO VIA SVM ---
            svm_intent, conf = self.intent_svm.predict(text)

            if conf < self.intent_svm.threshold:
                # --- (2) FALLBACK PRO LLM ---
                predicted_intent_raw = self._run_single_prediction(self.assistant._classify_intent_with_llm, text)
                predicted_intent = predicted_intent_raw.strip().lower().replace("'", "").replace('"', '').replace("''", '').replace('.', '')
                source = "llm"
            else:
                predicted_intent = svm_intent.lower()
                source = "svm"

            y_pred.append(predicted_intent)

            # Log detalhado
            self.results_log.append({
                'test_case': text,
                'task': 'intent_classification',
                'expected': true_intent,
                'predicted': predicted_intent,
                'confidence': conf,
                'source': source,
                'is_correct': true_intent == predicted_intent
            })

        self.intent_accuracy = accuracy_score(y_true, y_pred)
        self.intent_report = classification_report(y_true, y_pred, zero_division=0, output_dict=False)

        print(f"\nAcurácia Geral da Classificação de Intenção: {self.intent_accuracy:.2%}")
        print("\nRelatório de Classificação:")
        print(self.intent_report)

        # Matriz de Confusão
        labels = sorted(list(set(y_true)))
        cm = confusion_matrix(y_true, y_pred, labels=labels)
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
        plt.title('Matriz de Confusão - Classificação de Intenção (SVM+LLM)')
        plt.xlabel('Intenção Prevista')
        plt.ylabel('Intenção Real')
        plt.xticks(rotation=30, ha='right')
        plt.tight_layout(pad=2.0)
        plt.savefig('intent_confusion_matrix_svm_llm.png')
        print("Matriz de confusão salva em 'intent_confusion_matrix_svm_llm.png'")

    def evaluate_entity_extraction(self):
        """
        Avalia a precisão da extração de entidades (origem e destino).
        """
        print("\n--- Iniciando Avaliação: Extração de Entidades ---")
        entity_df = self.test_df[self.test_df['expected_intent'] == 'solicitar_rota'].copy()
        # Corrigido para não dropar linhas se apenas uma das colunas for nula
        entity_df = entity_df[['text', 'expected_origin', 'expected_destination']]

        if entity_df.empty:
            print("Nenhum caso de teste encontrado para extração de entidades.")
            self.origin_accuracy = 0
            self.destination_accuracy = 0
            return

        correct_origins = 0
        correct_destinations = 0
        total_entity_tests = 0

        for index, row in entity_df.iterrows():
            # Pula linhas onde não há o que testar
            if pd.isna(row['expected_origin']) and pd.isna(row['expected_destination']):
                continue

            total_entity_tests += 1
            text = row['text']
            expected_origin = str(row['expected_origin'])
            expected_destination = str(row['expected_destination'])

            extracted_locations = self._run_single_prediction(self.assistant._extract_location_from_text, row['text'])
            predicted_origin = str(extracted_locations.get('origin', ''))
            predicted_destination = str(extracted_locations.get('destination', ''))

            origin_correct = expected_origin.lower() == predicted_origin.lower()
            destination_correct = expected_destination.lower() == predicted_destination.lower()

            if origin_correct: correct_origins += 1
            if destination_correct: correct_destinations += 1

            # Log detalhado
            self.results_log.append({
                'test_case': text,
                'task': 'entity_extraction_origin',
                'expected': expected_origin,
                'predicted': predicted_origin,
                'is_correct': origin_correct
            })
            self.results_log.append({
                'test_case': text,
                'task': 'entity_extraction_destination',
                'expected': expected_destination,
                'predicted': predicted_destination,
                'is_correct': destination_correct
            })

        self.origin_accuracy = correct_origins / total_entity_tests if total_entity_tests > 0 else 0
        self.destination_accuracy = correct_destinations / total_entity_tests if total_entity_tests > 0 else 0

        print(f"\nAcurácia da Extração de 'Origem': {self.origin_accuracy:.2%}")
        print(f"Acurácia da Extração de 'Destino': {self.destination_accuracy:.2%}")

    def calculate_latency_stats(self):
        """ Calcula as estatísticas de latência. """
        if not self.latencies:
            self.latency_stats = "Nenhuma chamada ao LLM foi registrada."
            return

        self.latency_stats = (
            f"Total de chamadas ao LLM: {len(self.latencies)}\n"
            f"Latência Média: {np.mean(self.latencies):.4f} segundos\n"
            f"Latência Máxima (pior caso): {np.max(self.latencies):.4f} segundos\n"
            f"Latência Mínima (melhor caso): {np.min(self.latencies):.4f} segundos"
        )
        print("\n--- Métricas de Latência ---")
        print(self.latency_stats)

    def save_results_to_files(self):
        """
        Salva o resumo e os detalhes da avaliação em arquivos .txt e .csv.
        """
        print("\n--- Salvando Resultados ---")

        # 1. Salvar o resumo em .txt
        summary_filename = "evaluation_summary.txt"
        with open(summary_filename, "w", encoding="utf-8") as f:
            f.write("="*50 + "\n")
            f.write(f"Relatório de Avaliação do Modelo BusSense\n")
            f.write(f"Data da Avaliação: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*50 + "\n\n")

            f.write("1. Desempenho da Classificação de Intenção\n")
            f.write("-" * 40 + "\n")
            f.write(f"Acurácia Geral: {self.intent_accuracy:.2%}\n\n")
            f.write("Relatório de Classificação:\n")
            f.write(self.intent_report)
            f.write("\n\n")

            f.write("2. Desempenho da Extração de Entidades\n")
            f.write("-" * 40 + "\n")
            f.write(f"Acurácia da Extração de 'Origem': {self.origin_accuracy:.2%}\n")
            f.write(f"Acurácia da Extração de 'Destino': {self.destination_accuracy:.2%}\n\n")

            f.write("3. Métricas de Latência\n")
            f.write("-" * 40 + "\n")
            f.write(self.latency_stats + "\n")

        print(f"Relatório de resumo salvo em '{summary_filename}'")

        # 2. Salvar os detalhes em .csv
        details_filename = "evaluation_details.csv"
        results_df = pd.DataFrame(self.results_log)
        results_df.to_csv(details_filename, index=False, encoding='utf-8-sig')
        print(f"Resultados detalhados salvos em '{details_filename}'")


    def run_full_evaluation(self):
        """
        Roda todos os testes de avaliação e salva os resultados.
        """
        self.evaluate_intent_classification()
        self.evaluate_entity_extraction()
        self.calculate_latency_stats()
        self.save_results_to_files() # Novo passo
        print("\n--- Avaliação Concluída ---")


if __name__ == "__main__":
    TEST_DATASET_PATH = 'model_test_data.csv'

    evaluator = ModelEvaluator(test_data_path=TEST_DATASET_PATH)
    evaluator.run_full_evaluation()
