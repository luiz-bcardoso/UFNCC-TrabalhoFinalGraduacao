## Tempo = time.time()
## Precisão = consulta já montada com dados retornados (linha -> referencia *equals)
## Consistencia = quantas vezes ira executar e tem a memsa resposta? (lista[linhas] -> referencia *equals) 
## Falhas = entrou em algum except? (contabiliza)
## Consultas = numero de vezes que faz a mesma pergunta

import sqlite3
import time

from conecta_llm import Conecta
from resultado import Resultado

def executa_sql(sql):
    # Verifica se a consulta é segura
    if not Conecta.checa_consulta_segura(sql):
        return "Uma consulta potencialmente insegura foi detectada. Por favor, tente novamente."
    # Conecta no banco SQLite3 com cursor
    connection = sqlite3.connect("../db.sqlite3")
    cursor = connection.cursor()  
    # Utiliza o cursor para executar a consulta SQL
    with connection:
        cursor.execute(sql)
        tuplas_resultados = cursor.fetchall()
        nome_campos = [i[0].upper() for i in cursor.description]
        cursor.close()
    # Fecha a conexão com o banco e retorna os resultados   
    connection.close()
    return tuplas_resultados, nome_campos

def calcular_precisao(linha_resultado, linha_referencia):
    total_elementos = len(linha_referencia)
    num_acertos = 0
    # Verifica se a lista de referência está vazia
    if total_elementos == 0:
        return 0.0
    # Verifica se as listas têm o mesmo tamanho
    for dado_ref, dado_res in zip(linha_referencia, linha_resultado):
        if dado_ref == dado_res:
            num_acertos += 1     
    # Calcula a precisão e retorna        
    precisao = num_acertos / total_elementos
    return precisao
    
def gerar_resultados(lista_perguntas, lista_sql_referencia, qtd_execucoes):
    lista_resultados = []
    if(len(lista_perguntas) != len(lista_sql_referencia)):
        raise ValueError("As listas de perguntas e SQL de referência devem ter o mesmo tamanho.")
    
    for pergunta, sql_referencia in zip(lista_perguntas, lista_sql_referencia):
        lista_tempos = []
        lista_precisao = []
        consistencia = 0.0
        qtd_falhas = 0
        for i in range(qtd_execucoes):
            try:
                #1. Gera a consulta SQL via RPC (Temporizado)
                tempo_inicial = time.time()
                sql_gerado = Conecta.gera_sql(pergunta)
                print(f"[{i+1}] SQL : {sql_gerado}")
                tempo_passado = time.time() - tempo_inicial
                lista_tempos.append(round(tempo_passado, 2)) 
                #2. Executa a consulta SQL gerada e de referência
                (linha_ref, campos_ref) = executa_sql(sql_referencia)
                (linha_ger, campos_res) = executa_sql(sql_gerado)
                #3. Filtra os resultados
                lista_referencia = Conecta.filtra_resultados(linha_ref, campos_ref)
                lista_gerada = Conecta.filtra_resultados(linha_ger, campos_res)
                #4. Calcula a precisão
                precisao = calcular_precisao(lista_referencia, lista_gerada)
                lista_precisao.append(precisao)
            except Exception as e:
                # Se ocorrer um erro, contabiliza a falha e continua
                print(f"Erro na execução {i}: {e}")
                qtd_falhas += 1
                lista_precisao.append(0.0)
        #5. Calcula a consistência    
        consistencia = sum(lista_precisao) / qtd_execucoes
        #6. Cria o objeto Resultado e adiciona à lista
        resultado = Resultado(pergunta, lista_tempos, lista_precisao, consistencia, qtd_falhas, qtd_execucoes)
        lista_resultados.append(resultado)
    return lista_resultados

def testa_gera_sql(lista_sql_ref):
    for sql_ref in lista_sql_ref:
        tuplas_resultados, nome_campos = executa_sql(sql_ref)
        print(f"Resultado da consulta SQL: {tuplas_resultados}")
        print(f"Nome dos campos: {nome_campos}")

        lista_filtrada = Conecta.filtra_resultados(tuplas_resultados, nome_campos)
        print(f"Lista filtrada: {lista_filtrada}")
        print("-" * 50)
        
def testa_gera_precisao():
    lres = [[1, 'alex', 'alexz@ufn.com', '24/01/1970'], 
            [2, 'juca', 'juquis@ufn.com', '23/05/2000']]
    
    lref = [[1, 'alex', 'alexz@ufn.com', '24/01/1970'], 
            [2, 'juca', 'juquis@ufn.com', '23/05/2000']]
    
    precisao = calcular_precisao(lres, lref)
    print(f"Precisão: {precisao:.2f}")

def __main__():
    #testa_gera_precisao()
    #testa_gera_sql(lista_sql_ref)
    
    lista_perguntas = ["Me informe o nome, email e data de nascimento dos usuários que são do tipo 'ADMINISTRADOR'", 
                       "Me informe o nome, sigla e site de cada instituição"]
    
    lista_sql_ref = ["SELECT nome, email, data_nasc FROM usuario_usuario WHERE tipo = 'ADMINISTRADOR'",
                     "SELECT nome, sigla, site FROM instituicao_instituicao"]

    lista_perguntas_final = [
        "Me informe o nome, curso e área de todos os usuários no sistema",
        "Me infome o nome, email e lattes de todos os usuários que são do tipo 'PROFESSOR'",
        "Me informe o nome, email e último acesso de todos os usuarios do tipo 'ADMINISTRADOR'",
        "Me infrme o nome, sigla e site de cada instituição cadastrada no sistema",
        "Me informe o local de execução, area e curso de cada submissão cadastrada",
        "Me informe quantos usuários cadastrados nasceram antes do ano 2000",
        "Me informe o nome, area de conhecimento e curso pós de todos os usuários que tem curso de pós graduação",
        "Me informe o nome do avaliador suplente e o parecer do avaliador suplente e de todas as avaliações",
        "Me informe o nome do avaliador, a data de avaliação do responsável e o parecer do avaliador suplente e de todas as avaliações que foram realizadas pelo avaliador responsável CRISTINA DE FREITAS RODRIGUES",
        "Me informe o a descrição do edital, o nome, email e lattes do responsável e título de todas as submissões relaizadas no edital de numero 2021"
    ]

    lista_sql_ref_final = [
        "SELECT nome, curso_graduacao_vinculado, area_conhecimento_cnpq FROM usuario_usuario",
        "SELECT nome, email, lattes FROM usuario_usuario WHERE tipo = 'PROFESSOR'",
        "SELECT nome, email, last_login FROM usuario_usuario WHERE tipo = 'ADMINISTRADOR'",
        "SELECT nome, sigla, site FROM instituicao_instituicao",
        "SELECT local_execucao, area, curso_graduacao_vinculado FROM submissao_submissao",
        "SELECT COUNT(*) AS total_usuarios FROM usuario_usuario WHERE data_nasc < '2000-01-01'",
        "SELECT nome, area_conhecimento_cnpq, curso_pos_graduacao FROM usuario_usuario WHERE curso_pos_graduacao IS NOT NULL",
        "SELECT u.nome AS avaliador_suplente, a.parecer_avaliador_suplente FROM avaliacao_avaliacao a LEFT JOIN usuario_usuario u ON a.avaliador_suplente = u.id",
        "SELECT u.nome AS avaliador_responsavel, a.dt_avaliacao_responsavel, a.parecer_avaliador_suplente FROM avaliacao_avaliacao a JOIN usuario_usuario u ON a.avaliador_responsavel = u.id WHERE u.nome = 'CRISTINA DE FREITAS RODRIGUES'",
        "SELECT e.descricao, u.nome, u.email, u.lattes, s.titulo FROM submissao_submissao s JOIN edital_edital e ON s.edital = e.id JOIN usuario_usuario u ON s.responsavel = u.id WHERE e.numero = '2021'"
    ]
    # Cria a lista de resultados com 5 ocorrências para cada pergunta na lista.
    lista_resultados = gerar_resultados(lista_perguntas, lista_sql_ref, 5)
    print(*lista_resultados, sep='\n')
    
__main__()