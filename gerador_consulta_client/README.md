# Conectando ao Servidor RPC sem um Projeto Django

Nesta seção, vamos utilizar as mesmas classes do módulo gerador do projeto Django, mas sem a necessidade de um projeto completo. Será utilizado apenas as funções da classe `Conecta` para gerar consultas e atualizar o contexto.

**Nota:** Antes de começar, é necessário que o servidor esteja em funcionamento. Você pode encontrar a seção que explica como inicializar o servidor [aqui](https://github.com/luiz-bcardoso/UFNCC-TrabalhoFinalGraduacao/tree/main/GeradorConsulta_Server).

---

## Instalação e Configuração

### 1. Certifique-se de estar no diretório correto

Primeiro, navegue até o diretório do cliente.

```bash
cd gerador_consulta_client
```

### 2. Crie e ative um ambiente virtual (`venv`)

Crie um ambiente virtual para isolar as dependências do projeto:

```bash
#Linux
python3 -m venv venv
source venv/bin/activate
```

```bash
#Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instale as dependências do Python

Atualize o `pip` e instale as dependências necessárias listadas no arquivo `requirements.txt`:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Informe a URL pública do servidor

Crie um arquivo `.env` na **raiz** do repositório e adicione a URL do servidor. Para isso, use o comando:

```bash
# Linux
nano ../.env
```

```bash
# Windows
echo. > ..\.env
```
Dentro do arquivo `.env`, crie uma variável chamada `GERADORSQL_URL` e cole a URL do servidor gerado:

```bash
GERADORSQL_URL='<COLOQUE_SUA_URL_AQUI>'
```
### 5. Atualizar o contexto RAG do servidor via RPC

Com um esquema de banco de dados de qualquer projeto, envie o arquivo .json via RPC com o código atualiza_contexto.py

Obs.: Por padrão o esquema do COMIC é utilizado e já está configurado o caminho no código.
```bash
python atualiza_contexto.py
```

### 6. Execute o Cliente e Informe uma Pergunta

Agora você pode rodar o cliente para testar a conexão. Basta executar o comando abaixo:

```bash
python main.py
```
