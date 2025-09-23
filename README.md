# 🚍 BusSense – Assistente Inteligente para Transporte Público  

O **BusSense** é um Trabalho de Conclusão de Curso (TCC) que tem como objetivo criar um **assistente virtual inteligente** para o transporte público, com foco especial na **acessibilidade de pessoas com deficiência visual**.  

A solução combina:  
- **Back-end com Django e MongoDB**, responsável por cadastros, rotas e gerenciamento de dados.  
- **Módulo de Inteligência Artificial (IA)**, que utiliza **LLMs locais** e **embeddings vetoriais** para responder perguntas sobre transporte público de forma natural e personalizada.  

---

## 🚀 Tecnologias Utilizadas  

### 🔧 Back-end
- Python 3.10+  
- Django + Django REST Framework  
- MongoDB (NoSQL)  
- MongoEngine (ODM para Python)  

### 🤖 Inteligência Artificial
- [Transformers (HuggingFace)](https://huggingface.co/)  
- [llama.cpp](https://github.com/ggml-org/llama.cpp) (execução local de modelos LLaMA via CPU/GPU)  
- Embeddings vetoriais para rotas de transporte  

---

## 📂 Estrutura de Pastas  

```bash
BusSense/
├── back-end/
│   ├── model/
│   │   ├── main_assistant.py       # Script principal do assistente virtual
│   ├── utils/
│   │   ├── route_embeddings.py     # Armazena e gerencia embeddings vetorizados
│   ├── dump/                       # Backup do banco MongoDB
│   └── ...
```

---

## ⚙️ Configuração do Ambiente  

### 1. Clone o repositório  

```bash
git clone https://github.com/mathgoms02/BusSense.git
cd BusSense/back-end/
```

### 2. Crie e ative o ambiente virtual  

**Linux/macOS**  
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows**  
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instale as dependências  

```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados MongoDB  

Importe o dump inicial:  
```bash
mongorestore --db emtu_db dump/emtu_db
```

### 5. Inicie o servidor Django  

```bash
python manage.py runserver
```

- API: [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/)  
- Formulários: [http://127.0.0.1:8000/api/forms/](http://127.0.0.1:8000/api/forms/)  

---

## 🧠 Executando o Assistente de IA  

1. Configure e compile o **llama.cpp**:  
   - [Repositório oficial](https://github.com/ggml-org/llama.cpp)  
   - Baixe um modelo compatível (ex.: LLaMA ou Gemma).  

2. Execute o script principal:  
```bash
python model/main_assistant.py
```

Esse módulo carrega embeddings de rotas e responde perguntas com base no histórico do usuário.  

---

## 📦 Gerenciamento do Banco de Dados  

### Exportar (Backup)  
```bash
mongodump --db emtu_db --out dump
```

### Importar (Restaurar)  
```bash
mongorestore --db emtu_db dump/emtu_db
```

---

## 🔮 Objetivos Futuros  

- Previsão de atrasos baseada em dados históricos.  
- Sugestões personalizadas de rotas.  
- Aprendizado contínuo com base na experiência do usuário.  
- Integração em tempo real com APIs de transporte público.  

---

## 📜 Créditos  

Este projeto utiliza a implementação da **Meta AI** para execução local de LLMs via [llama.cpp](https://github.com/ggml-org/llama.cpp), desenvolvido por [@ggerganov](https://github.com/ggerganov) e comunidade.  
