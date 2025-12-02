# TaskFlow Kanban 

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Security](https://img.shields.io/badge/Security-Flask_Login-green?style=for-the-badge&logo=lock)

Um organizador de tarefas no estilo Kanban, desenvolvido com foco em Arquitetura Limpa, princípios **SOLID** e segurança. O sistema agora é multi-usuário (SaaS), garantindo privacidade e isolamento de dados.

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

O **TaskFlow** é uma aplicação web completa para gerenciamento de produtividade pessoal. Diferente de listas de tarefas simples, ele utiliza um painel Kanban (*To Do*, *Doing*, *Done*) e oferece um ambiente seguro onde cada usuário tem acesso exclusivo aos seus próprios dados.

Este projeto foi desenvolvido não apenas para entregar funcionalidade, mas para demonstrar a aplicação prática de padrões de engenharia de software robustos em Python, como **Injeção de Dependência**, **Repository Pattern** e **Autenticação Segura**.

##  Funcionalidades

O sistema implementa **CRUDs completos** para Tarefas e Usuários, além de regras de negócio de segurança:

* **Autenticação e Segurança:**
    * Sistema de Login e Cadastro de usuários.
    * Edição de Perfil (Alteração de nome e senha com validação de segurança).
    * Criptografia de senhas (Hashing) no banco de dados.
    * Controle de sessão seguro e rotas protegidas (`@login_required`).

* **Multi-Tenancy (Multi-usuário):**
    * Isolamento total de dados: cada usuário vê apenas as suas próprias tarefas.
    * Validação de propriedade no backend (impede manipulação de tarefas de outros usuários via API).

* **Gerenciamento de Tarefas:**
    * **[C]reate:** Adicionar novas tarefas.
    * **[R]ead:** Visualização em colunas Kanban.
    * **[U]pdate:** Atualização de status via *drag-and-drop* intuitivo.
    * **[D]elete:** Exclusão segura de tarefas.

## Arquitetura do Software

O backend segue uma arquitetura em 3 camadas (3-Tier) para garantir a **separação de responsabilidades** (SRP) e testabilidade.

1.  **Camada de Controladores (`/controllers`)**
    * Gerencia as rotas (Web e API).
    * Lida com a sessão do usuário (Login/Logout).
    * Não contém regras de negócio; apenas repassa dados para os serviços.

2.  **Camada de Serviços (`/services`)**
    * Coração da lógica de negócio e segurança.
    * Exemplos de regras: "Criptografar senha antes de salvar", "Verificar se o usuário é dono da tarefa antes de excluir", "Tarefas novas nascem como 'todo'".

3.  **Camada de Repositórios (`/repositories`)**
    * Responsável exclusivo pelo acesso ao dados (SQL).
    * Implementa a interface `BaseRepository` para desacoplamento.
    * Gerencia as tabelas `users` e `tasks` no SQLite.

A injeção de dependências é configurada no `app.py`, conectando as camadas de baixo para cima.

## Tecnologias Utilizadas

* **Backend:** Python 3, Flask, Flask-Login (Gestão de Sessão), Werkzeug (Segurança/Hash).
* **Banco de Dados:** SQLite 3 (Com suporte a Chaves Estrangeiras).
* **Frontend:** HTML5, CSS3, JavaScript (Vanilla ES6+).
* **Padrões:** SOLID, Repository Pattern, Dependency Injection, MVC.

## Como Executar

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/carloshfgit/taskflow.git](https://github.com/carloshfgit/taskflow.git)
    cd taskflow
    ```

2.  **Crie e ative o ambiente virtual:**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate
    
    # Linux/macOS
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Inicialize o Banco de Dados:**
    ```bash
    python init_db.py
    ```
    *Isso criará o arquivo `taskflow.db` com as tabelas `users` e `tasks` configuradas.*

5.  **Execute a aplicação:**
    ```bash
    python app.py
    ```

6.  Acesse `http://127.0.0.1:5000`. Você será redirecionado para a tela de Login/Cadastro.

## API Endpoints

A API é RESTful e todas as rotas abaixo são **protegidas** (requerem autenticação/sessão ativa).

| Método | Rota | Descrição |
| :--- | :--- | :--- |
| `POST` | `/login` | Autentica o usuário e cria a sessão. |
| `POST` | `/register` | Cria um novo usuário. |
| `GET` | `/logout` | Encerra a sessão do usuário (Logout). |
| `POST` | `/delete_account` | Exclui permanentemente a conta e tarefas do usuário. |
| `GET` | `/api/tasks` | Retorna as tarefas **do usuário logado**. |
| `POST` | `/api/tasks` | Cria tarefa para o usuário atual. |
| `PUT` | `/api/tasks/<id>` | Atualiza status (apenas se for dono da tarefa). |
| `DELETE`| `/api/tasks/<id>` | Exclui tarefa (apenas se for dono da tarefa). |
| `GET`| `/profile` | Exibe o formulário de edição de perfil. |
| `POST`| `/profile` | Processa a atualização de dados do usuário. |

## Estrutura do Projeto

```text
taskflow/
├── app.py                   # Configuração, DI e App Entry point
├── init_db.py               # Script de migração do banco
├── controllers/             # Camada de Interface
│   ├── auth_controller.py   # Login e Registro
│   ├── home_controller.py   # Tarefas e Dashboard
│   └── __init__.py
├── services/                # Regras de Negócio e Segurança
│   ├── user_service.py      # [NOVO] Lógica de usuários
│   ├── task_service.py      # Lógica de tarefas
│   └── __init__.py
├── repositories/            # Acesso a Dados (SQL)
│   ├── base_repository.py   # Interface
│   ├── user_repository.py   # Tabela Users
│   ├── task_repository.py   # Tabela Tasks
│   └── __init__.py
├── models/                  # Entidades
│   ├── user.py              # [NOVO] Modelo User
│   ├── task.py              # Modelo Task
│   └── __init__.py
├── static/                  # Assets (CSS/JS/Img)
├── views/                   # Templates HTML
│   ├── index.html           # Dashboard
│   ├── login.html           # Tela de Login
│   └── register.html        # Tela de Cadastro
|   └── profile.html         # Tela de Perfil

└── requirements.txt         # Dependências