import xmlrpc.client

# URL utilizada para conexão do servidor RPC
url_servidor = "https://b038-34-16-141-135.ngrok-free.app"

# Realiza a conexão com o serivor RPC pela URL.
proxy = xmlrpc.client.ServerProxy(url_servidor)

# Abre o arquivo JSON para envar para o servidor
with open("/workspaces/comic/esquema_banco_mysql.json", "r") as file:
    # Lê o conteúdo do arquivo JSON
    json_data = file.read()
    # Envia o JSON para o servidor
    resposta = proxy.atualizar_contexto(json_data)
    # Imprime a resposta do servidor    
    print(resposta)
