# TaskFlow Kanban 

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

Um organizador de tarefas no estilo Kanban, desenvolvido como um projeto para a disciplina de Programação Orientada a Objetos. O foco principal é a aplicação dos princípios **SOLID** e uma arquitetura de software orientada a objetos limpa em Python.

##  Tabela de Conteúdos

1.  [Sobre o Projeto](#sobre-o-projeto)
2.  [Funcionalidades](#funcionalidades)
3.  [Arquitetura do Software](#arquitetura-do-software)
4.  [Tecnologias Utilizadas](#tecnologias-utilizadas)
5.  [Como Executar](#como-executar)
6.  [Endpoints da API](#api-endpoints)
7.  [Estrutura do Projeto](#estrutura-do-projeto)

---

## Sobre o Projeto

O **TaskFlow** é uma aplicação web de página única (SPA) para gerenciamento de tarefas pessoais usando um painel Kanban com as colunas *To Do*, *Doing* e *Done*.

Este projeto foi desenvolvido como avaliação para a disciplina de **Programação Orientada a Objetos (POO)**. O principal objetivo não era apenas criar uma ferramenta funcional, mas fazê-lo utilizando uma arquitetura robusta, seguindo os 5 princípios **SOLID** e padrões de design como a Injeção de Dependência e o padrão de Camadas (Repository, Service, Controller).

##  Funcionalidades

Até o momento, o projeto implementa o **CRUD** completo para as tarefas, consumindo uma API RESTful própria:

* **[C]reate (Criar):** Adicionar novas tarefas através de um modal.
* **[R]ead (Ler):** Carregar e exibir todas as tarefas existentes no painel ao iniciar a aplicação.
* **[U]pdate (Atualizar):** Atualizar o status de uma tarefa (`todo`, `doing`, `done`) através de uma funcionalidade *drag-and-drop* intuitiva entre as colunas.
* **[D]elete (Excluir):** Excluir tarefas permanentemente do painel e do banco de dados.

## Arquitetura do Software

O backend foi projetado seguindo uma arquitetura limpa de 3 camadas para garantir a **separação de responsabilidades** (Single Responsibility Principle) e a **Inversão de Dependência** (Dependency Inversion Principle).



1.  **Camada de Controladores (`/controllers`)**
    * Responsável por gerenciar as rotas da API (endpoints).
    * Recebe requisições HTTP (JSON) e devolve respostas HTTP.
    * Não contém regras de negócio. Apenas orquestra o fluxo, chamando a camada de serviço.

2.  **Camada de Serviços (`/services`)**
    * Contém toda a lógica e regras de negócio da aplicação.
    * Ex: "Uma nova tarefa deve sempre ser criada com o status 'todo'".
    * Depende da *abstração* do repositório (`BaseRepository`), não da implementação concreta.

3.  **Camada de Repositórios (`/repositories`)**
    * É a única camada que "sabe" como falar com o banco de dados.
    * Implementa uma interface (`BaseRepository`) e lida com toda a lógica de persistência (comandos SQL).
    * Abstrai a fonte de dados (SQLite) do resto da aplicação.

O **`app.py`** (na raiz) atua como o ponto de entrada, realizando a **Injeção de Dependências** para "conectar" as camadas no início da aplicação.

## Tecnologias Utilizadas

* **Backend:**
    * Python 3
    * Flask (para o servidor web e API RESTful)
* **Banco de Dados:**
    * SQLite 3
* **Frontend:**
    * HTML5
    * CSS3
    * JavaScript (Vanilla JS, ES6+)
* **Padrões e Princípios:**
    * Arquitetura em Camadas (3-Tier)
    * SOLID
    * Injeção de Dependência (DI)
    * Padrão Repositório (Repository Pattern)

## Como Executar

Siga os passos abaixo para executar o projeto localmente.

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/taskflow.git](https://github.com/seu-usuario/taskflow.git)
    cd taskflow
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate
    
    # macOS / Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    *(Certifique-se de que seu `requirements.txt` contém `Flask`)*
    ```bash
    pip install -r requirements.txt
    ```

4.  **Inicialize o banco de dados:**
    *(Este comando só precisa ser executado uma vez para criar o arquivo `taskflow.db` e a tabela `tasks`)*
    ```bash
    python init_db.py
    ```

5.  **Rode a aplicação:**
    ```bash
    python app.py
    ```

6.  Acesse `http://127.0.0.1:5000` no seu navegador.

## API Endpoints

O projeto expõe uma API RESTful para gerenciar as tarefas:

| Método | Rota | Descrição |
| :--- | :--- | :--- |
| `GET` | `/api/tasks` | Retorna uma lista de todas as tarefas. |
| `POST` | `/api/tasks` | Cria uma nova tarefa. <br> *Body: `{ "title": "...", "description": "..." }`* |
| `PUT` | `/api/tasks/<int:task_id>` | Atualiza o status de uma tarefa. <br> *Body: `{ "status": "doing" }`* |
| `DELETE`| `/api/tasks/<int:task_id>` | Exclui uma tarefa. |

## Estrutura do Projeto

Abaixo está a organização dos arquivos do projeto, demonstrando a separação física das camadas:

```text
taskflow/
├── app.py                   # Ponto de entrada (Entry point) e DI Container
├── controllers/             # Camada de Interface (API Routes)
│   ├── __init__.py
│   └── home_controller.py
├── init_db.py               # Script de inicialização do banco
├── models/                  # Modelos de dados (DTOs/Entidades)
│   ├── __init__.py
│   └── task.py
├── repositories/            # Camada de Acesso a Dados
│   ├── base_repository.py   # Interface (Contrato)
│   ├── __init__.py
│   └── task_repository.py   # Implementação SQL
├── services/                # Camada de Regra de Negócio
│   ├── __init__.py
│   └── task_service.py
├── static/                  # Arquivos estáticos (Frontend)
│   ├── css/
│   │   └── style.css
│   ├── img/
│   │   └── laptop_img.png
│   └── js/
│       └── app.js
├── views/                   # Templates HTML
│   └── index.html
├── taskflow.db              # Arquivo do Banco de Dados SQLite
├── requirements.txt         # Dependências do projeto
└── README.md                # Documentação
