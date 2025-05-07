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
        
    connection.close()
    return tuplas_resultados, nome_campos

def calcular_precisao(linha_resultado, linha_referencia):
    total_elementos = len(linha_referencia)
    if total_elementos == 0:
        return 0.0

    acertos = 0
 
    for dado_ref, dado_res in zip(linha_referencia, linha_resultado):
        if dado_ref == dado_res:
            acertos += 1  
            
    precisao = acertos / total_elementos
    
    return precisao
    
def gerar_resultados(lista_perguntas, lista_sql_referencia, qtd_execucoes):
    lista_resultados = []
    
    if(len(lista_perguntas) != len(lista_sql_referencia)):
        raise ValueError("As listas de perguntas e SQL de referência devem ter o mesmo tamanho.")
    
    for pergunta, sql_referencia in zip(lista_perguntas, lista_sql_referencia):
        try:
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
                    print(f"Erro na execução {i}: {e}")
                    qtd_falhas += 1
                    lista_precisao.append(0.0)
            
            #5. Calcula a consistência    
            consistencia = sum(lista_precisao) / qtd_execucoes
            
            #6. Cria o objeto Resultado e adiciona à lista
            resultado = Resultado(pergunta, lista_tempos, lista_precisao, consistencia, qtd_falhas, qtd_execucoes)
            lista_resultados.append(resultado)
            
        except Exception as e:
            # Caso ocorra algum erro, registra a falha e continua
            print(f"Erro ao processar a pergunta: {e}")
        
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
    lista_perguntas = ["Me informe o nome, email e data de nascimento dos usuários que são do tipo 'ADMINISTRADOR'", 
                       "Me informe o nome, sigla e site de cada instituição"]
    
    lista_sql_ref = ["SELECT nome, email, data_nasc FROM usuario_usuario WHERE tipo = 'ADMINISTRADOR'",
                     "SELECT nome, sigla, site FROM instituicao_instituicao"]

    #GROK3 perguntas e ref. geradas usando json
    lista_perguntas_grok3 = [
    "Quais são os nomes das instituições cadastradas?",
    "Quais são os títulos das submissões feitas para o edital com número '2023/01'?",
    "Quais usuários têm o tipo 'PESQUISADOR' e estão ativos?",
    "Quais são as datas de avaliação do responsável e do suplente para a submissão com ID 5?",
    "Quais submissões têm o termo 'saúde' nas palavras-chave e foram submetidas após 01/01/2024?",
    "Quais instituições estão associadas como parceiras da submissão com ID 10?",
    "Quais são os nomes dos colaboradores da submissão com título contendo 'Estudo Clínico'?",
    "Quais avaliações têm parecer do responsável mencionando 'ética' e foram realizadas antes de 01/06/2024?",
    "Quais submissões de um edital que encerrou em 2023 têm um arquivo de relatório final e pertencem à área 'Medicina'?",
    "Quais usuários que colaboram em submissões com parecer de comissão contendo 'pendência' têm curso de pós-graduação e estão vinculados a uma instituição com sigla 'UFSC'?"
    ]

    lista_sql_ref_grok3 = [
        "SELECT nome FROM instituicao_instituicao",
        "SELECT titulo FROM submissao_submissao s JOIN edital_edital e ON s.edital_id = e.id WHERE e.numero = '2023/01'",
        "SELECT nome FROM usuario_usuario WHERE tipo = 'PESQUISADOR' AND is_active = 1",
        "SELECT dt_avaliacao_responsavel, dt_avaliacao_suplente FROM avaliacao_avaliacao WHERE submissao_id = 5",
        "SELECT titulo FROM submissao_submissao WHERE palavras_chave LIKE '%saúde%' AND dt_cadastro_submissao > '2024-01-01'",
        "SELECT i.nome FROM instituicao_instituicao i JOIN submissao_submissao_instituicoes_parceiras sip ON i.id = sip.instituicao_id WHERE sip.submissao_id = 10",
        "SELECT u.nome FROM usuario_usuario u JOIN submissao_submissao_colaborador sc ON u.id = sc.usuario_id JOIN submissao_submissao s ON sc.submissao_id = s.id WHERE s.titulo LIKE '%Estudo Clínico%'",
        "SELECT a.submissao_id FROM avaliacao_avaliacao a WHERE a.parecer_avaliador_responsavel LIKE '%ética%' AND a.dt_avaliacao_responsavel < '2024-06-01'",
        "SELECT s.titulo FROM submissao_submissao s JOIN edital_edital e ON s.edital_id = e.id WHERE e.encerra LIKE '2023%' AND s.arquivo_relatorio_final IS NOT NULL AND s.area = 'Medicina'",
        "SELECT DISTINCT u.nome FROM usuario_usuario u JOIN submissao_submissao_colaborador sc ON u.id = sc.usuario_id JOIN submissao_submissao s ON sc.submissao_id = s.id JOIN comissao_comissao c ON s.id = c.avaliacao_comissao_id JOIN instituicao_instituicao i ON u.instituicao_id = i.id WHERE c.comentario LIKE '%pendência%' AND u.curso_pos_graduacao IS NOT NULL AND i.sigla = 'UFSC'"
    ]

    #testa_gera_precisao()
    #testa_gera_sql(lista_sql_ref)

    lista_resultados = gerar_resultados(lista_perguntas, lista_sql_ref, 5)
    print(*lista_resultados, sep='\n')
    
__main__()