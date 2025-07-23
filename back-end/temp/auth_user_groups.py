from pymongo import MongoClient
import pandas as pd
from sqlalchemy import create_engine

# 1. Conecta no PostgreSQL
engine = create_engine("postgresql://postgres:1234@127.0.0.1:5432/emtu")

variable = "auth_user_groups"

# 2. Conecta no MongoDB
mongo_client = MongoClient("mongodb://127.0.0.1:27017/")
mongo_db = mongo_client["emtu_db"]
mongo_collection = mongo_db[variable]

# 3. Consulta os dados
df = pd.read_sql_query(f"SELECT * FROM {variable}", engine)

# Mostra os primeiros registros para debug
print(df.head())
print(f"Total de registros encontrados: {len(df)}")

# 4. Converte e insere se houver registros
records = df.to_dict(orient="records")

if records:
    mongo_collection.insert_many(records)
    print(f"Migrado {len(records)} registros com sucesso!")
else:
    print(f"⚠️ Nenhum registro encontrado na tabela '{variable}'.")
