# BusSense AI - Ramo sandbox-ai

Este projeto é um Trabalho de Conclusão de Curso (TCC) de nome **BusSense**, um assistente virtual desenvolvido com foco na **acessibilidade de pessoas cegas** no transporte público. Utiliza tecnologias de **Machine Learning**, **NLP** e **LLMs locais** para fornecer informações sobre horários de ônibus, rotas, atrasos e sugestões personalizadas com base no histórico do usuário.

## \:brain: Sobre este módulo (`main_assistant.py`)

Este script é o coração do modelo de assistente virtual, responsável por:

* Carregar a base de conhecimento (embeddings) com informações dos ônibus.
* Inicializar o modelo de linguagem local (via HuggingFace ou LLMs como o LLaMA).
* Processar a entrada do usuário (prompt) e retornar uma resposta natural com base nas rotas disponíveis.

## \:rocket: Tecnologias utilizadas

* Python 3.10+
* [Transformers (HuggingFace)](https://huggingface.co/ggml-org/gemma-3-1b-it-GGUF)
* [llama.cpp](https://github.com/ggml-org/llama.cpp) (para execução local de modelos LLaMA via CPU ou GPU)

## \:file\_folder: Estrutura de pastas relevante

```
BusSense/
├── back-end/
│   ├── model/
│   │   ├── main_assistant.py       # Script principal do assistente virtual
│   ├── utils/
│   │   ├── route_embeddings.py     # Armazena os embeddings vetorizados
│   └── ...
```

## \:gear: Como usar

1. Clone o repositório:

```bash
git clone https://github.com/mathgoms02/BusSense.git
cd BusSense/back-end/
```

2. Prepare o Ambiente (venv)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Configure o modelo LLaMA local com `llama.cpp`:

   * Acesse o repositório oficial: [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp)
   * Siga as instruções de instalação para compilar o projeto e baixar um modelo compatível.
   * Use a API local ou integre diretamente via bindings Python (como `llama-cpp-python`) conforme seu ambiente.

4. Execute o script principal:

```bash
python -m main.py
```

## \:bulb: Objetivos futuros

* Melhorar resultados do modelo.
* Aprendizado contínuo com base na experiência do usuário.
* Previsão de atrasos com base em dados históricos.
* Sugestões de rotas personalizadas.

## \:scroll: Créditos

Este projeto utiliza a implementação da Meta AI para execução local de LLMs via o projeto [llama.cpp](https://github.com/ggml-org/llama.cpp), desenvolvido por [@ggerganov](https://github.com/ggerganov) e comunidade. Recomendamos fortemente visitar o repositório oficial para entender melhor seu funcionamento e potencial.
