from xmlrpc.server import SimpleXMLRPCServer

# Define as funções utilizadas pelo cliente
def soma(x, y):
    return x + y

# Cria o servidor RPC
server = SimpleXMLRPCServer(("localhost", 8000))
print("Servidor criado e escutando na porta 8000...")

# Registra as funções
server.register_function(soma, "soma")

# Começa a rodar o servidor indefinidamente
server.serve_forever()
