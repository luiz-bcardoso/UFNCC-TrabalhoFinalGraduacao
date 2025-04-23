from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM

from pyngrok import ngrok

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

import json
import re
import threading
import subprocess
import time

esquema_banco = {}

# Define a função que atualiza o contexto usando JSON
def atualizar_contexto(json_str):
    global esquema_banco
    try:
        print('------ ATUALIZANDO CONTEXTO ------')
        if isinstance(json_str, dict):
            esquema_banco = json_str
        else:
            esquema_banco = json.loads(json_str)
        return 'Contexto atualizado com sucesso!'
    except Exception as e:
        print(f"Erro ao atualizar o contexto: {str(e)}")
        return f"Erro ao atualizar o contexto: {str(e)}"
    finally:
        print('CONTEXTO ATUAL > ',esquema_banco)
        print('---- FIM ATUALIZAÇÃO CONTEXTO ----')
    
# Define a função que gera consultas SQL
def gerar_resposta(prompt_usuario: str) -> str:
    print('------ NOVA REQUISIÇÃO DO USUÁRIO ------')
    print('PERGUNTA > ', prompt_usuario)
    try:
        # Generate and process response
        llm_response = sql_chain.invoke({
            "input_text"  : prompt_usuario,
            "schema_info" : json.dumps(esquema_banco)
        })
        print('RESPOSTA > ', llm_response)

        # Extract SQL query
        sql_query = extrair_consulta_sql(llm_response)
        print('QUERYSQL > ', sql_query)

        return sql_query
    except Exception as e:
        error_msg = f"Erro ao gerar resposta: {str(e)}"
        print(error_msg)
        return error_msg
    finally:
        print('------- FIM REQUISIÇÃO DO USUÁRIO ------')

def extrair_consulta_sql(resposta_llm: str) -> str:
    """
    Extrai e retorna uma consulta SQL formatada a partir da resposta do LLM,
    que deve estar entre crases triplas.
    Retorna uma mensagem de erro se nenhuma consulta SQL válida for encontrada.
    """
    try:
        # Padrão regex para encontrar conteúdo entre ```sql``` ou apenas ```
        padrao = r'```(?:sql)?\s*(.*?)\s*```'
        match = re.search(padrao, resposta_llm, re.DOTALL)

        if match:
            # Extrai a consulta SQL e remove espaços em branco
            consulta_sql = match.group(1).strip()

            # Remove o prefixo 'SQL' se existir
            if consulta_sql.upper().startswith('SQL'):
                consulta_sql = consulta_sql[3:].strip()

            # Verifica se a consulta começa com SELECT
            if not consulta_sql.upper().startswith('SELECT'):
                return "Erro: A consulta retornado pelo servidor não é para recuperar dados!"

            # Remove ponto e vírgula final, se houver
            return consulta_sql.rstrip(';')

        return "Erro: Não foi possível gerar uma consulta com essas informações, por favor, tente novamente."

    except Exception as erro:
        return f"Erro: Falha ao processar a consulta SQL - {str(erro)}"
    
# Define o template (personalidade) que será utilizada pelo modelo.
# Para respostas mais precisas o template é estruturado em inglês.
prompt_template_sql = PromptTemplate.from_template(
    """
    Given the following SQL database schema:
    {schema_info}

    Convert the following natural language query into a SQL SELECT statement using only the schema as reference:
    {input_text}

    Rules:
    1. If the user asks for anything that is not relevant to queries, just reply: "I don't know."
    2. Ignore unrecognized tables/columns, don’t try to create new ones.
    3. Return only SQL queries in ``` marks, and don’t leave notes.
    4. Use SELECT statements only.
    5. Table names are duplicated due to Django; for example, usuario should be usuario_usuario.
    6. Most tables/columns are in Brazilian Portuguese, natural language, and may contain accents. You will need to remove them to correctly find them in the context.
    """
)

def run_ollama_serve():
  subprocess.Popen(["ollama", "serve"])

thread = threading.Thread(target=run_ollama_serve)
thread.start()
time.sleep(5)

# Tenta recuperar o contexto para utlizar no RAG via arquivo JSON.
try:
    with open("./esquema_banco_comic.json", "r") as file:
      esquema_banco = atualizar_contexto(json.load(file))
except FileNotFoundError:
    print("Arquivo 'esquema_banco.json' não encontrado.")

# Incializa o modelo usando recém criado llama3.1.
llm = OllamaLLM(
    model="llama3.1",
    temperature=0.1  # Menor tempereatura = Respota mais determinisitca.
)

# Inicializa a chain para fazer chamadas para LLM usando o template.
sql_chain = prompt_template_sql | llm

# Cria o serivdor RPC para responder requisições.
class ManipuladorDeRequisicoes(SimpleXMLRPCRequestHandler):
    rpc_paths = ("/RPC2",)

server = SimpleXMLRPCServer(
    ("0.0.0.0", 1346),
    requestHandler=ManipuladorDeRequisicoes,
    allow_none=True
)

# Registra somente as funções para gerar consultas e atualizar contexto via RPC.
server.register_function(atualizar_contexto, "atualizar_contexto")
server.register_function(gerar_resposta, "gerar_resposta")

# Cria uma URL pública pelo ngrok para acessar o serviço fora do Google Colab.
try:
    url_publica = ngrok.connect(1346, bind_tls=True).public_url
    print("URL Pública: ", url_publica)
except Exception as e:
    print(f"Falha ao conectar com ngrok: {str(e)}")
    raise

# Instancia o servidor e executa sem interrupção
print("Servidor XML-RPC em execução...")
server.serve_forever()