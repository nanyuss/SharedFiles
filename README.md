# 📂 SharedFiles  

SharedFiles é uma API simples para compartilhamento e gerenciamento de arquivos. Este projeto fornece endpoints para upload, listagem e remoção de arquivos, utilizando **FastAPI** e armazenamento no **MongoDB**.  

## 🚀 Tecnologias Utilizadas  

- **FastAPI** - Framework web para construção da API.  
- **MongoDB** - Banco de dados NoSQL para armazenar metadados dos arquivos.  
- **Python** - Linguagem principal do projeto.  

## 📌 Funcionalidades  

- 📤 **Upload de arquivos**  
- 📜 **Listagem de arquivos armazenados**  
- 🗑️ **Remoção de arquivos**  

## 📦 Estrutura do Projeto  

```
SharedFiles/
│── api/
│   ├── files.py
│── core/
│   ├── database.py
│   ├── schemas/
│   │   ├── file.py
│   ├── data/
│   │   ├── files_info.py
│── app.py
│── example.env
│── requirements.txt
│── .gitignore
│── README.md
```

## ⚙️ Configuração  

### 1️⃣ Pré-requisitos  

- **Python 3.12.0** ou superior  
- **MongoDB** instalado ou disponível em um servidor remoto  

### 2️⃣ Instalação  

Clone o repositório:  

```bash
git clone https://github.com/seu-usuario/SharedFiles.git
cd SharedFiles
```

Crie e ative um ambiente virtual (opcional, mas recomendado):  

```bash
python -m venv venv
source venv/bin/activate  # No Windows, use: venv\Scripts\activate
```

Instale as dependências:  

```bash
pip install -r requirements.txt
```

### 3️⃣ Configuração do Banco de Dados  

Crie um arquivo `.env` baseado no `example.env` e defina suas credenciais:  

```
AUTHORIZATION="222a1c3d9e2e42e3982403a8efc8c596"
DEFAULT_URL="http://127.0.0.1"
MONGO_URI="mongodb://localhost:27017"

MONGO_URI_FILES_1 = "mongodb://localhost:27017"
MONGO_URI_FILES_2 = "mongodb://localhost:27017"
MONGO_URI_FILES_3 = "mongodb://localhost:27017"
MONGO_URI_FILES_4 = "mongodb://localhost:27017"
```

### 4️⃣ Executando o Projeto  

Inicie o servidor FastAPI:  

```bash
py app.py
```

Agora, acesse a documentação interativa da API no navegador:  

- **Swagger UI**: [http://127.0.0.1](http://127.0.0.1)   

## 🖥️ Endpoints da API  

| Método  | Endpoint        | Descrição                           |
|---------|----------------|-------------------------------------|
| `GET`  | `api/files/clusters`      | Retorna as informações de todas as clusters de arquivos, incluindo o armazenamento disponível, total, utilizado, número de arquivos, tipos de arquivos, e dados adicionais de cada cluster.       |
| `POST`  | `api/files/upload`      | Realiza o upload de um arquivo para o servidor. O tamanho máximo permitido é de 50 MB. O arquivo será armazenado no diretório de uploads e os metadados serão salvos no banco de dados.       |
| `GET`   | `api/files`       | Retorna uma lista contendo todos os metadados dos arquivos armazenados. |
| `GET`   | `api/files/{file_id}`       | Acessa o conteúdo de um arquivo armazenado no servidor com base no ID fornecido. |
| `DELETE` | `api/files/{file_id}` | Deleta um arquivo armazenado no servidor e seus metadados no banco de dados com base no ID fornecido.  |

## 🤝 Contribuições  

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests no repositório.

## 📜 Licença  

Este projeto está licenciado sob a **MIT License**.