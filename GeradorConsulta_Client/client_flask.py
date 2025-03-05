from flask import Flask, request, render_template
import xmlrpc.client

app = Flask(__name__)

# URL utilizada para conexão do servidor RPC
url_servidor = "https://9421-34-118-195-203.ngrok-free.app"

# Realiza a conexão com o servidor RPC pela URL.
proxy = xmlrpc.client.ServerProxy(url_servidor)

@app.route('/', methods=['GET', 'POST'])
def chatbot():
    resposta = None
    if request.method == 'POST':
        # Get user input from the form
        user_input = request.form['user_input']
        
        # Envia uma pergunta e recebe a resposta.
        resposta = proxy.gerar_resposta(user_input)

    # Render the external HTML template with the response (if any)
    return render_template('index.html', response=resposta)

if __name__ == '__main__':
    app.run(debug=True)