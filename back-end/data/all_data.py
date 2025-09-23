import pandas as pd
import json

json_path = "dados_completos_rotas.json"
output_path = "dados_completos_rotas.csv"

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(len(data))
    print(data[0]["codigo"])
    print(data[0]["rotas"][0]["destino"])

    # df = pd.DataFrame(data)

    # # df.to_csv(output_path, index=False, encoding='utf-8')

    # print(f"Conversão feita!")
    # print(df)

except FileNotFoundError:
    print(f"Erro, ficheiro não encontrado")
except Exception as e:
    print(f"Ocorreu um erro: {e}")