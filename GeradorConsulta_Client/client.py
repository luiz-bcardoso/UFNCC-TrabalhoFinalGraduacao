import xmlrpc.client

# URL utilizada para conexão do servidor RPC
url_servidor = "https://1ea9-35-204-181-100.ngrok-free.app"

# Realiza a conexão com o serivor RPC pela URL.
proxy = xmlrpc.client.ServerProxy(url_servidor)

# Envia uma pergunta e recebe a resposta.
pergunta = "me informe a quantidade de cada medicamento que sejam de tarja preta"
print("Usuário >", pergunta)
resposta = proxy.gerar_resposta(pergunta)
print("Lllama  >", resposta)

#Exibe a resposta gerada pela IA.
print("Resposta da IA:", resposta)