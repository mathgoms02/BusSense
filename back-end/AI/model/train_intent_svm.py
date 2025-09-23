# train_intent_svm.py  (execute: python train_intent_svm.py)
# (1) Imports básicos
import pandas as pd                   # (2) Lidar com CSV
from sklearn.model_selection import train_test_split  # (3) Separar treino/teste
from sklearn.feature_extraction.text import TfidfVectorizer  # (4) Transformar texto em números
from sklearn.svm import LinearSVC     # (5) Classificador SVM linear
from sklearn.pipeline import Pipeline # (6) Facilita encadear etapas
from sklearn.metrics import classification_report, confusion_matrix  # (7) Métricas
from sklearn.calibration import CalibratedClassifierCV  # (8) Para ter "probabilidades"
import joblib                         # (9) Salvar o modelo em disco
import os                             # (10) Utilidades de arquivo

# (11) Caminhos dos arquivos
DATA_CSV = "intent_dataset.csv"
MODEL_PATH = "intent_svm.pkl"

# (12) Carrega e limpa os dados
def load_data():
    df = pd.read_csv(DATA_CSV)                    # (13) Lê o CSV
    df = df.dropna(subset=["user_text","intent"]) # (14) Remove linhas vazias
    # (15) Mantém só as quatro classes de interesse
    allowed = {"solicitar_rota","feedback","conversacao_geral","desconhecido"}
    df = df[df["intent"].isin(allowed)]
    return df

# (16) Define o pipeline TF-IDF + SVM
def build_pipeline():
    pipe = Pipeline([
        # (17) TF-IDF de n-gramas de caracteres: robusto a erros de digitação/ASR
        ("tfidf", TfidfVectorizer(analyzer="char", ngram_range=(3,5), min_df=2, lowercase=True)),
        # (18) SVM linear com balanceamento para classes desbalanceadas
        ("svm", LinearSVC(class_weight="balanced", C=1.0))
    ])
    return pipe

def main():
    # (19) Carrega dados
    df = load_data()
    X = df["user_text"]               # (20) Textos
    y = df["intent"]                  # (21) Rótulos

    # (22) Divide em treino/teste (80/20) mantendo proporções das classes
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # (23) Cria e treina o pipeline
    pipe = build_pipeline()
    pipe.fit(X_tr, y_tr)

    # (24) Avalia no conjunto de teste
    y_pred = pipe.predict(X_te)
    print(classification_report(y_te, y_pred))
    print("Matriz de confusão:\\n", confusion_matrix(y_te, y_pred))

    # (25) Calibra o SVM para obter "probabilidades" e permitir threshold
    #      Observação: calibramos APENAS o estimador SVM usando as features do TF-IDF já treinado.
    tfidf = pipe.named_steps["tfidf"]
    svm = pipe.named_steps["svm"]
    calibrated = CalibratedClassifierCV(estimator=svm, method="sigmoid", cv=3)
    X_tr_vec = tfidf.transform(X_tr)
    calibrated.fit(X_tr_vec, y_tr)

    # (26) Salva em disco: TF-IDF + classificador calibrado + lista de classes
    bundle = {"tfidf": tfidf, "calibrated": calibrated, "labels": sorted(y.unique())}
    joblib.dump(bundle, MODEL_PATH)
    print("Modelo salvo em:", MODEL_PATH)

if __name__ == "__main__":
    main()