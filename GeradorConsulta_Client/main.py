from conecta_llm import Conecta
from decouple import config
import time

def iniciar_pergunta(pergunta):
    """
    Função para iniciar o processo de geração de consulta SQL.
    """
    try:        
        # 1. Atualizar o contexto do banco de dados (Manualmente, somente admin)
        print(f"> Atualizando contexto...")
        start_time = time.time()
        resposta = Conecta.atualiza_contexto()
        elapsed_time = time.time() - start_time
        print(f"[{elapsed_time:.2f}s] | Resposta: {resposta}\n")

        # 2. Gerar a consulta SQL via RPC
        print(f"> Gerando consulta SQL...")
        resposta_sql = Conecta.gerar_sql(pergunta)
        elapsed_time = time.time() - start_time
        print(f"[{elapsed_time:.2f}s] | Resposta: \n'{resposta_sql};'\n")

        # 3. Executa a consulta SQL
        print(f"> Aplicando consulta SQL...")
        resposta_execucao = Conecta.executa_sql(resposta_sql)
        elapsed_time = time.time() - start_time
        print(f"[{elapsed_time:.2f}s] | Resposta: {resposta_execucao}\n")
        
        total_time = time.time() - start_time
        return f"[{total_time:.2f}s] | Fim do processo."
  
    except Exception as e:
        return f"Erro ao iniciar o processo: {str(e)}"

def __main__():
    """
    Função principal para iniciar o processo de geração de consulta SQL.
    """
    # Pergunta do usuário
    pergunta = "Me informe o nome, email, cpf e data de nascimento de todos os usuários."

    # Iniciar o processo
    resposta = iniciar_pergunta(pergunta)
    print(resposta)
    
__main__()