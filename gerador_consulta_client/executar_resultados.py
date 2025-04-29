## Tempo = time.time()
## Precisão = consulta já montada com dados retornados (linha -> referencia *equals)
## Consistencia = quantas vezes ira executar e tem a memsa resposta? (lista[linhas] -> referencia *equals) 
## Falhas = entrou em algum except? (contabiliza)
## Consultas = numero de vezes que faz a mesma pergunta

import sqlite3
import time

from conecta_llm import Conecta
from resultado import Resultado

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
    qtd_falhas = 0
    
    if(len(lista_perguntas) != len(lista_sql_referencia)):
        raise ValueError("As listas de perguntas e SQL de referência devem ter o mesmo tamanho.")
    
    for pergunta, sql_referencia in zip(lista_perguntas, lista_sql_referencia):
        try:
            lista_tempos = []
            lista_precisao = []
            consistencia = 0.0
            
            for i in range(qtd_execucoes):
                #1. Gera a consulta SQL via RPC (Temporizado)
                tempo_inicial = time.time()
                sql_gerado = Conecta.gera_sql(pergunta)
                tempo_passado = time.time() - tempo_inicial
                lista_tempos.append(tempo_passado)
                
                #2. Executa a consulta SQL gerada e de referência
                linha_referencia = Conecta.executa_sql(sql_referencia)
                linha_resultado = Conecta.executa_sql(sql_gerado)
                
                #3. Calcula a precisão
                precisao = calcular_precisao(linha_resultado, linha_referencia)
                lista_precisao.append(precisao)
            
            # 4. Calcula o maior tempo, menor precisão e consistência    
            maior_tempo = max(lista_tempos)
            menor_precisao = min(lista_precisao) 
            consistencia = sum(lista_precisao) / qtd_execucoes
            
            #5. Cria o objeto Resultado e adiciona à lista
            resultado = Resultado(pergunta, maior_tempo, menor_precisao, consistencia, qtd_falhas, qtd_execucoes)
            lista_resultados.append(resultado)
            
        except Exception as e:
            # Caso ocorra algum erro, registra a falha e continua
            print(f"Erro ao processar a pergunta: {e}")
            qtd_falhas += 1
            continue
    return lista_resultados

def __main__():
    lres = [[1, 'alex', 'alexz@ufn.com', '24/01/1970'], [2, 'juca', 'juquis@ufn.com', '23/05/2000']]
    lref = [[1, 'alex', 'alexz@ufn.com', '24/01/1970'], [2, 'juca', 'juquis@ufn.com', '23/05/2000']]
    precisao = calcular_precisao(lres, lref)
    print(f"Precisão: {precisao:.2f}")
    
    lista_perguntas = ["Me informe o nome, email e data de nascimento dos usuários que são do tipo 'ADMINISTRADOR'", 
                       "Me informe o nome, sigla e site de cada instituição cadastrada"]
    
    lista_sql_ref = ["SELECT nome, email, data_nasc FROM usuario_usuario WHERE tipo = 'ADMINISTRADOR'",
                     "SELECT nome, sigla, site FROM instituicao_instituicao"]

    
    # Verifica se a consulta é segura
    Conecta.consulta_sql_safe(lista_sql_ref[0])

    connection = sqlite3.connect("../db.sqlite3")
    cursor = connection.cursor()
    
    with connection:
        cursor.execute(lista_sql_ref[0])
        resultados = cursor.fetchall()
        nome_campos = [i[0].upper() for i in cursor.description]
        cursor.close()

    print(f"Resultado da consulta SQL: {resultados}")
    print(f"Nome dos campos: {nome_campos}")

    lista_filtrada = Conecta.filtra_sql(resultados, nome_campos)
    print(f"Lista filtrada: {lista_filtrada}")
    
__main__()