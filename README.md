
# 📂 SharedFiles

> API REST para compartilhamento, listagem e gerenciamento de arquivos usando FastAPI e MongoDB (com fallback para SQLite).

---

## 🚀 Tecnologias Utilizadas

- **FastAPI** — Framework web rápido para criação de APIs.
- **MongoDB** — Armazenamento NoSQL para arquivos (via GridFS).
- **SQLite** — Alternativa local para testes e fallback.
- **Python 3.11+** — Linguagem principal do projeto.

---

## 📌 Funcionalidades

- 📤 Upload de arquivos (limite de 50MB, mas pode ser configurado no `.env`)
- 📜 Listagem completa de arquivos armazenados
- 🔍 Acesso direto ao conteúdo via ID
- 🗑️ Remoção de arquivos pelo ID
- 📊 Monitoramento de clusters MongoDB (caso configurado)
- 🧩 Suporte tanto a MongoDB quanto SQLite para ambientes variados

---

## 📦 Estrutura do Projeto

```
SharedFiles/
│── example.env
│── main.py
│── env.py
│── init.sql
│── requirements.txt
│── LICENSE
│
└── src/
    ├── app.py
    ├── api/
    │   └── files/
    │       ├── router.py
    │       └── docs.py
    ├── database/
    │   ├── client.py
    │   ├── mongo.py
    │   ├── sqlite.py
    │   └── utils.py
    └── schemas/
        └── file.py
```

---

## ⚙️ Configuração

### 1️⃣ Pré-requisitos

- **Python 3.11.0** ou superior
- **MongoDB local ou remoto** (opcional se for usar SQLite apenas)

### 2️⃣ Instalação

Clone o repositório:

```bash
git clone https://github.com/nanyuss/SharedFiles.git
cd SharedFiles
```

Crie e ative o ambiente virtual (Opcional, mas recomendado):

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

### 3️⃣ Variáveis de Ambiente

Crie um arquivo `.env` baseado no `example.env`:

```env
# Token de autorização para rotas protegidas
AUTHORIZATION=222a1c3d9e2e42e3982403a8efc8c596

# Tamanho máximo de upload (em bytes)
MAX_FILE_SIZE=52428800

# MongoDB principal (opcional se usar apenas SQLite)
MONGO_URI=

# Clusters distribuídos (para uso com GridFS)
MONGO_URI_FILES_PHOENIX=
MONGO_URI_FILES_NANO=
MONGO_URI_FILES_STAR=
MONGO_URI_FILES_CAT=
```

---

## ▶️ Execução do Projeto

Execute o servidor FastAPI com:

```bash
python main.py
```

Acesse a documentação interativa da API:

- [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🖥️ Endpoints da API

| Método   | Rota                     | Descrição                                                              |
|----------|--------------------------|-------------------------------------------------------------------------|
| `GET`    | `/files`                 | Lista todos os arquivos armazenados.                                   |
| `GET`    | `/files/{file_id}`       | Obtém o conteúdo de um arquivo específico.                             |
| `POST`   | `/files/upload`          | Faz upload de um novo arquivo.                                         |
| `DELETE` | `/files/{file_id}`       | Remove o arquivo correspondente ao ID.                                 |
| `GET`    | `/files/clusters`        | Retorna informações e status dos clusters de armazenamento (MongoDB).  |

---

## 📘 Exemplo de Resposta

### `GET /files`

```json
[
  {
    "file_id": "66a0e6faedc1...",
    "filename": "imagem.png",
    "size": 39200,
    "cluster": "PHOENIX",
    "uploaded_at": "2025-07-02T18:22:10Z"
  }
]
```

---

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

---

## 📜 Licença

Distribuído sob a licença **MIT**. Veja `LICENSE` para mais detalhes.

---

## 🧠 Inspiração

Este projeto foi inspirado no **[ADG Share](https://github.com/euandrelucas/adg-share)**, um servidor de compartilhamento de arquivos criado por André Lucas (@euandrelucas), desenvolvido com Node.js, Fastify e Prisma.  
SharedFiles busca replicar a ideia central — upload, download e controle de tamanho — mas com foco em modularidade, suporte a múltiplos clusters MongoDB, abstração para SQLite e escrita em Python com FastAPI.
