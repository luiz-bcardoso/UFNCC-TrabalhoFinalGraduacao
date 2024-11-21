import xmlrpc.client

# Conecta no servidor local
rpc_server = xmlrpc.client.ServerProxy(
    "http://localhost:8000/"
)

# Faz a chamada remota do méotodo (RPC)
resposta = rpc_server.soma(5, 3)
print(f"Servidor retornou a mensagem: {resposta}")






