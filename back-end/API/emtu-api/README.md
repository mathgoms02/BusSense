# emtu-api

Back-end da aplicação EMTU Acessível

## 1 - Clonando o repositório

```
https://github.com/UnifespCodeLab/emtu-api.git
```

## 2 - Requisitos

### 2.1 - Obrigatórios

- [yarn](https://yarnpkg.com/)
- [git](https://git-scm.com/)

### 2.2 - Opcionais

- [docker](https://www.docker.com/)
- [docker-compose](https://docs.docker.com/compose/)
- [postgres](https://www.postgresql.org/) (caso não for usar o docker)

## 3 - Setup

### 3.1 - Ambiente

- Crie um novo arquivo `.env`
- Copie o conteúdo do arquivo `.env.sample` para o `.env`

### 3.2 - Subindo o banco de dados

#### 3.2.1 - Com docker

- Abra o terminal na pasta do projeto e execute os seguintes comandos :

  - `docker compose up postgres`

#### 3.2.2 - Sem docker

- instale o postgres13 em sua máquina e crie um banco com nome `postgres` e senha `1234`

### 3.3 - Instalando dependências

- Abra outro terminal e execute:

  - `yarn install`

- <b>Atenção</b>: No momento que estou escrevendo essa doc o yarn está nessa versão: `1.22.19` e o node `19.8.1`

## 4 - Executando o projeto

- Em um terminal aberto na pasta do projeto execute:
  - `yarn run dev`
- Após o console deve imprimir na tela a seguinte mensagem:
  - `server is running on port 3333`
- Para acessar um rota de testes é possível acessar:
  - `http://localhost:3333/api-docs/`

## 5 - Sobre o fluxo de desenvolvimento

- (opcional) Dê uma olhada em como funcionam os [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)
- Vá até o board do github e encontre o [_emtu-api_](https://github.com/orgs/UnifespCodeLab/projects/5/views/1)
- Encontre a issue desejada
- Atribua a si mesmo
- Mude para a coluna _In Progress_
- Com o projeto já clonado em sua pasta desejada, crie uma branch baseada no que está fazendo. Por exemplo:
  - `git checkout -b issue-10`
- Uma boa prática é sempre deixar seus commits o mais '_atômicos_' possível
- Quando todo o desenvolvimento estiver finalizado abra um [pull request](https://github.com/UnifespCodeLab/emtu-api/compare). Lembrando precisa ser nesse sentido: `base: main` <- `compare: issue-10`
- Marque os revisores para que os mesmos recebam notificação e revisem o seu pr
- Vincule a issue aberta com o seu pr
- Corra pro abraço

## Docker

### 1 - Executando seed migration

dentro da pasta do codelab-loader, execute:

```bash
docker compose up emtu-db
```

em outro terminal execute:

```bash
docker compose exec emtu-db bash
cd /emtu/prisma
/bin/bash seed.sh
```

## Atenção

Ao executar duas vezes, a seed irá duplicar os dados e assim por diante
Caso precise, entre no container da api e restaure o banco utilizando o prisma: `ynpx prisma migrate reset`
