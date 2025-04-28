# Conectando no servidor RPC sem precisar de um projeto Django
Nesta seção, as mesmas classes utilizadas no projeto Django para o módulo gerador serão utilizadas aqui mas sem a necessidade de um projeto, apenas usando as funções da classe conecta para gerar consultas e o atualizar o contexto.

Antes de executar essa parte é necessário ter um servidor rodando, a seção onde inicializar o servidor pode ser encotrada [neste link](https://github.com/luiz-bcardoso/UFNCC-TrabalhoFinalGraduacao/tree/main/GeradorConsulta_Server).

---

## Instalação e Configuração

### 1. Crie e ative um ambiente virtual venv

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Instale as dependências do Python

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 3. Informar a URL pública do servidor
Altere a linha 12 e coloque a URL gerada pelo servidor
```python
...
url_servidor = '<COLOQUE_SUA_URL_AQUI>'
...
```

### 4. Execute o cliente e informe uma pergunta
```bash
python main.py
```
