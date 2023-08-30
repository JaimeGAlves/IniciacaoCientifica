## Bootstrap

### Install dependencies

Install the openbabel dependency on your system

```shell
sudo apt-get openbabel
```

Create a virtualenv and install the python dependencies

```shell
pip install -r requirements.txt
```

## Running the project

```shell
uvicorn server:app --reload
```

## Rotas
esquema de rotas

### POST /uploadfile

Recebe um arquivo e retorna o resultado do processamento

#### Request

```shell
curl -X POST "http://localhost:8000/uploadfile" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@/path/to/file"
```

#### Response

```json
{
  "message": "string",
  "file": {
    "project_id": "string",
    "id": "integer",
    "url": "string",
    "converted": "boolean",
    "updated_at": "string",
    "status": "string",
    "project_name": "string",
    "created_at": "string"
  }
}
```

### GET /status/{project_id}

Retorna o status do projeto no swissmodel

#### Request

```shell
curl -X GET "http://localhost:8000/status/{project_id}" -H "accept: application/json"
```

#### Response

```json
{
  "project_id": "string",
  "status": "string",
  "models": "integer",
  "date_created": "string",
  "project_title": "string",
}
```

### GET /all-files

Retorna todos os arquivos

#### Request

```shell
curl -X GET "http://localhost:8000/all-files" -H "accept: application/json"
```

#### Response

```json
[
  {
    "project_id": "string",
    "id": "integer",
    "url": "string",
    "converted": "boolean",
    "updated_at": "string",
    "status": "string",
    "project_name": "string",
    "created_at": "string"
  }
]
```

## Todo

- [x] setup
- [x] rota que recebe um file e retorna o resultado do processamento
- [x] subir arquivo pro dropbox e retornar o link