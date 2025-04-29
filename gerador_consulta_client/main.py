from conecta_llm import Conecta
import time

def atualizar_contexto():
    print(f"> Atualizando contexto...")
   
    tempo_inicial = time.time()
    resposta = Conecta.atualiza_contexto()
    tempo_passado = time.time() - tempo_inicial
    
    print(resposta)
    
    tempo_total = f"{tempo_passado:.2f}s"
    return tempo_total

def iniciar_pergunta(pergunta):
    try:        
        # 1. Gerar a consulta SQL via RPC
        print(f"[0.00s] > Gerando consulta SQL...")
        tempo_inicial = time.time()
        resposta_sql = Conecta.gera_sql(pergunta)
        tempo_passado = time.time() - tempo_inicial 
        print(f"[{tempo_passado:.2f}s] | Resposta: \n'{resposta_sql}'\n")

        # 2. Executa a consulta SQL
        print(f"> Aplicando consulta SQL...")
        resposta_execucao = Conecta.executa_sql(resposta_sql)
        tempo_passado = time.time() - tempo_inicial
        print(f"[{tempo_passado:.2f}s] | Resposta: \n{resposta_execucao}\n")
        
        # 3. Retorna o tempo total para gerar resposta
        tempo_total = f"{tempo_passado:.2f}s"
        return tempo_total
    
    except Exception as e:
        return f"Erro ao iniciar o processo: {str(e)}"

def __main__():
    # 1. Atualizar o contexto do banco de dados (Manualmente, somente admin)
    tempo_atualizar = atualizar_contexto()
    print('Tempo total para atualizar contexto: ', tempo_atualizar)
    
    # 2. Faz uma sequência de perguntas
    pergunta = input("Digite sua pergunta: ")
    tempo_pergunta = iniciar_pergunta(pergunta)
    print('Tempo total para criar relatório: ',tempo_pergunta)
    
__main__()