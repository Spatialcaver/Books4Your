# 📚 BooksForYou - Sistema de Gerenciamento de Biblioteca



Este projeto implementa uma API RESTful completa para gerenciamento de uma biblioteca, incluindo controle de usuários, livros, autores e empréstimos, utilizando **Django** e **Django Rest Framework (DRF)**.

---

## ⚙️ 1. Requisitos e Instalação

### 1.1 Pré-requisitos

* Python 3.x (Recomendado 3.10+)
* `pip` (Gerenciador de pacotes Python)
* `git`

### 1.2 Passo a Passo

1.  **Clone o Repositório:**
    ```bash
    git clone [URL_DESTE_REPOSITÓRIO]
    cd BooksForYou
    ```

2.  **Crie e Ative o Ambiente Virtual:**
    ```bash
    # Cria o ambiente
    python -m venv venv
    
    # Ativa o ambiente (Windows PowerShell)
    .\venv\Scripts\Activate
    
    # Se estiver usando Linux/macOS ou Git Bash:
    # source venv/bin/activate
    ```

3.  **Instale as Dependências:**
    ```bash
    pip install -r requirements.txt 
    # (Ou instale manualmente: Django, djangorestframework, djangof-filters, drf-spectacular, python-dotenv, djangorestframework-simplejwt)
    ```

---

## 📝 2. Configuração e Banco de Dados

### 2.1 Configuração do Arquivo `.env`

Crie um arquivo chamado **`.env`** na raiz do projeto (no mesmo diretório do `manage.py`) para armazenar as variáveis de ambiente sensíveis.

env
### Variáveis de Ambiente (.env)

### Chave Secreta do Django (Gere uma chave nova e segura)
```SECRET_KEY=sua_chave_secreta_aqui_para_producao```

### Modo de Debug
```DEBUG=True```

### Hosts Permitidos (separados por vírgula)
```ALLOWED_HOSTS=127.0.0.1,localhost```

## 2.2 Migrações e Superusuário
### Aplique as migrações no banco de dados SQLite e  crie um usuário administrador.

- Aplique as Migrações:

```Bash
py manage.py makemigrations
py manage.py migrate
```
- Crie o Superusuário (Admin):


```Bash

py manage.py createsuperuser 
```
#  3. Execução

### Execute o servidor de desenvolvimento do Django:

```Bash

py manage.py runserver
A API estará acessível em http://127.0.0.1:8000/.
```


### 4. Uso da API

### 4.1 Autenticação

A aplicação usa JWT (JSON Web Token) para autenticação. Todas as rotas (exceto `GET /books/list/` e as rotas de autenticação) exigem um **Access Token** no cabeçalho.

| Endpoint | Path | Método | Descrição |
| :--- | :--- | :--- | :--- |
| Obter Token | `/users/token/` | `POST` | Fornece `username` e `password` para obter o `access` e `refresh` token. |
| Renovar Token | `/users/token/refresh/` | `POST` | Envia o `refresh` token para obter um novo `access` token. |



## Authorization: Bearer [SEU_ACCESS_TOKEN_AQUI]

---

### 4.2 Endpoints Principais

| App | Endpoint | Método | Descrição | Requer Auth |
| :--- | :--- | :--- | :--- | :--- |
| Auth/User | `/users/create/` | `POST` | **CRUD:** Cria novo usuário (registro). | Sim |
| User | `/users/list/` | `GET` | **CRUD:** Lista todos os usuários. | Sim |
| Book | `/books/list/` | `GET` | **CRUD:** Lista todos os livros. | Não |
| Book | `/books/create/` | `POST` | **CRUD:** Cria um novo livro. | Sim |
| Borrowing | `/borrowings/create/` | `POST` | **Empréstimo:** Registra novo empréstimo (Regras de Negócio aplicadas). | Sim |
| Borrowing | `/borrowings/list/` | `GET` | **Empréstimo:** Lista os livros emprestados **pelo usuário autenticado**. | Sim |

---

### 🧩 5. Recursos Avançados (Filtros, Ordenação e Documentação)

#### 5.1 Documentação (Swagger UI)

Acesse a URL abaixo para interagir com a documentação em tempo real, testar endpoints e ver os esquemas de dados (Swagger UI):

[http://127.0.0.1:8000/api/schema/swagger-ui/](http://127.0.0.1:8000/api/schema/swagger-ui/)

---

### 5.2 Filtros e Ordenação (Book List)

O endpoint de listagem de livros (`/books/list/`) suporta filtragem e ordenação:

| Funcionalidade | Parâmetros de Query | Exemplo |
| :--- | :--- | :--- |
| **Filtro por Autor** | `?author_name=[nome]` ou `?author_id=[uuid]` | `?author_name=rowling` |
| **Filtro por Categoria** | `?category=[código_categoria]` | `?category=FAN` |
| **Ordenação** | `?ordering=[campo]` | `?ordering=-publication_date` (descendente) |
| **Campos Ordenáveis** | `title`, `publication_date`, `author__name` | - |

---

### 5.3 Paginação

Todas as listas de resultados são paginadas por padrão (10 itens por página). Use os parâmetros `?page=` e `?page_size=` para navegar e ajustar a paginação.


## 5.3 Executando tests
```Bash
py manage.py test borrowing


```
ou 

### 5.3 Usando Pytest
- Instale a dependencia no terminal usando o comando
```Bash
pip install pytest pytest-django

```

- Crie um arquivo na raiz do projeto chamado 'pytest.ini' com as seguintes configs: 
```python
# pytest.ini
[pytest]
# Configura o Pytest para carregar as configurações do Django
DJANGO_SETTINGS_MODULE = core.settings
# Define os apps onde o Pytest deve procurar por testes
python_files = tests.py test_*.py *_tests.py
# Adiciona o diretório raiz dos apps para descoberta de testes
addopts = --reuse-db

```

- No terminal execute o Comando:

```Bash
pytest

```


_______________________________________________________________________________________________________________________

## English README

_______________________________________________________________________________________________________________________



# 📚 BooksForYou - Library Management System

This project implements a complete RESTful API for managing a library, including user, book, author, and loan control, using **Django** and **Django Rest Framework (DRF)**.

---

## ⚙️ 1. Requirements and Installation

### 1.1 Prerequisites

* Python 3.x (3.10+ recommended)
* `pip` (Python package manager)
* `git`

### 1.2 Step-by-Step

1. **Clone the Repository:**

``bash

git clone [URL_OF_THIS_REPOSITORY]

cd BooksForYou

``

2. **Create and Activate the Virtual Environment:**

``bash

# Creates the environment
python -m venv venv

# Activates the environment (Windows PowerShell)

.\venv\Scripts\Activate

# If using Linux/macOS or Git Bash:

# source venv/bin/activate

```

3. **Install the Dependencies:**

``bash
pip install -r requirements.txt

# (Or install manually: Django, djangorestframework, djangof-filters, drf-spectacular, python-dotenv, djangorestframework-simplejwt)

``

---

## 📝 2. Configuration and Database

### 2.1 Configuring the `.env` File

Create a file called **`.env`** in the project root (in the same directory as `manage.py`) to store sensitive environment variables.

environment variables (.env)

### Django Secret Key (Generate a new and secure key)
```SECRET_KEY=your_secret_key_here_for_production```

### Debug Mode
```DEBUG=True```

### Allowed Hosts (comma-separated)
```ALLOWED_HOSTS=127.0.0.1,localhost```

## 2.2 Migrations and Superuser
### Apply the migrations to the SQLite database and create an administrator user.

- Apply Migrations:

```Bash
py manage.py makemigrations
py manage.py migrate
```
- Create the Superuser (Admin):

```Bash

py manage.py createsuperuser
```
# 3. Execution

### Run the Django development server:

```Bash

py manage.py runserver
The API will be accessible at http://127.0.0.1:8000/.

```

### 4. API Usage

### 4.1 Authentication

The application uses JWT (JSON Web Token) for authentication. All routes (except `GET /books/list/` and the authentication routes) require an **Access Token** in the header.

| Endpoint | Path | Method | Description |

| :--- | :--- | :--- | :--- |

| Get Token | `/users/token/` | `POST` | Provides `username` and `password` to obtain the `access` and `refresh` token. |

| Renew Token | `/users/token/refresh/` | `POST` | Sends the `refresh` token to obtain a new `access` token. |

## Authorization: Bearer [YOUR_ACCESS_TOKEN_HERE]

---

### 4.2 Main Endpoints

| App | Endpoint | Method | Description | Requires Auth |

| :--- | :--- | :--- | :--- | :--- |

| Auth/User | `/users/create/` | `POST` | **CRUD:** Creates a new user (registration). | Yes |

| User | `/users/list/` | `GET` | **CRUD:** Lists all users. | Yes |

| Book | `/books/list/` | `GET` | **CRUD:** Lists all books. | No |

| Book | `/books/create/` | `POST` | **CRUD:** Creates a new book. | Yes |

| Borrowing | `/borrowings/create/` | `POST` | **Loan:** Registers a new loan (Business Rules applied). | Yes |

| Borrowing | `/borrowings/list/` | `GET` | **Loan:** Lists the books borrowed **by the authenticated user**. | Yes |

---

### 🧩 5. Advanced Features (Filters, Sorting, and Documentation)

#### 5.1 Documentation (Swagger UI)

Access the URL below to interact with the real-time documentation, test endpoints, and view the data schemas (Swagger UI):

[http://127.0.0.1:8000/api/schema/swagger-ui/](http://127.0.0.1:8000/api/schema/swagger-ui/)

---

### 5.2 Filters and Sorting (Book List)

The book listing endpoint (`/books/list/`) supports filtering and sorting:

| Functionality | Query Parameters | Example |

| :--- | :--- | :--- |

| **Filter by Author** | `?author_name=[name]` or `?author_id=[uuid]` | `?author_name=rowling` |

| **Filter by Category** | `?category=[category_code]` | `?category=FAN` |

| **Sorting** | `?ordering=[field]` | `?ordering=-publication_date` (descending) |

| **Sortable Fields** | `title`, `publication_date`, `author__name` | - |

---

### 5.3 Pagination

All result lists are paginated by default (10 items per page). Use the parameters `?page=` and `?page_size=` to navigate and adjust the pagination.

## 5.3 Running Tests
```Bash py manage.py test borrowing

```
or

### 5.3 Using Pytest

- Install the dependency in the terminal using the command
```Bash pip install pytest pytest-django

```

- Create a file in the project root called 'pytest.ini' with the following configurations:
```python
# pytest.ini
[pytest]
# Configures Pytest to load Django settings
DJANGO_SETTINGS_MODULE = core.settings
# Defines the apps where Pytest should look for tests
python_files = tests.py test_*.py *_tests.py
# Adds the root directory of the apps for test discovery
addopts = --reuse-db

```

- In the terminal, execute the command:

```Bash pytest

```