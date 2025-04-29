import datetime
import xmlrpc.client

from django.db import connection
from django.template import Template, Context

class Conecta:
    
    @staticmethod
    def conecta_rpc():
        # Realiza a conexão com o serivor RPC pela URL.
        url_servidor = '<COLOQUE_SUA_URL_AQUI>'
        
        try:
            proxy = xmlrpc.client.ServerProxy(url_servidor)
            return proxy
        except Exception as e:
            erro = f"Erro de conexão, contate o administrador. \nCódigo: {str(e)}"
            return erro
    
    @staticmethod
    def atualiza_contexto():
        #TODO: Implementar gerador de contexto JSON usando models do projeto.
        try:
            proxy = Conecta.conecta_rpc()
            with open("esquema_banco.json", "r") as file:
                #Lê o arquivo Json e envia para o servidor
                json_data = file.read()
                resposta = proxy.atualizar_contexto(json_data)
                return resposta
        except Exception as e:
            return f"Erro ao atualizar contexto. Exceção: {str(e)}"
    
    @staticmethod
    def gera_sql(pergunta):
        try:
            proxy = Conecta.conecta_rpc()
            resposta = proxy.gerar_resposta(pergunta)
            return resposta
        except Exception as e:
            erro = f"Não foi possível conectar no servidor para gerar a consulta. Por favor, tente novamente mais tarde."
            return erro
        
    @staticmethod
    def consulta_sql_safe(sql):
        sql = sql.strip().lower()

        # Primeiro, verifica se a consulta começa com SELECT ou WITH
        if not sql.startswith("select") and not sql.startswith("with"):
            return False

        # Segundo, verifica se há ponto e vírgula no meio da consulta
        if ';' in sql:
            parts = [p.strip() for p in sql.split(';') if p.strip()]
            for part in parts:
                if not part.startswith('select') and not part.startswith('with'):
                    return False

        # Por fim, verifica se há palavras-chave potencialmente perigosas
        forbidden = ['insert', 'update', 'delete', 'drop', 'alter', 'create', 'exec', 'merge', 'truncate']
        if any(word in sql for word in forbidden):
            return False

        return True
    
    @staticmethod
    def executa_sql(script_sql):
        try:
            # Verifica se a consulta é segura
            if not Conecta.consulta_sql_safe(script_sql):
                return "Uma consulta potencialmente insegura foi detectada. Por favor, tente novamente."

            # Conecta no banco com cursor e obtém os resultados   
            with connection.cursor() as cursor:
                cursor.execute(script_sql)
                resultados = cursor.fetchall()
                
                # Se não houver resultados, retorna a mensagem
                if not resultados:
                    resultados = "Nenhum resultado relevante foi encontrado."         

                # Obtém os nomes dos campos
                nomes_campos = [i[0].upper() for i in cursor.description]
                
                cursor.close()
                
            # Se não houver "order by" na consulta, ordena a lista de listas   
            if "order by" not in script_sql.upper():
                lista_dados = sorted(resultados, key=lambda x: x[0])
            else:
                lista_dados = resultados
                
            # Filtra os resultados
            lista_filtrada = Conecta.filtra_sql(lista_dados, nomes_campos)

            # Gera a tabela HTML com os resultados filtrados
            return Conecta.gera_tabela_html(nomes_campos, lista_filtrada)
        except Exception as e:
            return f"Erro na execução da consulta. Contate o administrador. Erro: {str(e)}"
    
    @staticmethod
    def filtra_sql(resultados, nomes_campos):
        # Filtra campos indesejados
        campos_indesejados = {'SLUG', 'PASSWORD', 'ARQUIVO_PROJETO'}
        indices_validos = [i for i, nome in enumerate(nomes_campos) if nome not in campos_indesejados]
        nomes_campos = [nomes_campos[i] for i in indices_validos]
        
        # Se houver mais de 5 colunas, retorna a mensagem
        if len(nomes_campos) > 5:
            return "Mais de 5 colunas retornadas. Por favor, refine sua consulta."
        
        # Converte os resultados (tuplas) em uma lista de listas, filtrando os campos indesejados
        lista_dados = [[linha[i] for i in indices_validos] for linha in resultados]

        # Formata os objetos datetime.date/datetime para o formato brasileiro
        for linha in lista_dados:
            for i, valor in enumerate(linha):
                if isinstance(valor, datetime.date):
                    linha[i] = valor.strftime('%d/%m/%Y')
                if isinstance(valor, datetime.datetime):
                    linha[i] = valor.strftime('%d/%m/%Y %H:%M:%S')
                        
        return lista_dados
    
    @staticmethod
    def gera_tabela_html(nomes_campos, lista_dados):
        template_str = """
                        <h2 style="text-align:center;">Tabela de Resposta</h2>
                        <table class="table table-hover">
                            <thead>
                                <tr>
                                    {% for campo in nomes_campos %}
                                        <th>{{ campo }}</th>
                                    {% endfor %}
                                </tr>
                            </thead>
                            <tbody>
                                {% for item in lista_dados %}
                                    <tr>
                                        {% for valor in item %}
                                            <td>{{ valor }}</td>
                                        {% endfor %}
                                    <tr>
                                {% endfor %}
                            </tbody>
                        </table>  
                        <p><b>Total de registros:</b> {{ lista_dados|length }}</p>
                        """
        template = Template(template_str)
        context = Context({
            'nomes_campos': nomes_campos,
            'lista_dados': lista_dados
        })
        return template.render(context)