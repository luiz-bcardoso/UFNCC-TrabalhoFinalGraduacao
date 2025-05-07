import xmlrpc.client

from decouple import config

# URL utilizada para conexão do servidor RPC
url_servidor = config('GERADORSQL_URL')

# Realiza a conexão com o serivor RPC pela URL.
proxy = xmlrpc.client.ServerProxy(url_servidor)

# Abre o arquivo JSON para envar para o servidor
with open("../gerador_consulta_server/esquema_banco_comic.json", "r") as file:
    # Lê o conteúdo do arquivo JSON
    json_data = file.read()
    # Envia o JSON para o servidor
    resposta = proxy.atualiza_contexto(json_data)
    # Imprime a resposta do servidor    
    print(resposta)
