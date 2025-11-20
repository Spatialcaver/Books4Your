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