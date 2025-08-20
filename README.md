# BusSense - API Inteligente para Transporte Público

Este é o repositório do back-end do **BusSense**, um Trabalho de Conclusão de Curso (TCC) focado em criar um assistente inteligente para o transporte público, com foco especial na **acessibilidade para pessoas com deficiência visual**.

A API, desenvolvida com Django e MongoDB, serve como a base para todas as operações, desde o cadastro de usuários e rotas até a futura integração com módulos de Inteligência Artificial para alertas e análises em tempo real.

## 🚀 Tecnologias Utilizadas

  * **Back-end:** Python, Django, Django REST Framework
  * **Banco de Dados:** MongoDB
  * **ODM (Object-Document Mapper):** MongoEngine
  * **Inteligência Artificial (Futuro):** Transformers (HuggingFace), LLMs Locais

## 📋 Pré-requisitos

Antes de começar, garanta que você tenha as seguintes ferramentas instaladas em seu sistema:

1.  **Python 3.10+**
2.  **Git**
3.  **MongoDB Community Server**
4.  **MongoDB Compass (GUI Opcional, mas recomendado)**

-----

### Guia de Instalação dos Pré-requisitos

#### 1\. MongoDB Community Server

O MongoDB é o banco de dados NoSQL que utilizamos.

  * **Windows:**

    1.  Acesse a [página de download do MongoDB Community Server](https://www.mongodb.com/try/download/community).
    2.  Baixe o instalador `.msi` e siga as instruções do assistente de instalação. É recomendado instalar como um serviço de sistema para que ele inicie junto com o Windows.

  * **Linux (Exemplo para Ubuntu/Debian):**

    1.  Siga o [guia de instalação oficial para sua distribuição](https://www.mongodb.com/docs/manual/administration/install-on-linux/). Geralmente, envolve adicionar o repositório do MongoDB e instalar via `apt`.

    <!-- end list -->

    ```bash
    sudo apt-get install -y mongodb-org
    ```

    2.  Inicie e habilite o serviço do MongoDB:

    <!-- end list -->

    ```bash
    sudo systemctl start mongod
    sudo systemctl enable mongod
    ```

#### 2\. MongoDB Compass (Interface Gráfica)

O Compass é uma ferramenta visual para interagir com seu banco de dados.

  * **Windows:** Geralmente, a opção de instalar o Compass é oferecida durante a instalação do MongoDB Server.
  * **Linux e Windows (Standalone):**
    1.  Acesse a [página de download do MongoDB Compass](https://www.mongodb.com/try/download/compass).
    2.  Baixe e execute o instalador para o seu sistema operacional.

-----

## ⚙️ Configuração do Projeto

Siga os passos abaixo para configurar e rodar o ambiente de desenvolvimento local.

#### 1\. Clone o Repositório

```bash
git clone https://github.com/mathgoms02/BusSense.git
cd BusSense/back-end/
```

#### 2\. Crie e Ative o Ambiente Virtual (venv)

É crucial usar um ambiente virtual para isolar as dependências do projeto.

  * **Linux / macOS:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

  * **Windows:**

    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

#### 3\. Instale as Dependências Python

Com o ambiente virtual ativado, instale todos os pacotes necessários.

```bash
pip install -r requirements.txt
```

#### 4\. Importe os Dados do Banco (Primeira Vez)

O projeto precisa dos dados das rotas e usuários para funcionar. Nós utilizamos as ferramentas `mongodump` e `mongorestore` para isso.

Primeiro, garanta que o serviço do MongoDB esteja rodando. Depois, execute o comando abaixo no seu terminal, na pasta `back-end/`.

```bash
mongorestore --db emtu_db dump/emtu_db
```

*Este comando irá criar um banco de dados chamado `emtu_db` e importar todas as coleções contidas na pasta `dump/`.*

#### 5\. Rode a Aplicação

Finalmente, inicie o servidor Django.

```bash
python manage.py runserver
```

A API estará disponível em `http://127.0.0.1:8000/api/` e os formulários de cadastro em `http://127.0.0.1:8000/api/forms/`.

-----

## 📦 Gerenciamento do Banco de Dados

Aqui estão as instruções para exportar (fazer backup) e importar (restaurar) o banco de dados.

### Para Exportar os Dados (Criar um `dump`)

Se você fez alterações no banco de dados local e quer gerar um novo backup para compartilhar, siga estes passos.

1.  Garanta que o serviço do MongoDB esteja rodando.

2.  No terminal, na pasta `back-end/`, execute o comando:

    ```bash
    mongodump --db emtu_db --out dump
    ```

      * `--db emtu_db`: Especifica o nome do banco de dados que você quer exportar.
      * `--out dump`: Especifica que o conteúdo será salvo em uma pasta chamada `dump`.

    Isso irá sobrescrever (ou criar) a pasta `dump` com os dados mais recentes do seu banco `emtu_db`.

### Para Importar os Dados (Restaurar um `dump`)

Este é o mesmo comando usado na configuração inicial. Ele é útil para restaurar o banco de dados a partir de um backup.

1.  Garanta que o serviço do MongoDB esteja rodando.
2.  (Opcional) Se você quer limpar o banco de dados antes de importar, pode deletá-lo usando o MongoDB Compass ou o comando `mongo emtu_db --eval "db.dropDatabase()"`.
3.  No terminal, na pasta `back-end/`, execute o comando:
    ```bash
    mongorestore --db emtu_db dump/emtu_db
    ```