# intent_svm.py  (uso em produção)
# (1) Carrega o pacote salvo e faz predição com confiança
import joblib                  # (2) Para carregar o arquivo .pkl
import numpy as np             # (3) Operações numéricas

class IntentSVM:
    def __init__(self, model_path="intent_svm.pkl", threshold=0.55):
        # (4) Lê o pacote salvo (tfidf + calibrado + labels)
        self.bundle = joblib.load(model_path)
        self.tfidf = self.bundle["tfidf"]
        self.clf = self.bundle["calibrated"]
        self.labels = self.bundle["labels"]
        self.threshold = threshold

    def predict(self, text: str):
        # (5) Transforma o texto em vetor TF-IDF
        X = self.tfidf.transform([text])
        # (6) Obtém probabilidades (calibradas) por classe
        probs = self.clf.predict_proba(X)[0]
        # (7) Pega a classe de maior probabilidade e o valor de confiança
        idx = int(np.argmax(probs))
        pred = self.clf.classes_[idx]
        conf = float(probs[idx])
        return pred, conf